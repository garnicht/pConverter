# What is this repo about?

# Wie nutze ich diese files? First time installation.
1. Installiere python für dein Betriebssystem: https://www.python.org/downloads/
2. Lade diesen kompletten Ordner herunter, entpacke ihn und speicher ihn am Ort deiner Wahl. 
3. Setze Python Launcher.app als defualt für .py Dateien. (Kann bei Windows variieren)
    - Rechtsklick auf .py Datei
    - öffnen mit 
    - andere
    - Python 3.12 Ordner öffnen
    - Python Launcher.app auswählen 
    - "Immer öffnen mit" Checkbox anklicken
4. Führe install_requirements.py aus
    - ggf. wird um die Installation von dev tools gebeten. -> installieren
    - wiederhole Punkt 4
5. Beende das Terminal und starte es neu
6. converter.py nun ready to use

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
