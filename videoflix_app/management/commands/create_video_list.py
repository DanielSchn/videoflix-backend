# yourapp/management/commands/upload_videos.py
import os
from django.core.management.base import BaseCommand
from videoflix_app.models import Video
from django.core.files import File
from django.db import transaction

# Die vordefinierten Titel und Beschreibungen der Videos, basierend auf den Dateinamen
VIDEO_METADATA = {
    "howto_sports.mp4": {
        "title": "How to Master Sports",
        "description": "A comprehensive guide to excelling in various sports, offering expert tips and techniques for athletes of all skill levels.",
        "thumbnail": "howto_sports.png"
    },
    "breakout_crime.mp4": {
        "title": "Breaking the Law",
        "description": "A gripping documentary examining high-profile crime cases, exploring the causes, consequences, and criminal investigations that captivate the world.",
        "thumbnail": "breakout_crime.png"
    },
    "majesticwhales_documentary.mp4": {
        "title": "Giants of the Ocean",
        "description": "A mesmerizing exploration of the lives of whales, uncovering the beauty and mystery of these magnificent ocean giants.",
        "thumbnail": "majesticwhales_documentary.png"
    },
    "castle_documentary.mp4": {
        "title": "Castles Through Time",
        "description": "Journey through history as you explore the majestic castles that have stood the test of time, unraveling their rich stories and architectural wonders.",
        "thumbnail": "castle_documentary.png"
    },
    "manga_documentary.mp4": {
        "title": "The Art of Manga",
        "description": "A captivating dive into the world of manga, exploring its origins, impact on pop culture, and the artistic journey behind this beloved medium.",
        "thumbnail": "manga_documentary.png"
    },
    "dancing_sports.mp4": {
        "title": "Dancing Through Life",
        "description": "A vibrant exploration of dance in the world of sports, blending movement, rhythm, and athleticism to create breathtaking performances.",
        "thumbnail": "dancing_sports.png"
    },
    "hateyou_crime.mp4": {
        "title": "Hate You?",
        "description": "A powerful emotional journey that delves into the complexities of human relationships, exploring feelings of anger, betrayal, and the struggle to overcome deep-seated hatred.",
        "thumbnail": "hateyou_crime.png"
    },
    "friendship_romance.mp4": {
        "title": "Friendship",
        "description": "A heartwarming tale of friendship blossoming into romance, as two souls discover the beauty of love and connection.",
        "thumbnail": "friendship_romance.png"
    },
    "police_crime.mp4": {
        "title": "Police on the Beat",
        "description": "A thrilling documentary following police officers as they investigate crime, solve cases, and ensure justice is served in urban environments.",
        "thumbnail": "police_crime.png"
    },
    "babys_documentary.mp4": {
        "title": "Baby's Secret Language",
        "description": "An insightful exploration into the mysterious world of babies' communication, uncovering the subtle cues and gestures that reveal their thoughts and emotions.",
        "thumbnail": "babys_documentary.png"
}
}

class Command(BaseCommand):
    help = 'Uploads videos from a specified folder into the Video model'

    def handle(self, *args, **kwargs):
        video_folder = os.environ.get('VIDEO_FOLDER')
        video_files = [f for f in os.listdir(video_folder) if os.path.isfile(os.path.join(video_folder, f))]

        for video_file in video_files:
            video_file_lower = video_file.lower()

            if video_file.lower() in [key.lower() for key in VIDEO_METADATA]:
                metadata = VIDEO_METADATA[video_file_lower]
                video_title = metadata['title']
                video_description = metadata['description']
                video_thumbnail_name = metadata['thumbnail']
                
                video_path = os.path.join(video_folder, video_file)
                thumbnail_path = os.path.join(video_folder, video_thumbnail_name)

                if os.path.exists(video_path) and os.path.exists(thumbnail_path):
                    try:

                        with open(video_path, 'rb') as video_file_obj, open(thumbnail_path, 'rb') as thumbnail_file_obj:
                            video = Video(
                                title=video_title,
                                description=video_description,
                                original_file=File(video_file_obj, name=video_file)
                            )

                            video.thumbnail = File(thumbnail_file_obj, name=video_thumbnail_name)
                            video.save()

                        self.stdout.write(self.style.SUCCESS(f'Successfully uploaded video: {video_title} with thumbnail.'))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Error uploading video {video_title}: {e}'))
                else:
                    self.stdout.write(self.style.WARNING(f"File or Thumbnail not found for {video_file}. Video Path: {video_path}, Thumbnail Path: {thumbnail_path}"))