# rm

Remove paths from the index and optionally from disk.

## Synopsis
```
forge rm [--cached] PATHS...
```

## Options
- `--cached` — remove only from the index; do not delete the file from disk.

## Description
For each path, removes the corresponding entry from the index. If `--cached` is not provided, also deletes the file from disk (if it exists and is a regular file). Paths are normalized relative to the repository root.

Non-indexed paths are reported and skipped.

## Examples
- Untrack a file but keep it on disk:
```
forge rm --cached notes\todo.txt
```

- Untrack and delete from disk:
```
forge rm build\artifact.bin
```
