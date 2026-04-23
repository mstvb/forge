# pull

Holt neue Repository-Daten aus einem Quellverzeichnis (einfache Remote-Kopie).

## Synopsis
```
forge pull <SOURCE_DIR>
```

## Beschreibung
Liest `.forge/objects/` und `.forge/commits/` aus dem Quellverzeichnis und kopiert fehlende Elemente in das lokale Repository. Bestehende lokale Daten bleiben erhalten — es werden keine Dateien gelöscht oder überschrieben. Dies ist für einfache Backups oder manuelles Synchronisieren gedacht.

Wenn der Quellordner die erforderlichen Verzeichnisse nicht enthält, werden diese übersprungen.

## Beispiele
- In dein aktuelles Repository aus einem Backup-Verzeichnis ziehen:
```
forge pull D:\backups\myproject
```
