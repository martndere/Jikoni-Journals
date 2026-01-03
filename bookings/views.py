import stripe
import requests
import base64
import json
from datetime import datetime
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from .forms import BookingForm
from .models import Booking

# Initialize Stripe (Ensure these are in your settings.py)
stripe.api_key = getattr(settings, 'STRIPE_SECRET_KEY', 'sk_test_placeholder')

# Configuration: price per guest and guest threshold for paywall
PRICE_PER_GUEST = 15.00
PAYWALL_GUEST_THRESHOLD = 3


def booking_create_view(request):
    """
    Handles the creation of a new booking.
    - On GET, displays a blank booking form.
    - On POST, validates and either saves immediately or presents a paywall when the
      booking meets the paywall condition (e.g., number_of_guests >= threshold).
    """
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            # calculate amount due
            booking.amount_due = round(booking.guests * PRICE_PER_GUEST, 2)

            if booking.guests >= PAYWALL_GUEST_THRESHOLD:
                # Save booking in unpaid state and show paywall partial
                booking.is_paid = False
                booking.save()
                return render(request, 'bookings/partials/booking_paywall.html', {'booking': booking})

            # Small bookings: save and return success immediately
            booking.is_paid = False
            booking.save()
            return render(request, 'bookings/partials/booking_success.html', {'booking': booking})
    else:
        form = BookingForm()

    return render(request, 'bookings/booking_create.html', {'form': form})


def create_checkout_session(request, pk):
    """
    Creates a Stripe Checkout Session and redirects the user to the payment page.
    """
    booking = get_object_or_404(Booking, pk=pk)
    
    # Create Stripe Checkout Session
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': int(booking.amount_due * 100), # Stripe expects cents
                    'product_data': {
                        'name': f'Culinary Tour Booking ({booking.guests} Guests)',
                        'description': f'Booking for {booking.name} on {booking.tour_date}',
                    },
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri(reverse('booking_success')) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.build_absolute_uri(reverse('booking_create')),
            metadata={
                'booking_id': booking.id
            }
        )
        booking.stripe_checkout_id = checkout_session.id
        booking.save()
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
def stripe_webhook(request):
    """
    Handles Stripe webhooks to confirm payment securely.
    """
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = getattr(settings, 'STRIPE_WEBHOOK_SECRET', '')

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponseBadRequest()

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        booking_id = session.get('metadata', {}).get('booking_id')
        
        if booking_id:
            try:
                booking = Booking.objects.get(id=booking_id)
                booking.is_paid = True
                booking.save()
                
                # Send confirmation email
                subject = f"Booking Confirmed: {booking.name}"
                message = f"Hi {booking.name},\n\nYour booking for {booking.guests} guests on {booking.tour_date} is confirmed!\n\nThank you,\nJikoni Journals"
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [booking.email]
                send_mail(subject, message, from_email, recipient_list)
            except Booking.DoesNotExist:
                pass

    return JsonResponse({'status': 'success'})

def booking_success_view(request):
    return render(request, 'bookings/partials/booking_success.html')

# --- M-Pesa Integration ---

def get_mpesa_access_token():
    """Generates an OAuth access token for M-Pesa."""
    consumer_key = getattr(settings, 'MPESA_CONSUMER_KEY', '')
    consumer_secret = getattr(settings, 'MPESA_CONSUMER_SECRET', '')
    api_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    
    try:
        r = requests.get(api_url, auth=(consumer_key, consumer_secret))
        return r.json().get('access_token')
    except Exception as e:
        print(f"M-Pesa Auth Error: {e}")
        return None

def initiate_mpesa_payment(request, pk):
    """Initiates an STK Push to the user's phone."""
    if request.method != 'POST':
        return HttpResponseBadRequest("POST required")
        
    booking = get_object_or_404(Booking, pk=pk)
    phone = request.POST.get('phone_number')
    
    if not phone:
        return JsonResponse({'error': 'Phone number is required'}, status=400)
    
    # Format phone: 07xx to 2547xx
    if phone.startswith('0'):
        phone = '254' + phone[1:]
        
    booking.phone_number = phone
    booking.save()

    access_token = get_mpesa_access_token()
    if not access_token:
        return JsonResponse({'error': 'Failed to connect to M-Pesa'}, status=500)

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    business_short_code = getattr(settings, 'MPESA_SHORTCODE', '174379')
    passkey = getattr(settings, 'MPESA_PASSKEY', '')
    password_str = f"{business_short_code}{passkey}{timestamp}"
    password = base64.b64encode(password_str.encode()).decode()

    callback_url = request.build_absolute_uri(reverse('mpesa_callback'))
    print(f"\n🚀 Initiating M-Pesa Payment...")
    print(f"📡 Callback URL sent to Safaricom: {callback_url}\n")

    payload = {
        "BusinessShortCode": business_short_code,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": int(booking.amount_due), # M-Pesa accepts integers
        "PartyA": phone,
        "PartyB": business_short_code,
        "PhoneNumber": phone,
        "CallBackURL": callback_url,
        "AccountReference": f"Booking {booking.id}",
        "TransactionDesc": "Tour Booking"
    }

    headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}
    
    try:
        response = requests.post('https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest', json=payload, headers=headers)
        data = response.json()
        
        if data.get('ResponseCode') == '0':
            booking.mpesa_checkout_request_id = data.get('CheckoutRequestID')
            booking.save()
            return JsonResponse({'status': 'success', 'message': 'Check your phone to enter PIN'})
        else:
            return JsonResponse({'status': 'error', 'message': data.get('errorMessage', 'Failed')})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def mpesa_callback(request):
    """Receives the payment result from M-Pesa."""
    if request.method == 'POST':
        try:
            body = request.body.decode('utf-8')
            data = json.loads(body)
            
            # Log for debugging
            print("\n--- M-Pesa Callback Data ---")
            print(json.dumps(data, indent=2))
            print("----------------------------\n")

            stk_callback = data.get('Body', {}).get('stkCallback', {})
            result_code = stk_callback.get('ResultCode')
            checkout_id = stk_callback.get('CheckoutRequestID')

            # ResultCode 0 means successful payment
            if result_code == 0:
                booking = Booking.objects.filter(mpesa_checkout_request_id=checkout_id).first()
                if booking:
                    booking.is_paid = True
                    # Extract Receipt Number
                    meta_items = stk_callback.get('CallbackMetadata', {}).get('Item', [])
                    for item in meta_items:
                        if item.get('Name') == 'MpesaReceiptNumber':
                            booking.mpesa_receipt = item.get('Value')
                            break
                    booking.save()
                    print(f"✅ Booking {booking.id} confirmed via M-Pesa!")

                    # Send confirmation email
                    subject = f"Booking Confirmed: {booking.name}"
                    message = f"Hi {booking.name},\n\nYour booking for {booking.guests} guests on {booking.tour_date} is confirmed via M-Pesa!\nReceipt: {booking.mpesa_receipt}\n\nThank you,\nJikoni Journals"
                    from_email = settings.DEFAULT_FROM_EMAIL
                    recipient_list = [booking.email]
                    send_mail(subject, message, from_email, recipient_list)
            else:
                print(f"❌ Payment failed: {stk_callback.get('ResultDesc')}")

        except Exception as e:
            print(f"Error processing callback: {e}")
            
    return JsonResponse({'status': 'received'})
