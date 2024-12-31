# Zowe CLI Scriptbeheer

## Projectoverzicht
Dit project is een grafische gebruikersinterface (GUI) die ik heb ontwikkeld met Python's Tkinter, 
waarmee ik scripts kan beheren via Zowe CLI. 
Het platform maakt het mogelijk om scripts te downloaden, uploaden en te valideren via Zowe CLI-commando's. 
Gebruikers kunnen verbinding maken met de mainframe, scripts uploaden naar of downloaden van datasets en de 
scripts valideren om ervoor te zorgen dat ze voldoen aan de vereiste voorwaarden.

### Functies:
1. **Zowe CLI configuratie**: Stel de Zowe CLI-omgeving in met host, poort, gebruikersnaam en wachtwoord.
2. **Script downloaden**: Download scripts van de mainframe naar de lokale machine.
3. **Script uploaden**: Upload scripts van de lokale machine naar de mainframe.
4. **Scriptvalidatie**: Valideer scripts voordat ze worden geüpload of gedownload om te controleren of ze aan bepaalde voorwaarden voldoen (zoals bestandstype en leegte).

## Installatie-instructies

1. Zorg ervoor dat **Python 3.x** geïnstalleerd is.
2. Installeer de benodigde Python-pakketten:
    ```bash
    pip install tkinter subprocess logging
    ```
3. Zorg ervoor dat **Zowe CLI** geïnstalleerd en correct geconfigureerd is op je systeem. Meer informatie over de installatie van Zowe CLI vind je op de officiële [Zowe website](https://www.zowe.org/).

## Gebruik

### 1. Start de GUI
Om het platform te starten, voer ik het Python-script uit:
```bash
python app.py
  ```
## 2. Configureer Zowe CLI
Ik klik op de knop **"Configureer Zowe"** om verbinding te maken met de mainframe.  
Ik vul het hostadres, poortnummer, gebruikersnaam en wachtwoord in om de verbinding tot stand te brengen. Deze gegevens worden gebruikt om de Zowe CLI-omgeving correct in te stellen, zodat ik toegang krijg tot de mainframe.

## 3. Script Downloaden
Ik klik op de knop **"Download Script"** om een script van de mainframe naar mijn lokale machine te downloaden.  
Ik voer de naam van het script in dat ik wil downloaden.  
Vervolgens kies ik een locatie op mijn lokale machine om het bestand op te slaan.  


## 4. Script Uploaden
Ik klik op de knop **"Upload Bestand"** om een bestand van mijn lokale machine naar de mainframe te uploaden.  
Ik kies het bestand dat ik wil uploaden en voer de naam in van de remote dataset op de mainframe waar het bestand moet worden geüpload.

## Validatie
De validatie controleert of een bestand aan de volgende eisen voldoet:

- **Bestandstype**: Het bestandstype wordt gecontroleerd en alleen toegestane bestandstypes worden geaccepteerd. Afbeeldingen, video's, Office-documenten en andere niet-programmeerbare bestanden worden geweigerd.
- **Leegte**: Het bestand mag niet leeg zijn.

De validatie zorgt ervoor dat alleen geldige bestanden geüpload of gedownload kunnen worden.

## Mijn ervaring en problemen
Tijdens het ontwikkelen van dit project liep ik tegen een technisch probleem aan waarbij 
mijn verbinding met de mainframe niet goed werkte. Dit probleem verhinderde mij om de 
Zowe CLI-commando's succesvol uit te voeren, wat essentieel was voor het testen van de 
functionaliteiten van de applicatie. Ondanks mijn pogingen om de configuratie van Zowe 
CLI na te kijken en de verbinding te herstellen, was het niet mogelijk om verbinding te maken met de mainframe.

Als gevolg van deze technische moeilijkheden heb ik het project niet volledig 
kunnen afmaken zoals oorspronkelijk gepland. Omdat de applicatie niet volledig werkt heb ik ook gedaan screencast gemaakt.

