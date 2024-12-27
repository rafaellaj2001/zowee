import subprocess
import os
from config import LOCAL_REPOSITORY
import shutil

def upload_script(file_path, dataset_name):
    """
    Upload een script naar de mainframe met behulp van Zowe CLI.
    """
    try:
        # Debug: toon het oorspronkelijke bestandspad
        print(f"DEBUG: Opgegeven bestandspad: {file_path}")

        # Normaliseer het bestandspad
        file_path = os.path.normpath(file_path)
        print(f"DEBUG: Genormaliseerd bestandspad: {file_path}")

        # Controleer of het bestand bestaat
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"Het bestand '{file_path}' bestaat niet.")

        # Het pad waar de repository zich bevindt
        script_dir = os.path.dirname(os.path.abspath(__file__))
        script_dir = os.path.normpath(script_dir)
        print(f"DEBUG: Pad naar script_dir: {script_dir}")

        mainframe_path = os.path.join(script_dir, 'repository')
        mainframe_path = os.path.normpath(mainframe_path)
        print(f"DEBUG: Pad naar repository: {mainframe_path}")

        # Controleer of de repository-map bestaat
        if not os.path.exists(mainframe_path):
            raise FileNotFoundError(f"De repository-map '{mainframe_path}' bestaat niet.")

        # Pad naar Zowe CLI expliciet instellen als het niet in PATH zit
        zowe_cli_path = r'C:\Users\rafae\AppData\Roaming\npm\zowe.ps1'  # Pas dit aan naar jouw Zowe installatiepad

        # Bouw de Zowe CLI-opdracht
        zowe_command = [
            'powershell',  # Gebruik powershell om de zowe.ps1 uit te voeren
            zowe_cli_path,  # Pad naar Zowe CLI
            'files', 'upload', 'file-to-data-set',
            file_path,
            dataset_name
        ]

        # Debug: toon de Zowe CLI-opdracht
        print(f"DEBUG: Zowe CLI-opdracht: {' '.join(zowe_command)}")

        # Voer de Zowe CLI-opdracht uit
        result = subprocess.run(
            zowe_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Debug: toon de uitvoer van de Zowe CLI
        print(f"DEBUG: Zowe CLI stdout: {result.stdout}")
        print(f"DEBUG: Zowe CLI stderr: {result.stderr}")

        # Controleer de uitkomst van de opdracht
        if result.returncode == 0:
            return True, "Upload succesvol!"
        else:
            return False, f"Fout bij uploaden: {result.stderr}"

    except Exception as e:
        # Toon de fout in een debugbericht
        print(f"DEBUG: Er is een uitzondering opgetreden: {e}")
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
