from rest_framework import serializers
from videoflix_app.models import Video, VideoProgress

class VideoSerializer(serializers.ModelSerializer):
    """
    Serializer for the Video model.

    This serializer handles the conversion between the `Video` model and JSON representation, including
    validation and serialization of fields. It also handles file upload for video files.
    """
    original_file = serializers.FileField(write_only=True)

    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'created_at', 'video_480p', 'video_720p', 'video_1080p', 'thumbnail', 'category', 'original_file']
        read_only_fields = ['video_480p', 'video_720p', 'video_1080p', 'category']


class VideoProgressSerializer(serializers.ModelSerializer):
    """
    Serializer for the VideoProgress model.

    This serializer handles the conversion between the `VideoProgress` model and JSON representation, 
    focusing on tracking a user's progress in watching a video. It serializes data such as the user, 
    video name, and current watch time.
    """
    class Meta:
        model = VideoProgress
        fields = ['id', 'user', 'video_name', 'current_time']
        read_only_fields = ['user']
