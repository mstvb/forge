# push

Copy all repository data to a destination directory (simple remote copy).

## Synopsis
```
forge push <DESTINATION_DIR>
```

## Description
Copies `.forge/objects/` and `.forge/commits/` from the current repository to the destination. If the destination already contains those folders, they are replaced. This is intended for simple backups or sharing snapshots—there is no network protocol or merge logic.

If local folders are missing (e.g., no objects yet), the command skips them gracefully.

## Examples
- Push to a USB drive or network share:
```
forge push D:\backups\myproject
```
