# back

Stellt den Arbeitsbaum und den Index auf einen früheren Snapshot anhand der Commit-Nachricht wieder her.

## Synopsis
```
forge back "MESSAGE_SUBSTRING"
```

## Beschreibung
Durchsucht Commits, deren `message` den angegebenen Text (case-insensitive) enthält. Wählt unter den Treffern den neuesten nach Zeitstempel aus. Stellt alle Dateien aus diesem Snapshot auf der Festplatte wieder her, ersetzt den aktuellen Index durch die Dateizuordnung des Snapshots und aktualisiert `HEAD` auf diesen Commit.

Wenn kein passender Snapshot gefunden wird, wird eine Fehlermeldung ausgegeben.

## Beispiele
- Wiederherstellen nach Teilnachricht:
```
forge back "Initial"
```
