
from django.db import models
from datetime import datetime

from django.utils import timezone

class Prosecutions(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=300,default="none")
    created = models.DateTimeField(default=timezone.now)












