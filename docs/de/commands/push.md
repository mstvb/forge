# push

Kopiert alle Repository-Daten in ein Zielverzeichnis (einfache Remote-Kopie).

## Synopsis
```
forge push <DESTINATION_DIR>
```

## Beschreibung
Kopiert `.forge/objects/` und `.forge/commits/` aus dem aktuellen Repository in das Zielverzeichnis. Wenn das Ziel bereits diese Ordner enthält, werden sie ersetzt. Dies ist für einfache Backups oder das Teilen von Snapshots gedacht — es gibt kein Netzwerkprotokoll oder Merge-Logik.

Wenn lokale Ordner fehlen (z. B. noch keine Objekte), werden sie übersprungen.

## Beispiele
- Auf einen USB-Stick oder ein Netzlaufwerk pushen:
```
forge push D:\backups\myproject
```
