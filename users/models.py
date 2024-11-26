from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    custom = models.TextField(max_length=1000, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)
    registration_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    
    class Meta:
        ordering = ['email']
        verbose_name = "User"
        verbose_name_plural = "User"