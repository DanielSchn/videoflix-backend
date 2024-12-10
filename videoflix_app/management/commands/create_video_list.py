# yourapp/management/commands/upload_videos.py
import os
from django.core.management.base import BaseCommand
from videoflix_app.models import Video
from django.core.files import File
from django.db import transaction

# Die vordefinierten Titel und Beschreibungen der Videos, basierend auf den Dateinamen
VIDEO_METADATA = {
    "boxing_sports.mp4": {
        "title": "Boxing: The Fight for Glory",
        "description": "A thrilling journey into the world of boxing, showcasing intense matches, legendary fighters, and the perseverance needed to reach the top of the sport."
    },
    "howto_sports.mp4": {
        "title": "How to Master Sports",
        "description": "A comprehensive guide to excelling in various sports, offering expert tips and techniques for athletes of all skill levels."
    },
    "racing_sports.mp4": {
        "title": "Race to Victory: The Thrill of Racing",
        "description": "Dive into the fast-paced world of racing, exploring the excitement, skill, and adrenaline that go into becoming a champion on the track."
    },
    "breakout_crime.mp4": {
        "title": "Breaking the Law: Crime in Focus",
        "description": "A gripping documentary examining high-profile crime cases, exploring the causes, consequences, and criminal investigations that captivate the world."
    },
    "majesticwhales_documentary.mp4": {
        "title": "Majestic Whales: Giants of the Ocean",
        "description": "A mesmerizing exploration of the lives of whales, uncovering the beauty and mystery of these magnificent ocean giants."
    },
    "soccer_sports.mp4": {
        "title": "Soccer Legends: The Beautiful Game",
        "description": "An inspiring look at the passion, strategy, and history behind soccer, highlighting the iconic players and moments that have defined the sport."
    },
    "castle_documentary.mp4": {
        "title": "Castles Through Time: Stories of Strength",
        "description": "Journey through history as you explore the majestic castles that have stood the test of time, unraveling their rich stories and architectural wonders."
    },
    "manga_documentary.mp4": {
        "title": "The Art of Manga: A Cultural Phenomenon",
        "description": "A captivating dive into the world of manga, exploring its origins, impact on pop culture, and the artistic journey behind this beloved medium."
    },
    "sports_sports.mp4": {
        "title": "The Power of Sports: Uniting the World",
        "description": "A celebration of the global power of sports, showing how they bring people together and inspire millions across the world."
    },
    "dancing_sports.mp4": {
        "title": "Dancing Through Life: The Rhythm of Sports",
        "description": "A vibrant exploration of dance in the world of sports, blending movement, rhythm, and athleticism to create breathtaking performances."
    },
    "paralympic_documentary.mp4": {
        "title": "Paralympics: The Spirit of Champions",
        "description": "A moving documentary focusing on the inspiring athletes of the Paralympic Games, showcasing their strength, determination, and triumphs."
    },
    "friendship_romance.mp4": {
        "title": "Friendship & Romance: A Love Story",
        "description": "A heartwarming tale of friendship blossoming into romance, as two souls discover the beauty of love and connection."
    },
    "police_crime.mp4": {
        "title": "Police on the Beat: Investigating Crime",
        "description": "A thrilling documentary following police officers as they investigate crime, solve cases, and ensure justice is served in urban environments."
    }
}

class Command(BaseCommand):
    help = 'Uploads videos from a specified folder into the Video model'

    def handle(self, *args, **kwargs):
        video_folder = '/home/daniel/projects/videoflix-videos'
        video_files = [f for f in os.listdir(video_folder) if os.path.isfile(os.path.join(video_folder, f))]

        # Iteriere über die Video-Dateien und ordne sie den Metadaten zu
        for video_file in video_files:
            if video_file in VIDEO_METADATA:
                metadata = VIDEO_METADATA[video_file]
                video_title = metadata['title']
                video_description = metadata['description']
                video_path = os.path.join(video_folder, video_file)

                # Überprüfen, ob der Dateiname mit der MP4-Erweiterung endet
                if video_file.lower().endswith('.mp4'):
                    # Jetzt laden wir die Datei zusammen mit den Metadaten hoch und speichern sie
                    with transaction.atomic():
                        # Öffnen der Datei und Zuweisen zu `original_file`
                        with open(video_path, 'rb') as video_file_obj:
                            video = Video(
                                title=video_title,
                                description=video_description,
                                original_file=File(video_file_obj, name=video_file)  # Der Name der Datei wird als 'name' gesetzt
                            )
                            video.save()

                        # Erfolgreiches Hochladen
                        self.stdout.write(self.style.SUCCESS(f'Successfully uploaded video: {video_title}'))

                else:
                    self.stdout.write(self.style.WARNING(f'Skipping non-mp4 file: {video_file}'))
            else:
                self.stdout.write(self.style.WARNING(f'No metadata found for file: {video_file}'))
