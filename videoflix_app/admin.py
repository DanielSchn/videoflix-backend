from django.contrib import admin
from .models import Video, VideoProgress
from import_export.admin import ImportExportModelAdmin
from import_export import resources


class VideoResource(resources.ModelResource):
    
    class Meta:
        model = Video

@admin.register(Video)
class VideoAdmin(ImportExportModelAdmin):
    resource_class = VideoResource
    list_display = ['title', 'description', 'created_at', 'video_480p']
    list_filter = ['title', 'created_at']

admin.site.register(VideoProgress)