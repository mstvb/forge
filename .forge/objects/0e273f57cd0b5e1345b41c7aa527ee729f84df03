# pull

Fetch new repository data from a source directory (simple remote copy).

## Synopsis
```
forge pull <SOURCE_DIR>
```

## Description
Reads `.forge/objects/` and `.forge/commits/` from the source directory and copies any missing items into the local repository. Existing local data is preserved—there is no deletion or overwrite of existing files. This is intended for simple backups or manual syncing.

If the source does not contain the folders, they are skipped gracefully.

## Examples
- Pull into your current repository from a backup folder:
```
forge pull D:\backups\myproject
```
