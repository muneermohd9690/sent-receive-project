from django.db import models
from datetime import datetime


class Prosecutions(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=30,default="none")
    created = models.DateTimeField(default=datetime.now())










