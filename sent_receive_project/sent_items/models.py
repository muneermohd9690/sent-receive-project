from django.db import models
from datetime import datetime
from prosecutions.models import Prosecutions
from items.models import ItemDetails
from toners.models import TonerDetails

# Create your models here.
class SentItems(models.Model):
    send_date = models.DateTimeField(default=datetime.now())
    send_to = models.CharField(max_length=30)
    product = models.CharField(max_length=30)
    model_no = models.CharField(max_length=30)
    serial_no = models.CharField(max_length=30)
    received_by = models.CharField(max_length=30)

class Cart(models.Model):
    cartitems = models.ManyToManyField (TonerDetails ,null=True, blank=True )
    date_created = models.DateTimeField (default=datetime.now())
    active = models.BooleanField (default= True)
