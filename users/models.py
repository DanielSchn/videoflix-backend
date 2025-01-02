from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    Custom user model extending AbstractUser.

    This class extends the default Django `AbstractUser` model to provide additional
    fields and functionality specific to the application's user model.

    Fields:
        - custom: A TextField for custom data (up to 1000 characters), optional.
        - address: A CharField for storing the user's address, optional.
        - is_email_verified: A BooleanField to track whether the user's email has been verified.
        - registration_date: A DateTimeField that automatically sets the registration date when a user is created.
        - email: A unique EmailField used as the primary identifier for the user.
    """
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