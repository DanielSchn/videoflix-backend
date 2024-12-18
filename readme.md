##### English version below

# Backend für das Videoflix Project

Videoflix ist eine Video on demand Plattform für Endnutzer.\
Das Frontend ist hier zu finden:
`https://github.com/DanielSchn/videoflix-frontend`\

## Funktionen
- Registrierung incl. Emailvalidierung und Login.
- Passwort vergessen und anschliessendes neu setzen.
- Übersicht einer Liste aller Videos.
- Streamen von Videos in verschiedenen Auflösungen.

## Voraussetzungen
- Python (Version 3.x)
- Django (Version und zusätzliche Pakete siehe requirements.txt)

Alles benötigte kann über die requirements.txt installiert werden. (Siehe Punkt 3)

## Installation auf einem Linux System
### 1. Projekt klonen
```
cd In_den_Projektordner
git clone git@github.com:DanielSchn/videoflix-backend.git
cd videoflix-backend
```
### 2. Virtual Environment erstellen
Virtuelles Python-Umfeld erstellen und aktivieren
```
python -m venv env
source env/bin/activate # Linux/Mac
```
### 3. Abhängigkeiten installieren
```
pip install -r requirements.txt
```
### 4. Django-Projekt initialisieren
Datenbank migrieren und Server starten
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
Projekt läuft, je nach Konfiguration, unter `http://127.0.0.1:8000`.
### 5. Superuser (Admin) erstellen
Superuser kann direkt über das Terminal mit folgendem Befehl erstellt werden:
```
python manage.py createsuperuser
```
### 6. Videoupload über Management Befehl oder API View
```
python manage.py create_video_list
```
Dafür muss aber zwingend die Liste angepasst werden mit Dateinamen usw. oder auf Anfrage können die video bereitgestellt werden. Den Ordner auf dem System muss man in der .env unter VIDEO_FOLDER angeben.

In der API View:
```
http://127.0.0.1:8000/api/video/
```
können auch Videos hochgeladen werden.
Dort muss der Dateiname vom Thumbnail so aussehen:
```
BELIEBIGER-NAME_ERLAUBTE-KATEGORIE.jpg oder .png
=> erlaubte Kategorien sind in der .env unter ALLOWED_CATEGORIES angegeben.
```
Diese Kategorie im Dateinamen bestimmt die Videokategorie, welche während dem Upload ausgelesen wird.

## Konfiguration
In der Datei `settings.py` wurden einige wichtige Einstellungen vorgenommen, um das Projekt lokal auszuführen:
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'videoflix_app',
    'debug_toolbar',
    'django_rq',
    'import_export',
    'users',
]
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}
```
Diese Einstellungen ermöglichen 'Permissions' und die 'Authentication'.

## Nutzung
Nachdem der Server läuft, kannst du die API verwenden, um mit dem Videoflix Frontend zu arbeiten. Hier einige nützliche Befehle:

- Migriere die Datenbank:
```
python manage.py makemigrations
python manage.py migrate
```
- Starte den Entwicklungsserver:
```
python manage.py runserver
```

## Deployment
Für dieses Projekt gibt es derzeit keine spezifischen Deployment-Anweisungen.

## Lizenz
Dieses Projekt wurde als Teil eines Lernprojekts erstellt und steht ohne spezifische Lizenz zur Verfügung.

# English version

# Backend for the Videoflix Project

Videoflix is a video-on-demand platform for end users. \
The frontend can be found here:
`https://github.com/DanielSchn/videoflix-frontend`\

## Features
- Registration with email validation and login.
- Password reset functionality.
- Overview of a list of all videos.
- Streaming videos in various resolutions.

## Prerequisites
- Python (version 3.x)
- Django (version and additional packages listed in requirements.txt)

All required dependencies can be installed via requirements.txt (see step 3).

## Installation on a Linux system
### 1. Clone the project
```
cd to_your_project_directory
git clone git@github.com:DanielSchn/videoflix-backend.git
cd videoflix-backend
```
### 2. Create a virtual environment
Create and activate a virtual Python environment:
```
python -m venv env
source env/bin/activate # Linux/Mac
```
### 3. Install dependencies
```
pip install -r requirements.txt
```
### 4. Initialize the Django project
Migrate the database and start the server:
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
The project will run, depending on your configuration, at `http://127.0.0.1:8000`.
### 5. Create a superuser (admin)
You can create a superuser directly via the terminal with the following command:
```
python manage.py createsuperuser
```
### 6. Video upload via management command or API view
```
python manage.py create_video_list
```
Before using this command, you must adjust the video list with the appropriate filenames. Alternatively, the videos can be provided upon request. The folder containing the videos must be specified in the .env file under VIDEO_FOLDER.

Using the API view:
```
http://127.0.0.1:8000/api/video/
```
Videos can also be uploaded here. \
The thumbnail filenames must follow this format:
```
ANY-NAME_ALLOWED-CATEGORY.jpg or .png
=> Allowed categories are listed in the `.env` file under `ALLOWED_CATEGORIES`.
```
The category in the filename determines the video category, which is extracted during the upload process.

## Konfiguration
In the settings.py file, several important settings have been configured to run the project locally:
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'videoflix_app',
    'debug_toolbar',
    'django_rq',
    'import_export',
    'users',
]
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}
```
These settings enable permissions and authentication.

## Usage
Once the server is running, you can use the API to interact with the Videoflix frontend. Here are some useful commands:

- Migrate the database:
```
python manage.py makemigrations
python manage.py migrate
```
- Start the development server:
```
python manage.py runserver
```

## Deployment
There are currently no specific deployment instructions for this project.

## License
This project was created as part of a learning project and is provided without a specific license.