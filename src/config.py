# config.py
import os

# Configuratie voor scriptopslag
LOCAL_REPOSITORY = os.getenv("SCRIPT_REPOSITORY", r"C:\Users\rafae\source\repos\Mainframe\repository")

def validate_config():
    """Controleert of de configuratie geldig is."""
    try:
        # Normaliseer het pad
        normalized_path = os.path.normpath(LOCAL_REPOSITORY)

        # Controleer of de directory bestaat en beschrijfbaar is
        if not os.path.exists(normalized_path):
            raise ValueError(f"De lokale repository '{normalized_path}' bestaat niet.")
        elif not os.access(normalized_path, os.W_OK):
            raise PermissionError(f"Je hebt geen schrijftoegang tot de repository '{normalized_path}'.")
    except OSError as e:
        raise ValueError(f"Er is een fout opgetreden bij het controleren van de repository: {e}")