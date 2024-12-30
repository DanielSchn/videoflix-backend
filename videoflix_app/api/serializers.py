from rest_framework import serializers
from videoflix_app.models import Video, VideoProgress

class VideoSerializer(serializers.ModelSerializer):
    """
    Serializer for the Video model.

    This serializer handles the conversion between the `Video` model and JSON representation, including
    validation and serialization of fields. It also handles file upload for video files.

    Fields:
        - `id`: The unique identifier for the video (read-only).
        - `title`: The title of the video.
        - `description`: A short description of the video.
        - `created_at`: The timestamp of when the video was created (read-only).
        - `video_480p`, `video_720p`, `video_1080p`: The URLs or file paths to different resolution versions of the video (read-only).
        - `thumbnail`: A file path or URL to the video thumbnail.
        - `category`: The category or genre of the video (read-only).
        - `original_file`: A file input field for uploading the original video file (write-only).

    Configuration:
        - The `original_file` field is write-only, meaning it is used for input but will not appear in the output.
        - `read_only_fields`: Specifies that certain fields (`video_480p`, `video_720p`, `video_1080p`, and `category`) should be read-only and not updated through this serializer.

    Example Usage:
        - To serialize a `Video` object:
            video = Video.objects.get(id=1)
            serializer = VideoSerializer(video)
            serialized_data = serializer.data
        - To deserialize and save a new `Video` object:
            data = {
                "title": "My Video",
                "description": "Description of my video",
                "original_file": some_file,
            }
            serializer = VideoSerializer(data=data)
            if serializer.is_valid():
                serializer.save()

    Methods:
        - `is_valid()`: Validates the input data (e.g., checking file types).
        - `save()`: Saves the new video, including handling the video file.
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

    Fields:
        - `id`: The unique identifier for the video progress (read-only).
        - `user`: The user who is watching the video (read-only).
        - `video_name`: The name or identifier of the video being watched.
        - `current_time`: The current time (in seconds) of the video that the user has watched.

    Configuration:
        - `read_only_fields`: Specifies that the `user` field is read-only and should not be updated via the serializer.

    Example Usage:
        - To serialize a `VideoProgress` object:
            progress = VideoProgress.objects.get(id=1)
            serializer = VideoProgressSerializer(progress)
            serialized_data = serializer.data
        - To deserialize and save a new `VideoProgress` object:
            data = {
                "user": user_instance,
                "video_name": "Example Video",
                "current_time": 120,
            }
            serializer = VideoProgressSerializer(data=data)
            if serializer.is_valid():
                serializer.save()

    Methods:
        - `is_valid()`: Validates the input data (e.g., checking that `current_time` is a valid number).
        - `save()`: Saves the video progress for the user, updating the `current_time` field.

    Notes:
        - The `user` field is automatically set to the current user, as it is read-only and not expected to be updated by the client.
    """
    class Meta:
        model = VideoProgress
        fields = ['id', 'user', 'video_name', 'current_time']
        read_only_fields = ['user']
