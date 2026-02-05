# Concepts

Forge is a simple, local version-control system. Understanding a few core concepts helps you use it effectively.

## Repository layout

A Forge repository is any folder that contains a `.forge` directory. Inside `.forge` you will find:

- `objects/` — content-addressed file blobs, named by their SHA‑1 hash.
- `commits/` — JSON files representing snapshots of the index (with timestamp, message, parent, and file map).
- `index` — JSON map of tracked paths to object hashes.
- `HEAD` — text file containing the hash of the latest commit (or empty if none yet).

## Index

The index is a mapping of relative file paths to object hashes. Paths are stored relative to the repository root and normalized to use forward slashes (`/`) so they are stable across platforms.

Adding files updates the index and stores their contents as objects. Committing snapshots the current index into a commit object.

## Objects

Objects are binary-safe. When you `add` a file, Forge reads its bytes and computes a SHA‑1 hash of those bytes. If the object doesn’t exist yet in `.forge/objects`, it is written once and reused by reference in the index and commits.

## Commits and HEAD

A commit captures the current `index` plus metadata:
- `timestamp` (local time string)
- `message` (your text)
- `parent` (the previous commit’s hash if any)
- `files` (a copy of the index at the time)

`HEAD` contains the latest commit hash. The `log` command follows `HEAD → parent → ...` to print history from newest to oldest.

## Binary safety and text output

All content I/O is binary-safe. Commands that print file contents to the terminal (like `diff` and `show`) only render text if the data looks like UTF‑8. Otherwise they print a friendly note that binary data is not displayed.

## Path normalization

Forge normalizes paths when storing them in the index and commits. Even on Windows, they are stored as `subdir/file.txt` with forward slashes. On disk, Forge always writes to the correct OS path.

## Remote copy (push/pull)

Forge’s `push`/`pull` are simple directory copies for `.forge/objects` and `.forge/commits`:
- `push` recreates those folders at the destination.
- `pull` adds any missing objects/commits locally without deleting anything.

This is not a network protocol; it’s intended for simple backups or sharing snapshots between folders or machines.
