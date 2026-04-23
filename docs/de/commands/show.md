# show

Zeigt gespeicherte Inhalte nach Objekt-Hash oder anhand eines indizierten Pfads an. Gibt nur Text aus, wenn der Inhalt als UTF-8 erkannt wird; ansonsten wird Binärdaten angegeben.

## Synopsis
```
forge show --object <HASH>
forge show --path <FILE>
```

## Optionen
- `--object HASH` — zeigt den Inhalt des Objekts mit dem angegebenen SHA-1-Hash an.
- `--path FILE` — sucht `FILE` im Index und zeigt das dazugehörige gespeicherte Objekt an.

## Beschreibung
Liest die Objektbytes und gibt sie bei UTF-8-Text auf stdout aus. Bei Binärdaten wird stattdessen eine kurze Meldung ausgegeben.

Wenn `--path` verwendet wird, wird der Pfad relativ zum Repository-Root normalisiert und im Index nach dem zugehörigen Objekt-Hash gesucht.

## Beispiele
- Nach Hash anzeigen:
```
forge show --object 1a2b3c4d...
```

- Nach indiziertem Pfad anzeigen:
```
forge show --path src\app.py
```
