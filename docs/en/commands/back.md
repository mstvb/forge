# back

Restore the working tree and index to a previous snapshot by matching the commit message.

## Synopsis
```
forge back "MESSAGE_SUBSTRING"
```

## Description
Searches commits whose `message` contains the given text (case‑insensitive). Among matches, selects the newest by timestamp. Restores all files from that snapshot to disk, replaces the current index with the snapshot’s file map, and updates `HEAD` to the chosen commit.

If no matching snapshot is found, prints an error.

## Examples
- Restore by partial message:
```
forge back "Initial"
```
