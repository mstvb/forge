# status

Zeigt den aktuellen Status an: staged, geändert, gelöscht, untracked.

## Synopsis
```
forge status
```

## Beschreibung
Vergleicht den Arbeitsbaum mit dem Index und gibt vier Gruppen aus:
- Staged: Dateien im Index, die mit ihrem gespeicherten Objekt-Hash übereinstimmen.
- Geändert: indizierte Dateien, deren aktueller Inhalt vom Index abweicht.
- Gelöscht: indizierte Dateien, die auf der Festplatte fehlen.
- Untracked: Dateien im Arbeitsbaum, die nicht im Index stehen.

Wenn es nichts zu berichten gibt, wird eine Meldung für ein sauberes Arbeitsverzeichnis ausgegeben.

## Beispiel
```
forge status
Staged:
  src/app.py
Geändert:
  README.md
Untracked:
  notes/todo.txt
```
