# branch

Manage branches in the repository.

## Synopsis
```
forge branch --list
forge branch --create <name>
forge branch --checkout <name>
forge branch --delete <name>
```

## Description
Branches are simple pointers to commits. Without options, `forge branch` prints all known branches and marks the current branch with `*`.

- `--list` shows all branches.
- `--create <name>` creates a new branch at the current `HEAD` commit.
- `--checkout <name>` switches `HEAD` to the named branch.
- `--delete <name>` removes a branch.

## Example
```
forge branch --create feature/login
forge branch --list
forge branch --checkout feature/login
```
