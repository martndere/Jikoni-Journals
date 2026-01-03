# Generated migration to add payment fields to Booking
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='amount_due',
            field=models.DecimalField(default=0.0, help_text='Calculated amount due for this booking.', max_digits=8, decimal_places=2),
        ),
        migrations.AddField(
            model_name='booking',
            name='is_paid',
            field=models.BooleanField(default=False, help_text='Has this booking been paid?'),
        ),
    ]
