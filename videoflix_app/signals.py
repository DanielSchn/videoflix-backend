from .models import Video
from .tasks import convert_video
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
import os
import django_rq


@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for the `post_save` signal of the `Video` model. This function 
    is triggered whenever a new `Video` instance is saved.

    - If the video instance is newly created, it prints a success message and enqueues 
      a task to convert the original video to different resolutions (480p, 720p, 1080p) using a task queue.
    - If the video instance is updated (not created), it prints a message that the details 
      of the video were saved, but does not trigger any additional actions.

    Args:
        sender (Model): The model class that sent the signal.
        instance (Video): The actual `Video` instance that was saved.
        created (bool): A boolean that is `True` if the instance was created, `False` if it was updated.
        kwargs (dict): Additional keyword arguments.
    """
    if created:
        print('New video created')
        queue = django_rq.get_queue('default', autocommit=True)
        queue.enqueue(convert_video, instance.original_file.path, instance)
    else:
        print('Edited video details saved')


@receiver(post_delete, sender=Video)
def video_post_delete(sender, instance, *args, **kwargs):
    """
    Signal handler for the `post_delete` signal of the `Video` model. This function 
    is triggered whenever a `Video` instance is deleted.

    - It deletes the associated video files from the file system, including:
        - The original video file
        - The converted video files in various resolutions (480p, 720p, 1080p)
        - The thumbnail image
    - It prints messages to indicate which files were deleted and that the video object itself was deleted.

    Args:
        sender (Model): The model class that sent the signal.
        instance (Video): The `Video` instance that was deleted.
        args (tuple): Additional positional arguments.
        kwargs (dict): Additional keyword arguments.
    """
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

    if instance.thumbnail and instance.thumbnail.name:
        thumbnail_path = instance.thumbnail.path
        if os.path.isfile(thumbnail_path):
            os.remove(thumbnail_path)
            print('Thumbnail-Datei gelöscht!')

    print('Video-Objekt gelöscht!')