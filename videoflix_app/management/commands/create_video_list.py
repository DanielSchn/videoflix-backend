# yourapp/management/commands/upload_videos.py
import os
from django.core.management.base import BaseCommand
from videoflix_app.models import Video
from django.core.files import File
from django.db import transaction

# Die vordefinierten Titel und Beschreibungen der Videos, basierend auf den Dateinamen
VIDEO_METADATA = {
    "boxing_sports.mp4": {
        "title": "The Fight for Glory",
        "description": "A thrilling journey into the world of boxing, showcasing intense matches, legendary fighters, and the perseverance needed to reach the top of the sport.",
        "thumbnail": "boxing_sports.jpg"
    },
    "howto_sports.mp4": {
        "title": "How to Master Sports",
        "description": "A comprehensive guide to excelling in various sports, offering expert tips and techniques for athletes of all skill levels.",
        "thumbnail": "howto_sports.jpg"
    },
    "racing_sports.mp4": {
        "title": "Race to Victory",
        "description": "Dive into the fast-paced world of racing, exploring the excitement, skill, and adrenaline that go into becoming a champion on the track.",
        "thumbnail": "racing_sports.jpg"
    },
    "breakout_crime.mp4": {
        "title": "Breaking the Law",
        "description": "A gripping documentary examining high-profile crime cases, exploring the causes, consequences, and criminal investigations that captivate the world.",
        "thumbnail": "breakout_crime.jpg"
    },
    "majesticwhales_documentary.mp4": {
        "title": "Giants of the Ocean",
        "description": "A mesmerizing exploration of the lives of whales, uncovering the beauty and mystery of these magnificent ocean giants.",
        "thumbnail": "majesticwhales_documentary.jpg"
    },
    "soccer_sports.mp4": {
        "title": "Soccer Legends",
        "description": "An inspiring look at the passion, strategy, and history behind soccer, highlighting the iconic players and moments that have defined the sport.",
        "thumbnail": "soccer_sports.jpg"
    },
    "castle_documentary.mp4": {
        "title": "Castles Through Time",
        "description": "Journey through history as you explore the majestic castles that have stood the test of time, unraveling their rich stories and architectural wonders.",
        "thumbnail": "castle_documentary.jpg"
    },
    "manga_documentary.mp4": {
        "title": "The Art of Manga",
        "description": "A captivating dive into the world of manga, exploring its origins, impact on pop culture, and the artistic journey behind this beloved medium.",
        "thumbnail": "manga_documentary.jpg"
    },
    "bodybuilding_sports.mp4": {
        "title": "The Power of Sports",
        "description": "A celebration of the global power of sports, showing how they bring people together and inspire millions across the world.",
        "thumbnail": "bodybuilding_sports.jpg"
    },
    "dancing_sports.mp4": {
        "title": "Dancing Through Life",
        "description": "A vibrant exploration of dance in the world of sports, blending movement, rhythm, and athleticism to create breathtaking performances.",
        "thumbnail": "dancing_sports.jpg"
    },
    "paralympic_sports.mp4": {
        "title": "The Spirit of Champions",
        "description": "A moving documentary focusing on the inspiring athletes of the Paralympic Games, showcasing their strength, determination, and triumphs.",
        "thumbnail": "paralympic_sports.jpg"
    },
    "friendship_romance.mp4": {
        "title": "Friendship",
        "description": "A heartwarming tale of friendship blossoming into romance, as two souls discover the beauty of love and connection.",
        "thumbnail": "friendship_romance.jpg"
    },
    "police_crime.mp4": {
        "title": "Police on the Beat",
        "description": "A thrilling documentary following police officers as they investigate crime, solve cases, and ensure justice is served in urban environments.",
        "thumbnail": "police_crime.jpg"
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