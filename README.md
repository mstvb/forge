# Forge - Version Control

Local Version Control

## Contents

- [Installation](#installation)
- [Commands](#commands)
- [Project Links](#project-links)
- [Authors](#authors)

## Installation

### Windows Installation

Install UV
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Create Virtual Environment [.venv]
```bash
uv venv
```

Install PIPX
```bash
uv pip install pipx
```

Clone Repository
```bash
git clone https://github.com/mstvb/forge.git
```

Go to Directory
```bash
cd forge
```

Install Package with PIPX
```bash
uv run pipx install .
```

### Linux Installation

Install UV
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Create Virtual Environment [.venv]
```bash
uv venv
```

Install PIPX
```
uv pip install pipx
```

Clone Repository
```bash
git clone https://github.com/mstvb/forge.git
```

Go to Directory
```bash
cd forge
```

Install Package with PIPX
```bash
uv run pipx install .
```

## Commands

- ADD - Add Files
- BACK - Restore to last Snapshot (Commit)
- COMMIT - Commit Version
- DIFF - Show Difference 
- INIT - Initalize Version Control
- LOG - List History
- PULL - Copy Repository Data from other Drive
- PUSH - Copy Repository to new Destination
- RESTORE - Restore Files 
- RM - Remove Files
- SHOW - Display Content
- STATUS - List >> [ Staged | Changed | Deleted | Untracked ] Files
- TAG - Tags 
- RESET - Reset Forge
- BRANCH - Branches

## Project Links

> forge
* [Project Site](https://github.com/mstvb/forge)
* [Issues](https://github.com/mstvb/forge/issues)

## Authors

> Manuel Staufer (mstvb)
* [Github](https://github.com/mstvb)
* [Email](mailto::manuel.staufervb@gmail.com)
