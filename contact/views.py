from django.shortcuts import render
from .forms import InquiryForm

def contact_view(request):
    """
    Handles the contact form.
    - On GET, it displays the blank form.
    - On POST, it validates the data, saves it, and returns a "thank you" snippet for HTMX.
    """
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            form.save()
            # This renders a partial HTML snippet to be swapped by HTMX
            return render(request, 'contact/partials/thank_you.html')
    else:
        form = InquiryForm()

    return render(request, 'contact/contact_page.html', {'form': form})
