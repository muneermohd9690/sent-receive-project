from django.db import models
from prosecutions.models import Prosecutions
from items.models import ItemDetails
from items.models import Items
from toners.models import Toners,TonerDetails

# Create your models here.
class ExcelFile(models.Model):
    file = models.FileField(upload_to="excel")
