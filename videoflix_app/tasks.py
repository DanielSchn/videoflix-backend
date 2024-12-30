import subprocess
import os
from django.core.files import File
from .models import Video


RESOLUTIONS = {
    "480p": {"size": "hd480", "field": "video_480p"},
    "720p": {"size": "hd720", "field": "video_720p"},
    "1080p": {"size": "hd1080", "field": "video_1080p"},
}
ALLOWED_CATEGORIES = os.environ.get('ALLOWED_CATEGORIES').split(',')
    

def convert_video(source, video_instance):
    """
    Converts a given video file into multiple resolutions (defined in RESOLUTIONS) 
    and saves the converted videos into the associated fields of the provided `video_instance`.

    - It takes the original video (source file), converts it into different resolutions using `ffmpeg`,
      and stores the resulting files in the appropriate fields on the `Video` model.
    - The original file is deleted after the conversion, and the category of the video is set.
    
    Args:
        source (str): The path to the source video file that needs to be converted.
        video_instance (Video): The `Video` model instance where the converted files will be saved.

    Returns:
        Video | None: The updated `video_instance` if successful, or `None` if an error occurs.
    """
    if not os.path.isfile(source):
        print(f'Die Eingabedatei existiert nicht!')
        return None

    try:
        for resolution, config in RESOLUTIONS.items():
            file, _ = os.path.splitext(source)
            target = file + f'_{resolution}.mp4'

            cmd = f'ffmpeg -i "{source}" -s {config["size"]} -c:v libx264 -crf 23 -c:a aac -strict -2 "{target}"'
            print(f'Konvertiere {resolution}...')

            subprocess.run(cmd, capture_output=False, shell=True, check=True)

            with open(target, 'rb') as f:
                field_name = config['field']
                getattr(video_instance, field_name).save(os.path.basename(target), File(f), save=True)

            os.remove(target)
            print(f'{resolution} erfolgreich konvertiert und gespeichert!')

        os.remove(source)
        video_instance.original_file.delete(save=False)

        set_video_category(video_instance)

        video_instance.save()
        print(f'Alle Auflösungen wurden konvertiert und gespeichert!')
        return video_instance

    except Exception as e:
        print(f'Fehler bei der Verarbeitung der Videos: {str(e)}!')
        return None
    

def set_video_category_for_all():
    """
    Sets the category for all videos in the database by calling `set_video_category` 
    for each video instance.

    - This function loops through all `Video` instances and assigns categories 
      based on the thumbnail filename.

    Returns:
        None
    """
    videos = Video.objects.all()
    for video in videos:
        set_video_category(video)


def extract_category_from_filename(filename):
    """
    Extracts a category from the filename of a video thumbnail.

    - This function checks if the filename contains any category listed in `ALLOWED_CATEGORIES`.
      If a match is found, the corresponding category is returned.
    - If no category is found, `None` is returned.

    Args:
        filename (str): The filename of the thumbnail to extract the category from.

    Returns:
        str | None: The category found in the filename or `None` if no category matches.
    """
    for category in ALLOWED_CATEGORIES:
        if category in filename.lower():
            return category
    return None


def set_video_category(video_instance):
    """
    Sets the category for a given `video_instance` based on the filename of its thumbnail.

    - The category is determined by checking the thumbnail's filename using `extract_category_from_filename`.
    - If a valid category is found, it is assigned to the `category` field of the video instance, 
      and the video is saved.
    - If no category is found, a message is logged indicating that no valid category was found.

    Args:
        video_instance (Video): The `Video` model instance whose category needs to be set.

    Returns:
        None
    """
    filename = video_instance.thumbnail.name
    print(f"Thumbnail Dateiname: {filename}")

    category = extract_category_from_filename(filename)
    
    if category:
        video_instance.category = category
        video_instance.save()
        print(f"Kategorie \"{category}\" für Video ID {video_instance.id} gespeichert.")
    else:
        print(f"Keine gültige Kategorie im Thumbnail für Video ID {video_instance.id} gefunden.")