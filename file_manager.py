import subprocess
import os
from config import LOCAL_REPOSITORY
import shutil


def upload_script(file_path):
    """
    Upload het script naar de mainframe met behulp van Zowe CLI.
    """
    try:
        # Het pad waar het bestand ge�pload moet worden op de mainframe
        mainframe_path = "/path/to/mainframe/directory"  # Pas dit aan naar je eigen directory op de mainframe
        result = subprocess.run(
            ['zowe', 'files', 'upload', '--file', file_path, '--directory', mainframe_path],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        if result.returncode == 0:
            return True, "Upload succesvol!"
        else:
            return False, f"Fout bij uploaden: {result.stderr}"
    except Exception as e:
        return False, f"Er is een fout opgetreden: {e}"

def download_script(file_name):
    try:
        # Verkrijg het pad naar de Downloads-map
        user_profile = os.environ.get("USERPROFILE")
        downloads_folder = os.path.join(user_profile, "Downloads")
        
        # Het volledige pad naar het bestand in de Downloads-map
        destination_path = os.path.join(downloads_folder, os.path.basename(file_name))
        
        # Hier kopieer je het bestand naar de Downloads-map
        shutil.copy(file_name, destination_path)
        
        # Geef een succesbericht terug
        return True, f"Bestand is succesvol gedownload naar {destination_path}"
    except Exception as e:
        return False, f"Er is een fout opgetreden bij het downloaden: {e}"

def list_local_scripts():
    """
    Lijst de lokale scripts in de repository.
    """
    try:
        scripts = []
        for filename in os.listdir(LOCAL_REPOSITORY):
            if os.path.isfile(os.path.join(LOCAL_REPOSITORY, filename)):
                scripts.append(filename)
        return scripts
    except Exception as e:
        return f"Er is een fout opgetreden: {e}"
