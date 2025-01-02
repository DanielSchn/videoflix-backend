from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
class Video(models.Model):
    """
    Represents a video object in the system, including metadata, different resolution versions,
    and thumbnails.
    """
    original_file = models.FileField(upload_to='videos/originals/', blank=True, null=True)
    video_480p = models.FileField(upload_to='videos/480p/', blank=True, null=True)
    video_720p = models.FileField(upload_to='videos/720p/', blank=True, null=True)
    video_1080p = models.FileField(upload_to='videos/1080p/', blank=True, null=True)
    thumbnail = models.FileField(upload_to='img/', blank=True, null=True, help_text='Bitte Datei im Format beliebigerName_erlaubteKategorie.jpg oder .png! Erlaubte Kategorien: sports, documentary, romance, crime')
    title = models.CharField(max_length=250)
    description = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=50 , null=True, blank=True)

    def __str__(self):
        return self.title
    

class VideoProgress(models.Model):
    """
    Tracks a user's progress in watching a particular video, including the current playback position.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video_name = models.CharField(max_length=150)
    current_time = models.FloatField()

    def __str__(self):
        return f'{self.user} - {self.video_name} - {self.current_time}'