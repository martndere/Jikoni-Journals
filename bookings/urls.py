from django.urls import path
from . import views

urlpatterns = [
    path('new/', views.booking_create_view, name='booking_create'),
    path('checkout/<int:pk>/', views.create_checkout_session, name='booking_checkout'),
    path('webhook/stripe/', views.stripe_webhook, name='stripe_webhook'),
    path('success/', views.booking_success_view, name='booking_success'),
    path('mpesa/pay/<int:pk>/', views.initiate_mpesa_payment, name='mpesa_pay'),
    path('mpesa/callback/', views.mpesa_callback, name='mpesa_callback'),
]