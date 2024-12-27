import subprocess
import os
import logging

# Configureer logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Functie om Zowe CLI commando uit te voeren
def run_zowe_command(command):
    """Voer een Zowe CLI-commando uit via subprocess."""
    try:
        logging.info(f"Voer Zowe CLI-commando uit: {command}")
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        logging.info(f"Resultaat: {result.stdout}")
        return result.stdout
    except subprocess.CalledProcessError as e:
        logging.error(f"Error tijdens het uitvoeren van Zowe CLI-commando: {e}")
        logging.error(f"Standaardfout: {e.stderr}")
        return None

# Functie om een bestand naar de mainframe te uploaden
def upload_file(local_file, remote_file):
    """Upload een bestand naar de mainframe via Zowe CLI."""
    logging.info(f"Upload bestand: {local_file} naar dataset: {remote_file}")
    command = f"zowe zos-files upload file-to-data-set \"{local_file}\" \"{remote_file}\""
    return run_zowe_command(command)

# Functie om een bestand van de mainframe te downloaden
def download_file(remote_file, local_file):
    """Download een bestand van de mainframe via Zowe CLI."""
    logging.info(f"Download bestand: {remote_file} naar lokaal bestand: {local_file}")
    command = f"zowe zos-files download \"{remote_file}\" \"{local_file}\""
    return run_zowe_command(command)

# Functie om omgevingsvariabelen in te stellen voor Zowe CLI
def set_zowe_environment_variables(host, port, user, password):
    """Stel de omgevingsvariabelen in voor Zowe CLI."""
    logging.info(f"Instellen van omgevingsvariabelen voor Zowe CLI naar host {host} en poort {port}")
    os.environ["ZOWE_ZOSMF_HOST"] = host
    os.environ["ZOWE_ZOSMF_PORT"] = str(port)
    os.environ["ZOWE_ZOSMF_USER"] = user
    os.environ["ZOWE_ZOSMF_PASSWORD"] = password

# Hoofdlogica van het script
def main():
    # Stel je Zowe-server instellingen in
    host = "192.168.1.26"  # Vervang door je z/OSMF-server IP
    port = 8081            # Vervang door je poortnummer
    user = "rafa"          # Vervang door je z/OSMF gebruikersnaam
    password = "jouw-wachtwoord"  # Vervang door je z/OSMF wachtwoord

    set_zowe_environment_variables(host, port, user, password)

    # Kies of je wilt uploaden of downloaden
    action = input("Wil je een bestand uploaden (u) of downloaden (d)? ").strip().lower()

    if action == "u":
        # Bestanden uploaden
        local_file = input("Voer het pad in naar het bestand dat je wilt uploaden: ").strip()
        remote_file = input("Voer de naam in van de remote dataset op de mainframe: ").strip()

        if os.path.exists(local_file):
            logging.info(f"Bestand bestaat: {local_file}")
            upload_file(local_file, remote_file)
        else:
            logging.error(f"Het opgegeven lokale bestand bestaat niet: {local_file}")
    
    elif action == "d":
        # Bestanden downloaden
        remote_file = input("Voer de naam in van de remote dataset op de mainframe: ").strip()
        local_file = input("Voer het pad in naar waar je het bestand wilt opslaan: ").strip()

        download_file(remote_file, local_file)
    
    else:
        logging.error("Ongeldige keuze. Voer 'u' in om te uploaden of 'd' om te downloaden.")

if __name__ == "__main__":
    main()
