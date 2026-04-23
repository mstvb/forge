# show

Display stored content by object hash or by an indexed path. Only prints text if the content appears to be UTF‑8; otherwise indicates binary data.

## Synopsis
```
forge show --object <HASH>
forge show --path <FILE>
```

## Options
- `--object HASH` — show the contents of the object with the given SHA‑1 hash.
- `--path FILE` — look up `FILE` in the index and show its stored object.

## Description
Reads the object bytes and, if they look like UTF‑8 text, prints them to stdout. For binary data, prints a short note instead.

If `--path` is used, the path is normalized relative to the repository root and looked up in the index to find its object hash.

## Examples
- Show by hash:
```
forge show --object 1a2b3c4d...
```

- Show by indexed path:
```
forge show --path src\app.py
```
