import subprocess
import os
import sys
from pathlib import Path


# def convert_480p(source):
#    base_name = os.path.splitext(source)[0]
#    target = f"{base_name}_480p.mp4"
#    cmd = f'ffmpeg -i "{shlex.quote(source)}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{shlex.quote(target)}"'

#    try:
#        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
#        if result.returncode != 0:
#            print(f"Fehler bei der Konvertierung: {result.stderr}")
#            return None
#        print(f"Konvertierung erfolgreich: {target}")
#        return target
#    except FileNotFoundError:
#        print("FFmpeg ist nicht installiert oder nicht im PATH verfügbar.")
#        return None
#    except Exception as e:
#        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")
#        return None

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
    os.environ["PATH"] += ":/usr/bin"
    if not os.path.isfile(source):
        print("Die Eingabedatei existiert nicht.")
    source_path = Path(source)
    target_path = source_path.with_name(source_path.stem + '_480p.mp4')
    #cmd = 'ffmpeg -i "{}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source_path, target_path)
    # cmd = 'ffmpeg -y -i /home/daniel/projects/videoflix-backend/media/videos/test_video.mp4'
    cmd = 'ffmpeg -f lavfi -i testsrc=duration=5:size=1280x720:rate=30 test.mp4'
    try:
        process = subprocess.run(cmd, check=True, shell=True)
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