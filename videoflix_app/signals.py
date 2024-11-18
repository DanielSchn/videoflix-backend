from .models import Video
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
import os


@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    if created:
        print('New video created')
    else:
        print('Edited video details saved')


@receiver(post_delete, sender=Video)
def video_post_delete(sender, instance, *args, **kwargs):
    if instance.video_file:
        path = instance.video_file.path
        if os.path.isfile(path):
            os.remove(path)
            print('File deleted!')