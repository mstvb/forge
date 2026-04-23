# log

List commit history following `HEAD` from newest to oldest.

## Synopsis
```
forge log
```

## Description
Traverses the commit chain starting at `HEAD`, following each commit’s `parent` to print a linear history. If `HEAD` is not set, falls back to listing available commits unsorted.

## Example
```
forge log
--- Historie (HEAD → …) ---
[1a2b3c4] 2026-02-04 18:00:00 | Add feature
[0f1e2d3] 2026-02-04 17:00:00 | Initial setup
```
