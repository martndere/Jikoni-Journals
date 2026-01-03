from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['name', 'email', 'tour_date', 'guests', 'special_requirements']
        widgets = {
            'tour_date': forms.DateInput(attrs={'type': 'date'}),
            'guests': forms.NumberInput(attrs={'min': 1, 'max': 20}),
            'special_requirements': forms.Textarea(attrs={
                'rows': 4, 
                'placeholder': 'Dietary restrictions, accessibility needs, etc.'
            }),
        }
        labels = {
            'name': 'Full Name',
            'email': 'Email Address',
            'tour_date': 'Preferred Tour Date',
            'guests': 'Number of Guests',
        }