# Generated by Django 5.1.3 on 2024-12-18 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videoflix_app', '0009_remove_video_ts_segments_1080p_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='thumbnail',
            field=models.FileField(blank=True, help_text='Bitte Datei im Format beliebigerName_erlaubteKategorie.jpg oder .png! Erlaubte Kategorien: sports, documentary, romance, crime', null=True, upload_to='img/'),
        ),
    ]
