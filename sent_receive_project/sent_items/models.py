from django.db import models
from datetime import datetime
from prosecutions.models import Prosecutions
from items.models import Items
from toners.models import TonerDetails,Toners
from django.contrib.auth.models import User


# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_created = models.DateTimeField(default=datetime.now())
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

class CartItem(models.Model):
    product = models.ForeignKey(TonerDetails, on_delete=models.SET_NULL, blank=True, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=0)
    #created1 = models.DateTimeField(default=datetime.date())

class SentItems(models.Model):
    send_date = models.DateTimeField(default=datetime.now())
    send_to = models.CharField(max_length=30)
    product = models.ForeignKey(CartItem, on_delete=models.SET_NULL, blank=True, null=True)
    model_no = models.CharField(max_length=30)
    serial_no = models.CharField(max_length=30)
    received_by = models.CharField(max_length=30)


