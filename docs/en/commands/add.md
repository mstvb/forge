# add

Add files to the index (stage for snapshot). Supports adding specific paths or everything recursively, excluding the `.forge` folder.

## Synopsis
```
forge add [--all] [FILES...]
```

## Options
- `--all` — add all files under the current directory, recursively (skips `.forge`).

## Description
Reads file bytes, computes a SHA‑1 hash, stores unique content in `.forge/objects/`, and records the path→hash mapping in the index. Paths are stored relative to the repo root with forward slashes.

## Examples
- Add everything:
```
forge add --all
```

- Add specific files:
```
forge add src\main.py README.md
```

