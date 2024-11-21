import subprocess
import shlex
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


def convert_480p(source):
    # Verwende Pathlib für den Dateipfad
    source_path = Path(source)
    target_path = source_path.with_name(source_path.stem + '_480p.mp4')

    # FFmpeg-Kommando als Liste
    cmd = [
        'ffmpeg', 
        '-i', str(source_path),
        '-s', 'hd480',
        '-c:v', 'libx264', 
        '-crf', '23',
        '-c:a', 'aac', 
        '-strict', '-2', 
        str(target_path)
    ]

    try:
        # Starte den FFmpeg-Prozess
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Lese stdout und stderr in Echtzeit
        for line in process.stdout:
            print(line.strip())  # Fortschritt oder normale Ausgabe

        for line in process.stderr:
            print(line.strip(), file=sys.stderr)  # Fehlerausgabe

        # Warten, bis der Prozess abgeschlossen ist
        process.wait()

        # Überprüfen, ob der FFmpeg-Prozess erfolgreich war
        if process.returncode != 0:
            print(f"Fehler bei der Konvertierung (Rückgabewert: {process.returncode})", file=sys.stderr)
            return False
        else:
            print(f"Konvertierung erfolgreich abgeschlossen: {target_path}")
            return True

    except Exception as e:
        print(f"Fehler beim Starten von FFmpeg: {e}", file=sys.stderr)
        return False



def check_ffmpeg():
    process = subprocess.Popen(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()
    if process.returncode == 0:
        print(f"FFmpeg Version: {stdout}")
    else:
        print(f"FFmpeg Fehler: {stderr}", file=sys.stderr)

def simple_task(path):
    print(f"Processing: {path}")