# diff

Zeigt Unterschiede zwischen dem Arbeitsbaum und dem Index an.

## Synopsis
```
forge diff [PATHS...]
```

Wenn keine `PATHS` angegeben sind, werden alle indizierten Dateien verglichen und auch Unterschiede für untracked Dateien angezeigt.

## Beschreibung
- Für Textdateien wird ein Unified Diff ausgegeben (`a/` = Index, `b/` = Arbeitsbaum).
- Für Binärdateien wird eine kurze Meldung wie "Binary file X differs" ausgegeben.
- Wenn eine im Index verfolgte Datei auf der Festplatte fehlt, wird dies als gelöscht angezeigt.
- Wenn eine Datei auf der Festplatte existiert, aber nicht im Index steht, wird sie als untracked hinzugefügt angezeigt.

## Beispiele
- Alles diffen:
```
forge diff
```

- Eine einzelne Datei diffen:
```
forge diff src\app.py
```
