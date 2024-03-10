from django.db import models
from prosecutions.models import Prosecutions
from items.models import Items
from datetime import datetime
from datetime import date
# from django.conf import settings
from django.utils import timezone
from sent_items.models import CartItem
#import datetime
from django.contrib.contenttypes.fields import GenericRelation

from django.utils import timezone


# Create your models here.
class Toners(models.Model):

    toner_model = models.CharField(max_length=100,null=True)
    toner_printer = models.ForeignKey(Items,on_delete=models.CASCADE)
    total_qty = models.PositiveIntegerField(default=0,null=True)
    remaining_qty = models.PositiveIntegerField(default=0,null=True)
    created=models.DateTimeField(default=timezone.now)
    # objects = models.Manager()
    #history = HistoricalRecords()

class TonerDetails(models.Model):
    STATUS = [
        ('In-Stock', 'In-Stock'),
        ('Out-of-Stock', 'Out-of-Stock'),
    ]
    toner_model = models.ForeignKey(Toners,on_delete=models.CASCADE)
    status = models.CharField(max_length=30,default='In-Stock',choices=STATUS)
    issued_to = models.ForeignKey(Prosecutions, on_delete=models.CASCADE,default="31")
    employee_name = models.CharField(max_length=300,null=True)
    employee_designation = models.CharField(max_length=300,null=True)
    created=models.DateTimeField(default=timezone.now)
    date_dispatched=models.DateTimeField(default=timezone.now)


    cart_item = GenericRelation(CartItem, related_query_name='tonerdetails',on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date_dispatched']