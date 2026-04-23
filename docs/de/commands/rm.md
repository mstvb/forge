# rm

Entfernt Pfade aus dem Index und optional von der Festplatte.

## Synopsis
```
forge rm [--cached] PATHS...
```

## Optionen
- `--cached` — entfernt nur aus dem Index; löscht die Datei nicht von der Festplatte.

## Beschreibung
Für jeden Pfad entfernt der Befehl den entsprechenden Eintrag aus dem Index. Wenn `--cached` nicht angegeben ist, wird die Datei zusätzlich von der Festplatte gelöscht (falls sie existiert und eine reguläre Datei ist). Pfade werden relativ zum Repository-Root normalisiert.

Nicht im Index stehende Pfade werden gemeldet und übersprungen.

## Beispiele
- Eine Datei enttracken, aber auf der Festplatte lassen:
```
forge rm --cached notes\todo.txt
```

- Enttracken und von der Festplatte löschen:
```
forge rm build\artifact.bin
```
