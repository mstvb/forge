# commit

Create a snapshot (commit) of the current index with a message. Updates `HEAD` to the new commit.

## Synopsis
```
forge commit "MESSAGE"
```

## Description
Builds a commit object containing the current index, your message, a timestamp, and a `parent` reference to the previous commit (if any). The commit hash is computed stably from its JSON content, then written to `.forge/commits/`, and `HEAD` is set to this hash.

If no files are staged in the index, the command prints a message and exits.

## Examples
```
forge commit "Initial setup"
[Forge] >> Commit 1a2b3c4 gespeichert.
```
