from django.db import models
from django.db.models import F
from django.apps import apps

from sent_items.models import CartItem
from prosecutions.models import Prosecutions
from contracts.models import Contracts
from datetime import datetime
from datetime import date
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericRelation
from sent_items.models import CartItem


# from sent_items.models import CartItem
# import sent_items.models
# from excel.models import ExcelFile

# Create your models here.
class Items(models.Model):
    model_no = models.CharField(max_length=300, null=True)
    description = models.CharField(max_length=500, null=True)
    total_qty = models.PositiveIntegerField(default=0, null=True)
    remaining_qty = models.PositiveIntegerField(default=0, null=True)
    created = models.DateTimeField(default=timezone.now)



class ItemDetails(models.Model):
    STATUS = [
        ('In-Stock', 'In-Stock'),
        ('Out-of-Stock', 'Out-of-Stock'),
        ('issued-to', 'issued-to')
    ]
    serial_no = models.CharField(max_length=500, null=True)
    tag_no = models.CharField(max_length=500, null=True)
    room_tag = models.CharField(max_length=500, null=True)
    status = models.CharField(max_length=30, default='In-stock', choices=STATUS)
    model_no = models.ForeignKey(Items, on_delete=models.CASCADE)
    issued_to = models.ForeignKey(Prosecutions, on_delete=models.CASCADE)
    employee_name = models.CharField(max_length=500, null=True)
    employee_designation = models.CharField(max_length=500, null=True)
    created = models.DateTimeField(default=timezone.now)
    date_dispatched = models.DateTimeField(default=timezone.now)
    lpo_no = models.ForeignKey(Contracts, on_delete=models.SET_NULL, null=True, blank=True)
    pdf_file = models.FileField(upload_to='pdfs/itemdetails/', blank=True, null=True, default='')
    cart_item = GenericRelation(CartItem, related_query_name='itemdetails')



    class Meta:
        ordering = ['-date_dispatched']