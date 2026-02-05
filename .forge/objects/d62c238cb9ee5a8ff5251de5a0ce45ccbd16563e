# Troubleshooting

Common issues and how to resolve them.

## "Fehler: Kein Repository gefunden. Schmiede ein neues Repository mit 'forge init'."
- Cause: You are running a command in a folder that doesn’t have a `.forge` directory.
- Fix: Run `forge init` in your project root to create a repository.

## "[Forge] >> Keine Dateien für einen Snapshot."
- Cause: You tried to `commit` without staging any files in the index.
- Fix: Run `forge add --all` (or add specific files), then commit again.

## Missing object for a file (e.g., "Objekt <hash> fehlt …")
- Cause: The object referenced by the index or commit is not present in `.forge/objects/`.
- Fix: If you have a backup or remote, run `forge pull <source>` to fetch missing objects. Otherwise, re-add the file from disk if available.

## Permission denied when writing files
- Cause: The file is read-only or locked by another process.
- Fix: Close any programs locking the file or adjust permissions, then retry the command.

## Paths look odd on Windows (forward slashes)
- Cause: Forge normalizes internal paths to forward slashes for cross-platform consistency.
- Fix: This is expected. On disk, Forge writes using the correct OS path separators.

## I restored a snapshot and lost untracked changes
- Cause: `forge back` restores files from a snapshot and writes them to disk; untracked files are not part of the snapshot.
- Fix: Before running `back`, commit or copy your work elsewhere. Use `forge status` to see untracked files.

## After pull, history doesn’t show new commits
- Cause: `pull` adds objects/commits but doesn’t change your `HEAD`.
- Fix: Verify with `forge log`. If needed, restore a specific snapshot with `forge back "message"`.

## Binary file outputs are not displayed in diff/show
- Cause: Forge avoids printing binary data to the terminal.
- Fix: This is expected. Use external tools to inspect binary content if needed.
