# -*- coding: utf-8 -*-
import os

def validate_script(file_path):
    """
    Valideer het script op basis van de volgende regels:
    - Afwijzen als het bestand een afbeelding, video of Office-document is.
    - Andere bestandstypes worden toegestaan.
    - Bestand mag niet leeg zijn.
    """
    # Lijst van verboden extensies (media en niet-programmeerbare bestanden)
    invalid_extensions = [
        '.jpg', '.jpeg', '.png', '.gif', '.bmp',  # Afbeeldingen
        '.mp4', '.avi', '.mov', '.wmv', '.mkv',   # Video's
        '.docx', '.doc', '.pptx', '.ppt', '.xls', '.xlsx',  # Office-documenten
        '.pdf',  # PDF-documenten
        '.zip', '.rar', '.7z', '.tar', '.gz',  # Archiefbestanden
        '.txt'  # Tekstbestanden
    ]

    try:
        # Controleer of het bestand bestaat
        if not os.path.isfile(file_path):
            return False, "Bestand bestaat niet."

        # Controleer de extensie
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        if ext in invalid_extensions:
            return False, f"Ongeldig bestandstype: {ext.upper()}."

        # Controleer of het bestand niet leeg is
        if os.path.getsize(file_path) == 0:
            return False, "Het bestand is leeg."

        # Als alle controles slagen, is het bestand geldig
        return True, "Validatie succesvol."
    except Exception as e:
        return False, f"Validatie fout: {e}"
