# -*- coding: utf-8 -*-
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from validation import validate_script
from file_manager import upload_script, list_local_scripts, download_script
from config import LOCAL_REPOSITORY
import threading

def start_gui():
    # Hoofdvenster maken
    root = tk.Tk()
    root.title("Script Management Platform")
    root.geometry("800x600")
    root.configure(bg="#2E2E38")  # Achtergrondkleur van het venster

    # Voeg een achtergrondafbeelding toe
    bg_image_path = "background.jpg"  # Zet hier het pad naar je afbeelding
    if os.path.exists(bg_image_path):
        bg_image = tk.PhotoImage(file=bg_image_path)
        bg_label = tk.Label(root, image=bg_image)
        bg_label.place(relwidth=1, relheight=1)

    # Stijl instellen voor ttk-widgets
    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure(
        "TButton",
        font=("Arial", 12),
        foreground="#FFFFFF",
        background="#4CAF50",
        padding=10,
        focuscolor="none",
        borderwidth=0
    )
    style.map(
        "TButton",
        background=[("active", "#45A049")],
        foreground=[("active", "#FFFFFF")],
    )
    style.configure("TLabel", font=("Arial", 14), background="#2E2E38", foreground="#FFFFFF")
    
    # Welkomstlabel
    label = ttk.Label(root, text="Welkom bij het Script Management Platform!", font=("Arial", 16, "bold"))
    label.pack(pady=20)

    # Functie voor het uploaden van een script
    def upload():
        def upload_in_background():
            # Het bestand kiezen
            file_path = filedialog.askopenfilename(
                title="Kies een script om te uploaden",
                filetypes=[("Alle bestanden", "*.*")]
            )

            if file_path:
                # Debug: Controleer of het bestand bestaat
                if not os.path.isfile(file_path):
                    messagebox.showerror("Bestand Niet Gevonden", "Het geselecteerde bestand bestaat niet.")
                    return

                # Validatie van het script
                valid, message = validate_script(file_path)
                if valid:
                    # Controleer het pad voor uploaden (LOCAL_REPOSITORY)
                    if not os.path.exists(LOCAL_REPOSITORY):
                        messagebox.showerror("Fout", "De lokale opslagmap bestaat niet.")
                        return

                    try:
                        # Probeer het bestand te uploaden
                        success, upload_message = upload_script(file_path)
                        messagebox.showinfo("Upload Resultaat", upload_message)
                    except Exception as e:
                        messagebox.showerror("Upload Fout", f"Er is een fout opgetreden tijdens het uploaden: {e}")
                else:
                    messagebox.showerror("Validatie Mislukt", message)
            else:
                messagebox.showwarning("Geen Bestand Gekozen", "Je hebt geen bestand geselecteerd.")
                
        # Start de upload in een aparte thread
        threading.Thread(target=upload_in_background, daemon=True).start()


    # Functie om lokale scripts te tonen
    def show_local_scripts():
        from datetime import datetime

        scripts = list_local_scripts()

        if isinstance(scripts, str):  # Als er een fout of een speciaal bericht is
            scripts = []  # Zorg ervoor dat er geen fout optreedt bij een lege lijst

        # Maak een nieuw venster voor de tabel
        table_window = tk.Toplevel(root)
        table_window.title("Lokale Scripts")
        table_window.geometry("900x500")
        table_window.configure(bg="#2E2E38")

        # Label bovenaan
        label = ttk.Label(table_window, text="Beschikbare Lokale Scripts", anchor="center", background="#2E2E38", foreground="#FFFFFF", font=("Arial", 14))
        label.pack(pady=10)

        # Treeview (tabel) instellen
        columns = ("Naam Script", "Bestandstype", "Grootte (KB)", "Datum Toegevoegd", "Actie")
        tree = ttk.Treeview(table_window, columns=columns, show="headings", height=15)

        # Kolommen definiëren
        tree.heading("Naam Script", text="Naam Script")
        tree.heading("Bestandstype", text="Bestandstype")
        tree.heading("Grootte (KB)", text="Grootte (KB)")
        tree.heading("Datum Toegevoegd", text="Datum Toegevoegd")
        tree.heading("Actie", text="Actie")

        tree.column("Naam Script", width=300, anchor="w")
        tree.column("Bestandstype", width=100, anchor="center")
        tree.column("Grootte (KB)", width=100, anchor="center")
        tree.column("Datum Toegevoegd", width=150, anchor="center")
        tree.column("Actie", width=100, anchor="center")

        # Voeg scripts toe aan de tabel (of laat het leeg als er geen scripts zijn)
        if scripts:
            for script in scripts:
                file_path = os.path.join(LOCAL_REPOSITORY, script)
                if os.path.isfile(file_path):
                    size_kb = os.path.getsize(file_path) / 1024  # Grootte in KB
                    extension = os.path.splitext(script)[1]  # Bestandstype
                    date_added = os.path.getctime(file_path)  # Aanmaakdatum (UNIX-timestamp)
                    formatted_date = datetime.fromtimestamp(date_added).strftime("%Y-%m-%d %H:%M")

                    # Voeg de gegevens toe aan de tabel
                    tree.insert("", "end", values=(script, extension, f"{size_kb:.2f}", formatted_date, "Download"))

        # Voeg de tabel toe aan het venster
        tree.pack(pady=10, padx=20)

        # Voeg stijl toe aan de tabel
        style.configure("Treeview", font=("Arial", 12), rowheight=25, background="#3B3B45", foreground="#FFFFFF", fieldbackground="#3B3B45")
        style.configure("Treeview.Heading", font=("Arial", 14, "bold"), background="#4CAF50", foreground="#FFFFFF")
        style.map("Treeview", background=[("selected", "#45A049")], foreground=[("selected", "#FFFFFF")])

        # Label tonen als er geen scripts zijn
        if not scripts:
            empty_label = ttk.Label(table_window, text="Geen scripts gevonden.", background="#2E2E38", foreground="#FFFFFF", font=("Arial", 12))
            empty_label.pack(pady=10)

        # Download-knop activeren
        def on_tree_select(event):
            selected_item = tree.focus()
            if selected_item:
                values = tree.item(selected_item, "values")
                if values and values[-1] == "Download":
                    file_name = values[0]  # Naam van het geselecteerde script
                    file_path = os.path.join(LOCAL_REPOSITORY, file_name)
            
                    # Oproepen van de downloadfunctie om naar de Downloads-map te downloaden
                    success, message = download_script(file_path)
            
                    # Toon een bericht met het resultaat van de download
                    messagebox.showinfo("Download Resultaat", message)

        tree.bind("<Double-1>", on_tree_select)

    # Extra visuele elementen
    # Voeg een mooie, informatieve label toe
    info_label = ttk.Label(root, text="Upload en download scripts gemakkelijk voor je mainframe!", font=("Arial", 12, "italic"))
    info_label.pack(pady=30)

    # Voeg een rand of kader toe rond het hoofdvenster om het visueel aantrekkelijker te maken
    border_frame = tk.Frame(root, bg="#4CAF50", bd=10)
    border_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.7)

    # Voeg een tekstvak toe met nuttige informatie
    text_box = tk.Text(border_frame, wrap="word", height=6, font=("Arial", 12), bg="#3B3B45", fg="#FFFFFF", bd=0, padx=10, pady=10)
    text_box.insert(tk.END, "Gebruik deze applicatie om je scripts te beheren en te uploaden naar je mainframe.")
    text_box.config(state=tk.DISABLED)
    text_box.pack(fill=tk.BOTH, expand=True)

    # Knoppen voor interactie
    button_upload = ttk.Button(root, text="Script Uploaden", command=upload)
    button_upload.pack(pady=10)

    button_show_local = ttk.Button(root, text="Toon Lokale Scripts", command=show_local_scripts)
    button_show_local.pack(pady=10)

    # Start de GUI loop
    root.mainloop()

# Start de GUI wanneer het script wordt uitgevoerd
if __name__ == "__main__":
    try:
        start_gui()
    except Exception as e:
        print(f"Er is een fout opgetreden: {e}")
