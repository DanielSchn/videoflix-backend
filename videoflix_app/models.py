from django.db import models

# Create your models here.
class Video(models.Model):

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