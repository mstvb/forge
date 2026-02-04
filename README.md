# Forge - Version Control

Local Version Control

## Contents

- [Installing](#installing)
- [Project Links](#project-links)
- [Authors](#authors)
- [License](#license)


### Installing

```bash
cd src/forge/
pip install --user --editable .
```

### Usage

> Erstelle ein Repository im aktuellen Verzeichnis
```bash
forge init
```

> Füge Dateien zu Repository hinzu
```bash
forge add --files
```

> Repository Version zu Snapshot umändern
```bash
forge back --message
```

> Füge einen Snapshot zum Repository hinzu
```bash
forge commit --message
```

> Liste alle Snapshots auf
```bash
forge log
```

> Hole Daten aus Remote-Repository
```bash
forge pull --path
```

> Übertrage Daten in ein Remote-Repository
```bash
forge push --path
```

> Zeige Status des Repository
```bash
forge status
```

## Project Links

> forge
* [Project Site](https://github.com/mstvb/forge)
* [Issues](https://github.com/mstvb/forge/issues)

## Authors

> Manuel Staufer (mstvb)
* [Github](https://github.com/mstvb)
* [Email](mailto::manuel.staufervb@gmail.com)

## License

This project is licensed with [License](LICENSE)