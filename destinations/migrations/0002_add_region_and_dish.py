# Generated migration to add region and staple_dish fields
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('destinations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mappin',
            name='region',
            field=models.CharField(blank=True, help_text="e.g., 'Kiambu', 'Mombasa', 'Nakuru'", max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='mappin',
            name='staple_dish',
            field=models.CharField(blank=True, help_text="Cultural or staple food of this region, e.g., 'Potato Salad', 'Coastal Seafood'", max_length=255, null=True),
        ),
    ]
