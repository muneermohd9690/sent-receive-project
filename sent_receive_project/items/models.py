from django.db import models
from prosecutions.models import Prosecutions
from datetime import datetime

# Create your models here.
class Items(models.Model):

    model_no= models.CharField(max_length=30,null= True )
    description=models.CharField(max_length=50,null= True )
    total_qty=models.IntegerField(default= 0,null= True )
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False)
    date_updated = models.DateTimeField(auto_now_add=False, auto_now=True)



class ItemDetails(models.Model):
    STATUS = (
        ('In-Stock', 'In-Stock'),
        ('Out-of-Stock', 'Out-of-Stock'),
        ('issued-to', 'issued-to')
    )
    serial_no = models.CharField(max_length=50, null=True)
    rem_qty = models.IntegerField(default=0)
    status = models.CharField(max_length=30, default='in-stock', choices=STATUS)
    model_no=models.ForeignKey(Items,on_delete= models.CASCADE)
    issued_to =models.ForeignKey(Prosecutions,on_delete=models.CASCADE)
    employee_name=models.CharField(max_length=50,null=True)
    date_created = models.DateTimeField(auto_now_add=True,auto_now=False)
    date_updated = models.DateTimeField(auto_now_add=False,auto_now=True)
