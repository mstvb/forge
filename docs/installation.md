# Installation

Forge requires Python 3.12 or newer.

Install in editable (development) mode from the project root:

```
pip install --user --editable .
```

This will install the `forge` command.

Verify installation:

```
forge --help
```

Notes:
- On Windows PowerShell you might need to restart your terminal after install.
- The CLI entry point is exposed as `forge` via the project configuration.
