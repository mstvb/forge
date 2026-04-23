# reset

## Synopsis
```
forge reset [--yes] [--dry-run] [--backup-dir <dir>]
```

## Description
Resets Forge by removing local repository data and optionally backing up files.

- `--yes` performs the reset without further confirmation.
- `--dry-run` shows which files would be deleted without actually deleting them.
- `--backup-dir <dir>` saves a backup of repository data to the given directory before reset.

## Examples
```
forge reset --dry-run
```

```
forge reset --yes
```

```
forge reset --backup-dir /tmp/forge-backup
```
