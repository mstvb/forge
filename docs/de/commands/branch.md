# branch

Verwaltet Branches im Repository.

## Synopsis
```
forge branch --list
forge branch --create <name>
forge branch --checkout <name>
forge branch --delete <name>
```

## Beschreibung
Branches sind einfache Zeiger auf Commits. Ohne Optionen zeigt `forge branch` alle bekannten Branches an und markiert den aktuellen Branch mit `*`.

- `--list` zeigt alle Branches.
- `--create <name>` erstellt einen neuen Branch beim aktuellen `HEAD`-Commit.
- `--checkout <name>` wechselt `HEAD` auf den angegebenen Branch.
- `--delete <name>` entfernt einen Branch.

## Beispiel
```
forge branch --create feature/login
forge branch --list
forge branch --checkout feature/login
```
