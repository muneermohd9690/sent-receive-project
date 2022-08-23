from django.db import models
from django.db.models import F

from prosecutions.models import Prosecutions
from datetime import datetime
#from excel.models import ExcelFile

# Create your models here.
class Items(models.Model):

    model_no= models.CharField(max_length=30,null= True)
    description=models.CharField(max_length=50,null= True )
    total_qty=models.PositiveIntegerField(default=0,null=True)
    created = models.DateTimeField(default=datetime.now())




class ItemDetails(models.Model):
    STATUS = [
        ('In-Stock', 'In-Stock'),
        ('Out-of-Stock', 'Out-of-Stock'),
        ('issued-to', 'issued-to')
    ]
    serial_no = models.CharField(max_length=50,null=True)
    tag_no = models.CharField(max_length=50, null=True)
    rem_qty = models.IntegerField(default=0)
    status = models.CharField(max_length=30, default='In-stock', choices=STATUS)
    model_no=models.ForeignKey(Items,on_delete= models.CASCADE)
    issued_to =models.ForeignKey(Prosecutions,on_delete=models.CASCADE)
    employee_name=models.CharField(max_length=50,null=True)
    employee_designation = models.CharField(max_length=50, null=True)
    created = models.DateTimeField(default=datetime.now())







