# Quickstart

This quickstart walks you through the most common Forge tasks in a fresh folder.

Assumptions:
- Windows PowerShell is shown in examples (works similarly on other platforms).
- You are in your project folder.

## 1. Initialize a repository

```
forge init
```

This creates a `.forge` folder with `objects`, `commits`, an empty `HEAD`, and an empty `index`.

## 2. Add files

- Add specific files:

```
forge add path\to\file1 path\to\file2
```

- Add everything (recursively), excluding `.forge`:

```
forge add --all
```

## 3. Commit staged files

```
forge commit "Initial snapshot"
```

Each commit stores the current index and links to the previous one via a `parent` field. `HEAD` is updated to the new commit.

## 4. Check status and view diffs

```
forge status
forge diff
```

- `status` lists staged, changed, deleted, and untracked files.
- `diff` shows a unified diff between the index and the working tree for text files.

## 5. Make changes, commit again

Edit a tracked file, then:

```
forge diff
forge commit "Change content"
```

## 6. Browse history

```
forge log
```

Shows the history following `HEAD` from newest to oldest.

## 7. Restore to a previous snapshot by message

```
forge back "Initial"
```

Matches by partial or full commit message, selects the newest match, restores files, updates `index` and `HEAD`.

## 8. Remove files from tracking (and disk)

- Only unstage (keep file on disk):

```
forge rm --cached path\to\file
```

- Also delete from disk:

```
forge rm path\to\file
```

## 9. Restore files from the index

- Restore all indexed files:

```
forge restore --all
```

- Restore specific paths:

```
forge restore path\to\file
```

## 10. Show stored content

- By object hash:

```
forge show --object <sha1>
```

- By indexed path:

```
forge show --path path\to\file
```

## 11. Simple remote copy (push/pull)

- Push to a directory:

```
forge push D:\some\remote\folder
```

- Pull new data from a directory:

```
forge pull D:\some\remote\folder
```

Notes:
- Push recreates the `objects` and `commits` folders at the destination.
- Pull adds any missing objects/commits locally (non-destructive).
