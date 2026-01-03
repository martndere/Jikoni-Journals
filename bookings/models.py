from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Booking(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    tour_date = models.DateField()
    guests = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(20)]
    )
    special_requirements = models.TextField(blank=True)
    is_paid = models.BooleanField(default=False)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    stripe_checkout_id = models.CharField(max_length=255, blank=True, null=True)
    # M-Pesa Fields
    mpesa_receipt = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    mpesa_checkout_request_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.tour_date}"