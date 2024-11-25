from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    custom = models.TextField(max_length=1000, default='')
    phone = models.CharField(max_length=25, default='')
    address = models.CharField(max_length=100, default='')