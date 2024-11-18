from django.contrib import admin
from .models import Video


class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'created_at']
    list_filter = ['title', 'created_at']

# Register your models here.
admin.site.register(Video, VideoAdmin)