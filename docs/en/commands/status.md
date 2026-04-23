# status

Show the current state: staged, changed, deleted, untracked.

## Synopsis
```
forge status
```

## Description
Compares the working tree with the index and prints four groups:
- Staged: files in the index that match their stored object hash.
- Changed: indexed files whose current content differs from the index.
- Deleted: indexed files missing from disk.
- Untracked: files in the working tree that are not in the index.

If there is nothing to report, prints a clean-working-directory message.

## Example
```
forge status
Staged:
  src/app.py
Geändert:
  README.md
Untracked:
  notes/todo.txt
```
