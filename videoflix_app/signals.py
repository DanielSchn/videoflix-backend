from .models import Video
from .tasks import convert_video
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
import os
import django_rq


@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    if created:
        print('New video created')
        queue = django_rq.get_queue('default', autocommit=True)
        queue.enqueue(convert_video, instance.original_file.path, instance)
    else:
        print('Edited video details saved')


@receiver(post_delete, sender=Video)
def video_post_delete(sender, instance, *args, **kwargs):
    if instance.original_file and instance.original_file.name:
        original_path = instance.original_file.path
        if os.path.isfile(original_path):
            os.remove(original_path)
            print('Originaldatei gelöscht!')

    resolutions = ['480p', '720p', '1080p']
    for resolution in resolutions:
        
        field_name = f'video_{resolution}'
        video_field = getattr(instance, field_name, None)
        
        if video_field and video_field.name:
            converted_path = video_field.path
            if os.path.isfile(converted_path):
                os.remove(converted_path)
                print(f'{resolution} Datei gelöscht!')

    print('Video-Objekt gelöscht!')