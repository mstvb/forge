# restore

Restore files from the index (from stored objects) to the working tree.

## Synopsis
```
forge restore [--all] [PATHS...]
```

## Options
- `--all` — restore all files currently listed in the index.

## Description
Determines target paths either from `PATHS` or, with `--all`, from the full index. For each target, reads the corresponding object from `.forge/objects/` and writes it to the working tree, creating parent directories as needed. Prints how many files were restored.

If a requested path is not in the index, it prints a warning and skips it. If an object is missing, it reports an error for that path.

## Examples
- Restore everything tracked:
```
forge restore --all
```

- Restore just one file:
```
forge restore src\app.py
```
