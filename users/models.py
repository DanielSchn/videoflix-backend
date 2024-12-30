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

    Configuration:
        - `USERNAME_FIELD`: Specifies that the `email` field will be used for authentication.
        - `REQUIRED_FIELDS`: Specifies that the `username` field is required when creating a user via the Django admin interface.

    Methods:
        - `__str__(self)`: Returns the user's email as the string representation of the user.

    Meta:
        - `ordering`: Specifies that the users will be ordered by their email field.
        - `verbose_name` and `verbose_name_plural`: Specifies the human-readable singular and plural names for the model.

    Example Usage:
        - To create a user with this custom model:
            user = CustomUser.objects.create_user(email="user@example.com", username="user", password="password123")

    Permissions and Authentication:
        - The `email` field is used as the unique identifier for the user instead of the default `username`.
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