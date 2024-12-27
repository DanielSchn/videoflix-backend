from rest_framework import serializers
from videoflix_app.models import Video, VideoProgress

class VideoSerializer(serializers.ModelSerializer):
    original_file = serializers.FileField(write_only=True)

    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'created_at', 'video_480p', 'video_720p', 'video_1080p', 'thumbnail', 'category', 'original_file']
        read_only_fields = ['video_480p', 'video_720p', 'video_1080p', 'category']


class VideoProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoProgress
        fields = ['id', 'user', 'video_name', 'current_time']
        read_only_fields = ['user']
