import subprocess
import os
import sys
from pathlib import Path


def test_worker_permissions():
    test_file = '/home/daniel/projects/videoflix-backend/media/videos/test_file.txt'
    try:
        with open(test_file, 'w') as f:
            f.write('Test')
        os.remove(test_file)
        print("Worker hat Schreibrechte.")
    except Exception as e:
        print(f"Fehler: {e}")


def convert_480p(source):
    if not os.path.isfile(source):
        print("Die Eingabedatei existiert nicht.")

    file, _ = os.path.splitext(source)
    target = file + f'_480p.mp4'
    
    cmd = f'ffmpeg -i "{source}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{target}"'
    #cmd = f'ffmpeg -i "/home/daniel/projects/videoflix-backend/output.mp4" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{target}"'

    #Reine Testdatei die NUR erstellt wird!
    #cmd = 'ffmpeg -f lavfi -i testsrc=duration=5:size=1280x720:rate=30 -y test.mp4'
    try:
        process = subprocess.run(cmd, capture_output=False, shell=True, check=True)
        process.check_returncode()
    except Exception as e:
          print(f"Fehler beim Ausführen des FFmpeg-Befehls: {str(e)}")
          return None



def check_ffmpeg():
    process = subprocess.Popen(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()
    if process.returncode == 0:
        print(f"FFmpeg Version: {stdout}")
    else:
        print(f"FFmpeg Fehler: {stderr}", file=sys.stderr)


def simple_task(path):
    print(f"Processing: {path}")



# Funktion an sich läuft. Ist für später gedacht dann mit video.js
def convert_with_hls(source):
    if not os.path.isfile(source):
        print("Die Eingabedatei existiert nicht.")

    file, _ = os.path.splitext(source)
    target = file + f'_{'480p'}.m3u8'
    cmd = f'ffmpeg -i "{source}" -codec: copy -start_number 0 -hls_time 10 -hls_list_size 0 -f hls "{target}"'

    try:
        process = subprocess.run(cmd, check=True, shell=True)
        process.check_returncode()
    except Exception as e:
         print(f"Fehler beim Ausführen des FFmpeg-Befehls: {str(e)}")
         return None