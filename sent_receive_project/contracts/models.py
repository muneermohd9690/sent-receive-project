from django.db import models
from django.utils import timezone


# Create your models here.
class Contracts(models.Model):
    lpo_no = models.CharField(max_length=300, null=True)
    warranty_range = [(i, str(i)) for i in range(1, 11)]
    warranty_years = models.IntegerField(
        choices=warranty_range,
        default=1,  # Default value (optional)
    )
    warranty_start = models.DateTimeField(default=timezone.now)
    warranty_end = models.DateTimeField(default=timezone.now)
    purchased_by_choice = [
        ('local', 'Local Finance'),
        ('central', 'Central Finance')
    ]
    purchased_by = models.CharField(
        max_length=20,  # Set the maximum length based on your requirements
        choices=purchased_by_choice,
        default='central',  # Default value (optional)
    )
    purchased_date = models.DateTimeField(default=timezone.now)
    pdf_file = models.FileField(upload_to='pdfs/', blank=True, null=True, default='')


