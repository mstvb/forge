# restore

Stellt Dateien aus dem Index (aus gespeicherten Objekten) in den Arbeitsbaum wieder her.

## Synopsis
```
forge restore [--all] [PATHS...]
```

## Optionen
- `--all` — stellt alle derzeit im Index gelisteten Dateien wieder her.

## Beschreibung
Bestimmt Zielpfade entweder aus `PATHS` oder bei `--all` aus dem vollständigen Index. Für jedes Ziel liest es das entsprechende Objekt aus `.forge/objects/` und schreibt es in den Arbeitsbaum, wobei bei Bedarf Elternverzeichnisse erstellt werden. Gibt aus, wie viele Dateien wiederhergestellt wurden.

Wenn ein angeforderter Pfad nicht im Index steht, wird eine Warnung ausgegeben und der Pfad übersprungen. Wenn ein Objekt fehlt, wird für diesen Pfad ein Fehler gemeldet.

## Beispiele
- Alle verfolgten Dateien wiederherstellen:
```
forge restore --all
```

- Nur eine Datei wiederherstellen:
```
forge restore src\app.py
```
