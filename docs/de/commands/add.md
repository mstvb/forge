# add

Fügt Dateien dem Index hinzu (für einen Snapshot vormerken). Unterstützt das Hinzufügen einzelner Pfade oder alles rekursiv und schließt den `.forge`-Ordner aus.

## Synopsis
```
forge add [--all] [FILES...]
```

## Optionen
- `--all` — fügt alle Dateien im aktuellen Verzeichnis rekursiv hinzu (überspringt `.forge`).

## Beschreibung
Liest die Dateiinhalte ein, berechnet einen SHA-1-Hash, speichert eindeutige Inhalte in `.forge/objects/` und legt die Pfad→Hash-Zuordnung im Index ab. Pfade werden relativ zum Repository-Root mit Vorwärtsschrägstrichen gespeichert.

## Beispiele
- Alles hinzufügen:
```
forge add --all
```

- Bestimmte Dateien hinzufügen:
```
forge add src\main.py README.md
```
