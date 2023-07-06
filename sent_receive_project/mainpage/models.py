from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# Create your models here.
from django import forms

class CreateUserForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','password1','password2']