# log

Listet die Commit-Historie beginnend bei `HEAD` von neu nach alt auf.

## Synopsis
```
forge log
```

## Beschreibung
Durchläuft die Commit-Kette ab `HEAD` und folgt dabei der `parent`-Verknüpfung jedes Commits, um eine lineare Historie auszugeben. Wenn `HEAD` nicht gesetzt ist, werden stattdessen verfügbare Commits unsortiert aufgelistet.

## Beispiel
```
forge log
--- Historie (HEAD → …) ---
[1a2b3c4] 2026-02-04 18:00:00 | Add feature
[0f1e2d3] 2026-02-04 17:00:00 | Initial setup
```
