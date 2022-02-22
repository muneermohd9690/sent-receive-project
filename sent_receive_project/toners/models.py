from django.db import models
from prosecutions.models import Prosecutions
from items.models import Items
from datetime import datetime

# Create your models here.
class Toners(models.Model):

    toner_model = models.CharField(max_length=10,null=True)
    toner_printer = models.ForeignKey(Items,on_delete=models.CASCADE)
    total_qty = models.PositiveIntegerField(default=0,null=True)
    remaining_qty = models.PositiveIntegerField(default=0,null=True)
    created=models.DateTimeField(default=datetime.now())

    objects = models.Manager()

class TonerDetails(models.Model):
    STATUS = [
        ('In-Stock', 'In-Stock'),
        ('Out-of-Stock', 'Out-of-Stock'),
    ]
    toner_model = models.ForeignKey(Toners,on_delete=models.CASCADE)
    status = models.CharField(max_length=30,default='In-Stock',choices=STATUS)
    issued_to = models.ForeignKey(Prosecutions, on_delete=models.CASCADE)
    employee_name = models.CharField(max_length=30,null=True)
    employee_designation = models.CharField(max_length=30,null=True)
    created = models.DateTimeField(default=datetime.now())
