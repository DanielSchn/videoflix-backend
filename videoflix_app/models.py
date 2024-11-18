from django.db import models

# Create your models here.
class Video(models.Model):

    video_file = models.FileField(upload_to='videos', blank=True, null=True)
    title = models.CharField(max_length=250)
    description = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title