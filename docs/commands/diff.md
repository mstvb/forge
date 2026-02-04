# diff

Show differences between the working tree and the index.

## Synopsis
```
forge diff [PATHS...]
```

If no `PATHS` are specified, diffs all indexed files and also reports differences for untracked files.

## Description
- For text files, prints a unified diff (`a/` = index, `b/` = working tree).
- For binary files, prints a short note like "Binary file X differs".
- If a file tracked in the index is missing from disk, it shows as deleted.
- If a file exists on disk but is not in the index, it shows as untracked added content.

## Examples
- Diff everything:
```
forge diff
```

- Diff a single file:
```
forge diff src\app.py
```
