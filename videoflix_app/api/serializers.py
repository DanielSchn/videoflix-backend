from rest_framework import serializers
from videoflix_app.models import Video

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'created_at', 'video_480p', 'video_720p', 'video_1080p', 'original_file']
