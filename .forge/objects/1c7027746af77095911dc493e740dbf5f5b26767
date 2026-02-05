# Workflows

This page shows common day‑to‑day workflows using Forge.

## Daily workflow

1) Initialize (once per project):
```
forge init
```

2) Add files to tracking:
```
forge add --all
```

3) Commit a snapshot with a message:
```
forge commit "Initial setup"
```

4) Make changes, review, and commit:
```
forge status
forge diff
forge commit "Describe the change"
```

Repeat step 4 as needed.

## Restore a file or the whole tree

- Restore everything the index currently tracks:
```
forge restore --all
```

- Restore just one file:
```
forge restore path\to\file
```

## Go back to a previous snapshot by message

Find the snapshot by (partial) message and restore it:
```
forge back "Initial"
```
This restores all files from that snapshot and moves `HEAD` to it.

## Stop tracking or delete files

- Stop tracking but keep on disk:
```
forge rm --cached path\to\file
```

- Stop tracking and delete from disk:
```
forge rm path\to\file
```

## Share or back up snapshots (simple remote copy)

- Push your local objects and commits to a directory (e.g., a USB drive or network share):
```
forge push D:\backups\myproject
```

- Later, pull new data into another clone/folder:
```
forge pull D:\backups\myproject
```

Notes:
- `push` recreates `objects/` and `commits/` at the destination.
- `pull` adds missing items locally (non‑destructive).
