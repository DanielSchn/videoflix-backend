from .models import Video
from .tasks import convert_480p, simple_task, check_ffmpeg
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
import os
import django_rq


@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    if created:
        print('New video created')
        #queue = django_rq.get_queue('default')
        #queue.enqueue(simple_task, '/path/to/file')
        #queue = django_rq.get_queue('default', autocommit=True)
        #queue.enqueue(check_ffmpeg)
        #queue.enqueue(convert_480p, instance.video_file.path)
        convert_480p(instance.video_file.path)
    else:
        print('Edited video details saved')
        


@receiver(post_delete, sender=Video)
def video_post_delete(sender, instance, *args, **kwargs):
    if instance.video_file:
        path = instance.video_file.path
        if os.path.isfile(path):
            os.remove(path)
            print('File deleted!')