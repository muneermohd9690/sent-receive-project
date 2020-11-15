from django.db import models

# Create your models here.
class Items(models.Model ):
    STATUS=(
        ('In-Stock','In-Stock'),
        ('Out-of-Stock','Out-of-Stock'),
        ('available','available')
    )
    serial_no = models.CharField(max_length= 50,null= True )
    model_no= models.CharField(max_length=30,null= True )
    description=models.CharField(max_length=50,null= True )
    total_qty=models.IntegerField(default= 0,null= True )
    rem_qty = models.IntegerField()
    status=models.CharField(max_length= 30,default='in-stock',choices=STATUS)


