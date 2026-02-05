# FAQ

## What is Forge?
A simple, local version-control tool that snapshots files in your project folder. It keeps data in `.forge/` and provides a small CLI.

## Is Forge a replacement for Git?
No. Forge is intentionally minimal. It’s great for quick local snapshots, experiments, and simple backups. It does not support branches or merges.

## Where does Forge store my data?
Inside a `.forge` directory at the root of your project:
- `objects/` stores file contents by SHA‑1 hash
- `commits/` stores snapshot metadata
- `index` stores the current set of tracked files
- `HEAD` points to the latest commit

## Does Forge support binary files?
Yes. Files are hashed and stored as raw bytes. `diff` and `show` will avoid printing binary blobs, and instead display a short note.

## Why do paths look like `dir/file.txt` on Windows?
Forge normalizes internal paths to use forward slashes for cross‑platform stability. When writing to disk, it uses the correct OS path separators.

## How does `back` choose which snapshot to restore?
It matches commits whose message contains your search text (case‑insensitive) and selects the newest match by timestamp.

## Does `pull` overwrite or delete local data?
No. `pull` only adds missing objects and commits; it doesn’t delete or overwrite existing items.

## Can I recover data if I delete a tracked file?
Yes. If it’s still in the index or a commit, use `forge restore path\to\file` or `forge back "message"` to restore.

## How do I remove a file from tracking but keep it on disk?
Use `forge rm --cached path\to\file`.

## What about remote hosting or collaboration?
`push` and `pull` are directory copies meant for simple backup or manual syncing. There’s no network protocol or conflict resolution.
