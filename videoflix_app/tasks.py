import subprocess
import shlex
import os

def convert_480p(source):
    base_name = os.path.splitext(source)[0]
    target = f"{base_name}_480p.mp4"
    cmd = f'ffmpeg -i "{shlex.quote(source)}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{shlex.quote(target)}"'
    #run = subprocess.run(cmd, capture_output=True)

    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Fehler bei der Konvertierung: {result.stderr}")
            return None
        print(f"Konvertierung erfolgreich: {target}")
        return target
    except FileNotFoundError:
        print("FFmpeg ist nicht installiert oder nicht im PATH verfügbar.")
        return None
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")
        return None