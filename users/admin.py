from django.contrib import admin
from .models import CustomUser
from .forms import CustomUserCreationForm
from django.contrib.auth.admin import UserAdmin

# admin.site.register(CustomUser)

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    add_form = CustomUserCreationForm
    fieldsets = (
        
        (
            'Individuelle Daten',
            {
                'fields': (
                    'custom',
                    'is_email_verified',
                    'address',
                )
            }
        ),
        *UserAdmin.fieldsets,
    )