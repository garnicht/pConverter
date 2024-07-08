# What is this repo about?
Make pCon csv export usable for weclapp csv import.

# Wie nutze ich diese files? First time installation Windows
1. Installiere python: https://www.python.org/downloads/:
    - [x] Use admin privileges... if possible
    - [x] Add python.exe to PATH 
    - [x] remove the MAX_PATH Limitation..., if asked

2. Lade den kompletten Ordner von github.com herunter, entpacke ihn und speicher ihn am Ort deiner Wahl:
    - klicke auf den Grünen Button "<> Code"
    - klicke auf "Download ZIP"

3. Installiere Microsoft Visual C++ 14.0: https://visualstudio.microsoft.com/de/visual-cpp-build-tools/
    - Installiere

4. Setze Python.exe als defualt/standard für .py Dateien, falls erforderlich.
        - Rechtsklick auf .py Datei
        - öffnen mit 
        - andere
        - wählen sie app von pc

4. Führe install_requirements.py aus (zu finden im heruntergeladenen Ordner)
    - falls es nicht geht, installiere "Microsoft Visual C++ 14.0": https://visualstudio.microsoft.com/de/visual-cpp-build-tools/
        - NUR "Desktopentwicklung mit C++" anklicken und installieren
        - wiederhole Punkt 4
5. Beende das Terminal und starte es neu

6. converter.py nun ready to use, d.h. die Datei kann auch an anderen Ort verschoben werden.


# Wie nutze ich diese files? First time installation MAC
1. Installiere python für dein Betriebssystem: https://www.python.org/downloads/

2. Lade den kompletten Ordner von github.com herunter, entpacke ihn und speicher ihn am Ort deiner Wahl
    - klicke auf den Grünen Button "<> Code"
    - klicke auf "Download ZIP"

3. Setze Python Launcher.app als defualt/standard für .py Dateien.
    - Entweder:
        - Rechtsklick auf .py Datei
        - öffnen mit 
        - andere
        - Python 3.12 Ordner öffnen
        - Python Launcher.app auswählen 
        - "Immer öffnen mit" Checkbox anklicken
    - Oder:
        - wähle eine .py Datei aus
        - drücke command + I
        - unter öffnen mit, wähle Python Launcher.app
        - klicke auf Button "Alle ändern..."

4. Führe install_requirements.py aus (zu finden im heruntergeladenen Ordner)
    - ggf. wird um die Installation von dev tools gebeten. -> installieren
    - wiederhole Punkt 4

5. Beende das Terminal und starte es neu

6. converter.py nun ready to use, d.h. die Datei kann auch an anderen Ort verschoben werden.

# Wie funktioniert converter.py? 
- Converter.py benötigt eine csv mit dem Namen import.csv in der selben directory (Ordner/Folder). 
- Kopfartikelnummer wird als Input via Terminal erfragt
- Converter.py ändert nun das csv Format und fügt die Artikelnummer an der richtigen Stelle ein
- standard output -> finished_[Kopfartikelnummer].csv. Falls bereits vorhanden, wird der alte Output überschrieben. 

# Wie kann ich eine requirements.txt erstellen? 
nutze hierfür folgenden Befehl: 

```
pip list --format=freeze > requirements.txt
```

ohne 'list --format=' ist der output im falschen Format falls eine Conda env genutzt wird

# Wie umgehe ich das "python not found" problem? 
Anstatt 
```
pip install -r requirements.txt
```
nutzen wir
```
python3 -m pip install -m requirements.txt
```
improvement ideas: 
- [x] name von import.csv to import_[Kopfartikelnummer].csv. [Kopfartikelnummer] = Variable. Um manuelles eintippen von Artikelnumer zu unmgehen
- [ ] Mit hilfe von weclapp api artikel automatisch erstellen mit all den gewünschten Daten 
- [ ] mit hilfe von weclapp api und evtl. artikelliste.csv artikelliste hochladen 
- [ ] change install_requirements.py to check which platform its executed, then executes different subprocess -> for windows its python -m... not python3 -m...
- [ ] delete the old csvs? 