import subprocess
import os
from django.core.files import File
from .models import Video


RESOLUTIONS = {
    "480p": {"size": "hd480", "field": "video_480p"},
    "720p": {"size": "hd720", "field": "video_720p"},
    "1080p": {"size": "hd1080", "field": "video_1080p"},
}
    

def convert_video(source, video_instance):
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
    

ALLOWED_CATEGORIES = os.environ.get('ALLOWED_CATEGORIES').split(',')

def set_video_category_for_all():
    videos = Video.objects.all()
    for video in videos:
        set_video_category(video)

def extract_category_from_filename(filename):
    for category in ALLOWED_CATEGORIES:
        if category in filename.lower():
            return category
    return None

def set_video_category(video_instance):
    filename = video_instance.thumbnail.name
    print(f"Thumbnail Dateiname: {filename}")

    category = extract_category_from_filename(filename)
    
    if category:
        video_instance.category = category
        video_instance.save()
        print(f"Kategorie \"{category}\" für Video ID {video_instance.id} gespeichert.")
    else:
        print(f"Keine gültige Kategorie im Thumbnail für Video ID {video_instance.id} gefunden.")