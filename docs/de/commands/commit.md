# commit

Erstellt einen Snapshot (Commit) des aktuellen Index mit einer Nachricht. Aktualisiert `HEAD` auf den neuen Commit.

## Synopsis
```
forge commit "MESSAGE"
```

## Beschreibung
Erstellt ein Commit-Objekt, das den aktuellen Index, Ihre Nachricht, einen Zeitstempel und eine `parent`-Referenz auf den vorherigen Commit (falls vorhanden) enthält. Der Commit-Hash wird stabil aus dem JSON-Inhalt berechnet, dann in `.forge/commits/` geschrieben und `HEAD` auf diesen Hash gesetzt.

Wenn keine Dateien im Index gestaged sind, gibt der Befehl eine Meldung aus und beendet sich.

## Beispiele
```
forge commit "Initial setup"
[Forge] >> Commit 1a2b3c4 gespeichert.
```
