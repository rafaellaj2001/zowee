import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import subprocess
import os
import logging
from validation import validate_script

# Configureer logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Functie om Zowe CLI commando uit te voeren
def run_zowe_command(command):
    """Voer een Zowe CLI-commando uit via subprocess."""
    try:
        logging.info(f"Voer Zowe CLI-commando uit: {command}")
        # Zorg ervoor dat subprocess met 'utf-8' encoding werkt
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True, encoding='utf-8')
        logging.info(f"Resultaat: {result.stdout}")
        return result.stdout
    except subprocess.CalledProcessError as e:
        logging.error(f"Error tijdens het uitvoeren van Zowe CLI-commando: {e}")
        logging.error(f"Standaardfout: {e.stderr}")
        return None

# Functie om omgevingsvariabelen in te stellen voor Zowe CLI
def set_zowe_environment_variables(host, port, user, password):
    """Stel de omgevingsvariabelen in voor Zowe CLI."""
    logging.info(f"Instellen van Zowe CLI omgevingsvariabelen: {host}, {port}, {user}")
    os.environ["ZOWE_ZOSMF_HOST"] = host
    os.environ["ZOWE_ZOSMF_PORT"] = str(port)
    os.environ["ZOWE_ZOSMF_USER"] = user
    os.environ["ZOWE_ZOSMF_PASSWORD"] = password
    os.environ["ZOWE_CLI_CONFIG_DIR"] = os.path.expanduser("~/.zowe")

# Functie om scripts op te halen van de mainframe
def get_scripts_list():
    """Verkrijg een lijst van beschikbare scripts op de mainframe via Zowe CLI."""
    command = "zowe zos-files data-set list"
    result = run_zowe_command(command)
    
    if result:
        # Parseer de lijst van datasets
        scripts = []
        for line in result.splitlines():
            # Je kunt de logica aanpassen om de datasetnaam te extraheren
            if "DSN=" in line:
                scripts.append(line.split("DSN=")[-1].strip())
        return scripts
    return []

# Functie om een script te downloaden
def download_file():
    # Verkrijg een lijst van scripts van de mainframe
    scripts = get_scripts_list()
    
    if scripts:
        # Maak een nieuw venster voor de lijst van scripts
        download_window = tk.Toplevel(root)
        download_window.title("Kies Script om te Downloaden")
        download_window.geometry("400x300")
        
        # Voeg een lijstbox toe
        listbox = tk.Listbox(download_window, height=10, width=50)
        for script in scripts:
            listbox.insert(tk.END, script)
        
        listbox.pack(pady=20)
        
        def on_select_script():
            # Verkrijg het geselecteerde script
            selected_script = listbox.get(tk.ACTIVE)
            if selected_script:
                # Vraag de gebruiker om een locatie om het bestand op te slaan
                local_file = filedialog.asksaveasfilename(
                    title="Kies locatie om het bestand op te slaan", 
                    defaultextension=".txt", 
                    filetypes=[("Text bestanden", "*.txt")]
                )
                
                if local_file:
                    # Stel het Zowe-commando in om het bestand te downloaden
                    command = f"zowe zos-files download \"{selected_script}\" \"{local_file}\""
                    run_zowe_command(command)
                    messagebox.showinfo("Success", f"Script succesvol gedownload naar {local_file}")
                else:
                    messagebox.showerror("Fout", "Geen locatie geselecteerd.")
            download_window.destroy()
        
        # Voeg een knop toe om het geselecteerde script te downloaden
        select_button = tk.Button(download_window, text="Download Geselecteerd Script", command=on_select_script)
        select_button.pack(pady=10)
        
    else:
        messagebox.showerror("Fout", "Er zijn geen scripts gevonden op de mainframe.")

# Functie om bestand te uploaden naar de mainframe
def upload_file():
    local_file = filedialog.askopenfilename(title="Kies het bestand om te uploaden", filetypes=[("All Files", "*.*")])
    
    if local_file:
        # Voer validatie uit voor het te uploaden bestand
        valid, message = validate_script(local_file)
        if valid:
            remote_dataset = simpledialog.askstring("Remote Dataset", "Voer de naam in van de remote dataset op de mainframe waar je het bestand wilt uploaden:")
            
            if remote_dataset:
                # Upload het bestand naar de mainframe
                command = f"zowe zos-files upload file-to-data-set \"{local_file}\" \"{remote_dataset}\""
                result = run_zowe_command(command)
                
                if result:
                    messagebox.showinfo("Success", f"Bestand succesvol gepload naar {remote_dataset}")
                else:
                    messagebox.showerror("Fout", "Er is een fout opgetreden bij het uploaden van het bestand.")
            else:
                messagebox.showerror("Fout", "Ongeldige remote datasetnaam.")
        else:
            messagebox.showerror("Fout", message)  # Toon validatiefout
    else:
        messagebox.showerror("Fout", "Geen bestand geselecteerd voor upload.")

# Functie om Zowe CLI verbinding in te stellen
def configure_zowe():
    host = simpledialog.askstring("Host", "Voer het Zowe hostadres in:")
    port = simpledialog.askstring("Port", "Voer de Zowe poort in:")
    user = simpledialog.askstring("User", "Voer je gebruikersnaam in:")
    password = simpledialog.askstring("Password", "Voer je wachtwoord in:", show="*")
    
    if host and port and user and password:
        set_zowe_environment_variables(host, int(port), user, password)
        messagebox.showinfo("Instellingen", "Zowe CLI is succesvol geconfigureerd.")
    else:
        messagebox.showerror("Fout", "Alle velden moeten ingevuld zijn.")

# Hoofdvenster instellen
root = tk.Tk()
root.title("Zowe CLI Scriptbeheer")
root.geometry("500x350")  # De grootte van het venster
root.config(bg="#000000")  # Zwarte achtergrond

# Definieer kleuren
primary_color = "#006400"  # Donker groen
secondary_color = "#00FF00"  # Licht groen voor meldingen
background_color = "#000000"  # Zwart voor de achtergrond

# Styling van knoppen en invoervelden
button_style = {
    'width': 20,
    'height': 2,
    'bg': primary_color,
    'fg': "white",
    'font': ("Helvetica", 12),
    'relief': "flat",
    'bd': 0,
    'highlightthickness': 0
}

label_style = {
    'bg': background_color,
    'fg': primary_color,
    'font': ("Helvetica", 14, 'bold')
}

# Toevoegen van een titel bovenaan
title_label = tk.Label(root, text="Zowe CLI Scriptbeheer", **label_style)
title_label.grid(row=0, column=0, columnspan=3, pady=20)

# Knoppen toevoegen voor uploaden, downloaden en configureren van Zowe
configure_button = tk.Button(root, text="Configureer Zowe", command=configure_zowe, **button_style)
configure_button.grid(row=1, column=0, pady=10, padx=20, sticky="ew")

download_button = tk.Button(root, text="Download Script", command=download_file, **button_style)
download_button.grid(row=2, column=0, pady=10, padx=20, sticky="ew")

upload_button = tk.Button(root, text="Upload Bestand", command=upload_file, **button_style)
upload_button.grid(row=3, column=0, pady=10, padx=20, sticky="ew")

# Zorg voor een mooie ruimte tussen de knoppen en voorkom dat ze de randen raken
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)

# Start de GUI
root.mainloop()
