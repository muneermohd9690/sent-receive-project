from django.db import models
from prosecutions.models import Prosecutions
from items.models import ItemDetails
from items.models import Items
from toners.models import Toners,TonerDetails
from sent_items.models import CartItem,Cart
from django.db import models
from datetime import datetime
from django.utils import timezone

# Create your models here.
class Forms(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=30,default="none")
    created = models.DateTimeField(default=timezone.now)

