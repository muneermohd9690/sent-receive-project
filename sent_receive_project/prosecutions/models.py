
from django.db import models
from datetime import datetime
from simple_history.models import HistoricalRecords
from django.utils import timezone

class Prosecutions(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=300,default="none")
    created = models.DateTimeField(default=timezone.now)
    #history = HistoricalRecords()










