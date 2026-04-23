# reset

## Synopsis
```
forge reset [--yes] [--dry-run] [--backup-dir <dir>]
```

## Beschreibung
Setzt Forge zurück, indem lokale Repository-Daten entfernt und optional Dateien gesichert werden.

- `--yes` führt den Reset ohne weitere Bestätigung aus.
- `--dry-run` zeigt an, welche Dateien gelöscht würden, ohne sie tatsächlich zu löschen.
- `--backup-dir <dir>` speichert ein Backup der Repository-Daten im angegebenen Verzeichnis, bevor der Reset durchgeführt wird.

## Beispiele
```
forge reset --dry-run
```

```
forge reset --yes
```

```
forge reset --backup-dir /tmp/forge-backup
```
