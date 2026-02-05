#!/usr/bin/env python3
import os
import hashlib
import json
import click
import shutil
import difflib
from datetime import datetime

class Forge:
    """
    Parameters
    ----------
    base_path : str | default = '.forge'
        Path of Forge

    Attributes
    ----------
    base_path : str
        Path of Forge

    objects_path : str
        Path of Objects

    commit_path : str
        Path of Commits

    index_path : str
        Path of Indexes

    Methods
    -------
    ensure_repo()
        Check Forge is Initialized

    _hash_file(data)
        Hash Files for Version Control

    _get_index()
        Returns Index of Repository

    _save_index()
        Save Index of Repository
    """
    def __init__(self, base_path: str = '.forge'):
        self.base_path = base_path
        self.objects_path = os.path.join(self.base_path, "objects")
        self.commits_path = os.path.join(self.base_path, "commits")
        self.index_path = os.path.join(self.base_path, "index")
        self.head_path = os.path.join(self.base_path, "HEAD")

    def ensure_repo(self):
        if not os.path.exists(self.base_path):
            click.secho("Fehler: Kein Repository gefunden. Schmiede ein neues Repository mit 'forge init'.")
            exit(1)
        # Ensure subdirectories exist for robustness
        os.makedirs(self.objects_path, exist_ok=True)
        os.makedirs(self.commits_path, exist_ok=True)

    def _hash_file(self, data):
        """Backward-compatible: hash a text string (UTF-8). Prefer _hash_bytes."""
        if isinstance(data, bytes):
            return hashlib.sha1(data).hexdigest()
        return hashlib.sha1(str(data).encode("utf-8")).hexdigest()

    def _hash_bytes(self, data: bytes) -> str:
        return hashlib.sha1(data).hexdigest()

    def _relpath(self, path: str) -> str:
        """Normalize a path to be relative to repo root, with forward slashes for stability."""
        p = os.path.relpath(path, start=os.getcwd())
        return p.replace("\\", "/")

    def _abspath(self, rel: str) -> str:
        return os.path.abspath(rel)

    def _read_json(self, path: str, default):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return default

    def _write_json(self, path: str, data):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, sort_keys=True)

    def _get_index(self):
        return self._read_json(self.index_path, {})

    def _save_index(self, index):
        # ensure keys normalized
        norm = {self._relpath(k): v for k, v in index.items()}
        self._write_json(self.index_path, norm)

    def _read_head(self):
        try:
            with open(self.head_path, "r", encoding="utf-8") as f:
                return f.read().strip() or None
        except FileNotFoundError:
            return None

    def _write_head(self, commit_hash: str):
        with open(self.head_path, "w", encoding="utf-8") as f:
            f.write(commit_hash + "\n")

    def _read_commit(self, commit_hash: str):
        path = os.path.join(self.commits_path, commit_hash)
        return self._read_json(path, None)

    def _write_commit(self, commit_hash: str, data: dict):
        path = os.path.join(self.commits_path, commit_hash)
        self._write_json(path, data)

# --- CLI Definition mit Click ---

@click.group()
def cli():
    """Forge - Version Control"""
    pass

@cli.command()
def init():
    """Erstelle ein neues Forge-Repository im aktuellen Verzeichnis.
    
    Initialisiert die notwendige Verzeichnisstruktur für Versionskontrolle.
    """
    f = Forge()
    if os.path.exists(f.base_path):
        click.secho("[Forge] >> Repository existiert bereits.", fg="red", bold=True)

    else:
        for path in [f.base_path, f.objects_path, f.commits_path]:
            os.makedirs(path, exist_ok=True)
        # create empty HEAD and index
        with open(f.head_path, "w", encoding="utf-8") as _:
            _.write("")
        f._save_index({})
        click.secho("[Forge] >> Repository erfolgreich initalisiert", fg="green", bold=True)

@cli.command()
@click.option('--all', 'add_all', is_flag=True, help='Alle Dateien rekursiv hinzufügen (ignoriert . Verzeichnisse)')
@click.argument('files', nargs=-1, type=click.Path(exists=True))
def add(add_all, files):
    """Indexiere Dateien für den nächsten Commit.
    
    Fügt Dateien dem Index hinzu. Mit --all werden alle Dateien rekursiv erfasst.
    """
    f = Forge()
    f.ensure_repo()
    index = f._get_index()

    # Verzeichnisse die grundsätzlich ignoriert werden sollen
    ignore_dirs = {'.forge', '.git', '.venv', '.idea', '__pycache__', '.pytest_cache', '.tox', '.egg-info', '.eggs', 'node_modules', '.vscode', '.env'}

    # Sammle Kandidaten
    candidates = []
    if add_all:
        for root, dirs, fnames in os.walk(os.getcwd()):
            # dirs filtern: ignorierte Verzeichnisse auslassen
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            
            for name in fnames:
                path = os.path.join(root, name)
                candidates.append(path)
    candidates.extend(files)

    added = 0
    for path in candidates:
        if os.path.isdir(path):
            continue
        try:
            with open(path, 'rb') as stream:
                content = stream.read()
        except Exception as e:
            click.secho(f"[Forge] >> Konnte {path} nicht lesen: {e}", fg='red')
            continue
        file_hash = f._hash_bytes(content)
        obj_path = os.path.join(f.objects_path, file_hash)
        if not os.path.exists(obj_path):
            with open(obj_path, 'wb') as obj:
                obj.write(content)
        index[f._relpath(path)] = file_hash
        added += 1

    f._save_index(index)
    click.secho(f"[Forge] >> {added} Datei(en) hinzugefügt.", fg="green", bold=True)

@cli.command()
@click.option('--cached', is_flag=True, help='Entferne nur aus dem Index, nicht vom Disk')
@click.option('--all', 'remove_all', is_flag=True, help='Alle Dateien aus dem Index entfernen')
@click.argument('files', nargs=-1, type=click.Path())
def rm(cached, remove_all, files):
    """Entferne Dateien aus dem Index und optional vom Disk.
    
    Removes files from the staging area. Mit --cached wird nur der Index aktualisiert.
    Ohne --cached werden Dateien auch vom Disk gelöscht.
    """
    f = Forge()
    f.ensure_repo()
    index = f._get_index()

    if not index:
        click.secho("[Forge] >> Index ist leer.", fg="yellow", bold=True)
        return

    # Sammle zu löschende Dateien
    to_delete = []
    if remove_all:
        to_delete = list(index.keys())
    else:
        for path in files:
            rel_path = f._relpath(path)
            if rel_path in index:
                to_delete.append(rel_path)
            else:
                click.secho(f"[Forge] >> '{rel_path}' nicht im Index gefunden.", fg="yellow")

    removed = 0
    for rel_path in to_delete:
        if rel_path in index:
            # Lösche aus dem Index
            del index[rel_path]
            
            # Lösche Datei vom Disk, wenn --cached nicht gesetzt
            if not cached:
                abs_path = f._abspath(rel_path)
                try:
                    if os.path.isfile(abs_path):
                        os.remove(abs_path)
                except Exception as e:
                    click.secho(f"[Forge] >> Konnte {rel_path} nicht löschen: {e}", fg="red")
                    continue
            
            removed += 1

    f._save_index(index)
    click.secho(f"[Forge] >> {removed} Datei(en) entfernt.", fg="green", bold=True)

@cli.command()
@click.argument('message', type=str, required=True)
def commit(message):
    """Erstelle einen Snapshot (Commit) des aktuellen Index mit einer Nachricht.
    
    Speichert den aktuellen Zustand indexierter Dateien als Snapshot.
    """
    f = Forge()
    f.ensure_repo()
    index = f._get_index()
    if not index:
        click.secho("[Forge] >> Keine Dateien für einen Snapshot.", fg="red", bold=True)
        return
    parent = f._read_head()
    commit_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "message": message,
        "parent": parent,
        "files": index,
    }
    # stabile Hash-Bildung
    commit_hash = hashlib.sha1(json.dumps(commit_data, sort_keys=True).encode("utf-8")).hexdigest()
    f._write_commit(commit_hash, commit_data)
    f._write_head(commit_hash)
    click.secho(f"[Forge] >> Commit {commit_hash[:7]} gespeichert.", fg="green", bold=True)

# ... (vorheriger Code bleibt gleich)

@cli.command()
def status():
    """Zeige den Status des Arbeitsverzeichnisses und des Index.
    
    Listet Dateien nach Status auf: indexed, modified, deleted, untracked.
    """
    f = Forge()
    f.ensure_repo()
    index = f._get_index()

    staged = []
    modified = []
    deleted = []
    untracked = []

    # Check indexed files against working tree
    for rel, obj_hash in index.items():
        abs_path = f._abspath(rel)
        if not os.path.exists(abs_path):
            deleted.append(rel)
            continue
        try:
            with open(abs_path, 'rb') as fh:
                data = fh.read()
        except Exception:
            continue
        h = f._hash_bytes(data)
        if h != obj_hash:
            modified.append(rel)
        else:
            staged.append(rel)

    # Find untracked files
    for root, dirs, files in os.walk(os.getcwd()):
        # skip directories starting with .
        if any(part.startswith('.') for part in root.split(os.sep)):
            continue
        # Remove directories starting with . from traversal
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for name in files:
            path = os.path.join(root, name)
            if any(part.startswith('.') for part in path.split(os.sep)):
                continue
            rel = f._relpath(path)
            if rel not in index:
                untracked.append(rel)

    if not any([staged, modified, deleted, untracked]):
        click.secho("[Forge] >> Nichts zu tun. Arbeitsverzeichnis sauber.", fg="green", bold=True)
        return

    if staged:
        click.secho("Staged:", fg='green', bold=True)
        for p in sorted(staged):
            click.secho(f"  {p}")
    if modified:
        click.secho("Geändert:", fg='yellow', bold=True)
        for p in sorted(modified):
            click.secho(f"  {p}")
    if deleted:
        click.secho("Gelöscht:", fg='red', bold=True)
        for p in sorted(deleted):
            click.secho(f"  {p}")
    if untracked:
        click.secho("Untracked:", fg='blue', bold=True)
        for p in sorted(untracked):
            click.secho(f"  {p}")

@cli.command()
@click.argument('remote_path', type=click.Path())
def push(remote_path):
    """Synchronisiere alle Snapshots und Objekte zu einem Remote-Verzeichnis.
    
    Kopiert die komplette Repository-Historie zum Remote-Standort.
    """
    f = Forge()
    f.ensure_repo()
    
    if not os.path.exists(remote_path):
        os.makedirs(remote_path)
        
    # Kopiere alle Objekte und Commits zum Ziel
    for folder in ["objects", "commits"]:
        src = os.path.join(f.base_path, folder)
        dst = os.path.join(remote_path, folder)

        # Wenn lokal nichts vorhanden ist, überspringen
        if not os.path.exists(src):
            continue

        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
        
    click.secho(f"[Forge] >> Repository erfolgreich nach {remote_path} geschoben.", fg="green", bold=True)

@cli.command()
@click.argument('remote_path', type=click.Path(exists=True))
def pull(remote_path):
    """Lade Snapshots und Objekte von einem Remote-Repository herunter.
    
    Integriert neue Commits und Objekte vom Remote ohne Überschreiben.
    """
    f = Forge()
    f.ensure_repo()
    
    # Hole Objekte und Commits vom Remote
    for folder in ["objects", "commits"]:
        src = os.path.join(remote_path, folder)
        dst = os.path.join(f.base_path, folder)

        # Wenn auf dem Remote nichts vorhanden ist, überspringen
        if not os.path.exists(src):
            continue

        # Stelle sicher, dass das lokale Zielverzeichnis existiert
        os.makedirs(dst, exist_ok=True)

        # Wir fügen nur neue Dateien hinzu, statt zu löschen
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if not os.path.exists(d):
                shutil.copy2(s, d)
                
    click.secho("[Forge] >> Neue Daten erfolgreich gezogen.", fg="green", bold=True)

@cli.command()
@click.argument('message', type=str)
def back(message):
    """Stelle den Zustand aus einem früheren Snapshot basierend auf der Nachricht wieder her.
    
    Sucht einen Snapshot mit einer übereinstimmenden Nachricht und stellt ihn wieder her.
    """
    f = Forge()
    f.ensure_repo()

    matches = []
    for c_hash in os.listdir(f.commits_path):
        data = f._read_commit(c_hash)
        if not data:
            continue
        if message.lower() in data.get('message', '').lower():
            try:
                t = datetime.strptime(data['timestamp'], "%Y-%m-%d %H:%M:%S")
            except Exception:
                # Fallback: use file modification time
                t = datetime.fromtimestamp(os.path.getmtime(os.path.join(f.commits_path, c_hash)))
            matches.append((t, c_hash, data))

    if not matches:
        click.secho(f"[Forge] >> Kein Snapshot mit Nachricht '{message}' gefunden.", fg="red", bold=True)
        return

    # Wähle den jüngsten passenden Commit
    matches.sort(reverse=True)
    chosen_time, chosen_hash, chosen_data = matches[0]

    # Wiederherstellen der Dateien aus dem Commit
    for rel_path, obj_hash in chosen_data.get('files', {}).items():
        obj_file = os.path.join(f.objects_path, obj_hash)
        if not os.path.exists(obj_file):
            click.secho(f"[Forge] >> Objekt {obj_hash} für {rel_path} fehlt.", fg="red")
            continue
        abs_path = f._abspath(rel_path)
        dir_name = os.path.dirname(abs_path)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)
        with open(obj_file, 'rb') as o, open(abs_path, 'wb') as out:
            out.write(o.read())

    # Index aktualisieren und HEAD setzen
    f._save_index(chosen_data.get('files', {}))
    f._write_head(chosen_hash)
    click.secho(f"[Forge] >> Repository auf Snapshot {chosen_hash[:7]} ('{chosen_data.get('message', '')}') zurückgesetzt.", fg="green", bold=True)

@cli.command()
def log():
    """Zeige die Snapshot-Historie ab HEAD rückwärts.
    
    Listet alle Snapshots mit Zeitstempel und Nachricht in chronologischer Reihenfolge.
    """
    f = Forge()
    f.ensure_repo()
    head = f._read_head()

    chain = []
    visited = set()
    current = head
    while current and current not in visited:
        visited.add(current)
        data = f._read_commit(current)
        if not data:
            break
        chain.append((current, data))
        current = data.get('parent')

    if not chain:
        # Fallback: keine HEAD gesetzt, zeige vorhandene Commits unsortiert
        commits = os.listdir(f.commits_path) if os.path.exists(f.commits_path) else []
        if not commits:
            click.secho("[Forge] >> Keine Snapshots vorhanden.", fg="red", bold=True)
            return
        click.secho("--- Snapshots (unsortiert) ---", fg="green")
        for c_hash in sorted(commits, reverse=True):
            data = f._read_commit(c_hash)
            if not data:
                continue
            click.secho(f"[{c_hash[:7]}] {data.get('timestamp','?')} | {data.get('message','')}" , fg="blue", bold=True)
        return

    click.secho("--- Historie (HEAD → …) ---", fg="green", bold=True)
    for c_hash, data in chain:
        click.secho(f"[{c_hash[:7]}] {data.get('timestamp','?')} | {data.get('message','')}", fg="blue", bold=True)


@cli.command()
@click.option('--cached', is_flag=True, help='Nur aus dem Index entfernen, Datei behalten')
@click.argument('paths', nargs=-1, type=click.Path())
def rm(cached, paths):
    """Entferne Dateien aus dem Index und optional vom Dateisystem.
    
    Mit --cached bleibt die Datei erhalten; ohne wird sie gelöscht.
    """
    f = Forge()
    f.ensure_repo()
    if not paths:
        click.secho("[Forge] >> Keine Pfade angegeben.", fg='red', bold=True)
        return
    index = f._get_index()
    removed = 0
    for p in paths:
        rel = f._relpath(p)
        if rel in index:
            del index[rel]
            removed += 1
            if not cached:
                abs_p = f._abspath(rel)
                if os.path.exists(abs_p) and os.path.isfile(abs_p):
                    try:
                        os.remove(abs_p)
                    except Exception as e:
                        click.secho(f"[Forge] >> Konnte {abs_p} nicht löschen: {e}", fg='red')
        else:
            click.secho(f"[Forge] >> {rel} nicht im Index.", fg='yellow')
    f._save_index(index)
    click.secho(f"[Forge] >> {removed} Pfad(e) entfernt.", fg='green', bold=True)


def _is_text_bytes(b: bytes) -> bool:
    try:
        b.decode('utf-8')
        return True
    except Exception:
        return False


@cli.command()
@click.option('--all', 'restore_all', is_flag=True, help='Alle indexierten Dateien wiederherstellen')
@click.argument('paths', nargs=-1, type=click.Path())
def restore(restore_all, paths):
    """Stelle Dateien aus dem gespeicherten Index again.
    
    Überschreibt lokale Änderungen mit der im Index gespeicherten Version.
    """
    f = Forge()
    f.ensure_repo()
    index = f._get_index()

    targets = []
    if restore_all or not paths:
        targets = list(index.keys())
    else:
        for p in paths:
            rel = f._relpath(p)
            if rel in index:
                targets.append(rel)
            else:
                click.secho(f"[Forge] >> {rel} nicht im Index.", fg='yellow')

    restored = 0
    for rel in targets:
        obj_hash = index.get(rel)
        if not obj_hash:
            continue
        obj_file = os.path.join(f.objects_path, obj_hash)
        if not os.path.exists(obj_file):
            click.secho(f"[Forge] >> Objekt {obj_hash} fehlt für {rel}.", fg='red')
            continue
        abs_path = f._abspath(rel)
        os.makedirs(os.path.dirname(abs_path) or '.', exist_ok=True)
        with open(obj_file, 'rb') as src, open(abs_path, 'wb') as dst:
            dst.write(src.read())
        restored += 1
    click.secho(f"[Forge] >> {restored} Datei(en) wiederhergestellt.", fg='green', bold=True)


@cli.command()
@click.argument('paths', nargs=-1, type=click.Path())
@click.option('--details', is_flag=True, help='Zeige vollständige Diffs statt Zusammenfassung')
def diff(paths, details):
    """Vergleiche Arbeitsverzeichnis mit dem Index - Zusammenfassung oder Details.
    
    Zeigt standardmäßig nur Zeilenzahlen. Mit --details werden vollständige Unterschiede angezeigt.
    """
    f = Forge()
    f.ensure_repo()
    index = f._get_index()

    files_with_diff = []

    def get_diff_info(rel):
        """Gibt Informationen über die Unterschiede zurück."""
        abs_path = f._abspath(rel)
        obj_hash = index.get(rel)
        
        info = {
            'file': rel,
            'status': None,
            'added_lines': 0,
            'removed_lines': 0,
            'is_binary': False
        }
        
        if obj_hash is None:
            # untracked: show as added
            if not os.path.exists(abs_path):
                return None
            with open(abs_path, 'rb') as fh:
                b = fh.read()
            if not _is_text_bytes(b):
                info['status'] = 'UNTRACKED (Binary)'
                info['is_binary'] = True
                return info
            text = b.decode('utf-8', errors='replace').splitlines(keepends=False)
            info['status'] = 'NEW FILE'
            info['added_lines'] = len(text)
            if details:
                info['diff'] = list(difflib.unified_diff([], text, fromfile=f"a/{rel}", tofile=f"b/{rel}"))
            return info
            
        obj_file = os.path.join(f.objects_path, obj_hash)
        if not os.path.exists(obj_file):
            click.secho(f"[Forge] >> Objekt {obj_hash} fehlt für {rel}.", fg='red')
            return None
            
        with open(obj_file, 'rb') as fh:
            ob = fh.read()
            
        if not os.path.exists(abs_path):
            # deleted in working tree
            if _is_text_bytes(ob):
                info['status'] = 'DELETED'
                a = ob.decode('utf-8', errors='replace').splitlines(False)
                info['removed_lines'] = len(a)
                if details:
                    info['diff'] = list(difflib.unified_diff(a, [], fromfile=f"a/{rel}", tofile=f"b/{rel}"))
            else:
                info['status'] = 'DELETED (Binary)'
                info['is_binary'] = True
            return info
            
        with open(abs_path, 'rb') as fh:
            wb = fh.read()
            
        if not _is_text_bytes(ob) or not _is_text_bytes(wb):
            if ob != wb:
                info['status'] = 'MODIFIED (Binary)'
                info['is_binary'] = True
            else:
                return None
            return info
            
        a = ob.decode('utf-8', errors='replace').splitlines(False)
        b = wb.decode('utf-8', errors='replace').splitlines(False)
        
        if a == b:
            return None
            
        info['status'] = 'MODIFIED'
        diff = list(difflib.unified_diff(a, b, fromfile=f"a/{rel}", tofile=f"b/{rel}"))
        info['added_lines'] = sum(1 for line in diff if line.startswith('+') and not line.startswith('+++'))
        info['removed_lines'] = sum(1 for line in diff if line.startswith('-') and not line.startswith('---'))
        
        if details:
            info['diff'] = diff
        return info

    def print_diff_details(info):
        """Drucke die vollständigen Diff-Details."""
        status_colors = {
            'NEW FILE': 'green',
            'MODIFIED': 'yellow',
            'DELETED': 'red',
            'UNTRACKED (Binary)': 'yellow',
            'MODIFIED (Binary)': 'yellow',
            'DELETED (Binary)': 'red'
        }
        color = status_colors.get(info['status'], 'white')
        click.secho(f"\n📄 {info['file']} ({info['status']})", fg=color, bold=True)
        
        if 'diff' in info:
            for line in info['diff']:
                if line.startswith('+++') or line.startswith('---'):
                    click.secho(line, fg='cyan')
                elif line.startswith('+'):
                    click.secho(line, fg='green')
                elif line.startswith('-'):
                    click.secho(line, fg='red')
                elif line.startswith('@@'):
                    click.secho(line, fg='blue')
                else:
                    click.echo(line)

    def print_summary(info):
        """Drucke eine Zusammenfassung."""
        status_colors = {
            'NEW FILE': 'green',
            'MODIFIED': 'yellow',
            'DELETED': 'red',
            'UNTRACKED (Binary)': 'yellow',
            'MODIFIED (Binary)': 'yellow',
            'DELETED (Binary)': 'red'
        }
        color = status_colors.get(info['status'], 'white')
        
        if info['is_binary']:
            click.secho(f"  {info['file']:<50} {info['status']}", fg=color)
        else:
            lines_info = ""
            if info['added_lines'] > 0:
                lines_info += f"+{info['added_lines']} "
            if info['removed_lines'] > 0:
                lines_info += f"-{info['removed_lines']}"
            click.secho(f"  {info['file']:<50} {info['status']:<20} {lines_info}", fg=color)

    if paths:
        rels = [f._relpath(p) for p in paths]
    else:
        # default: all indexed files
        rels = sorted(set(list(index.keys())))
        # plus untracked files
        for root, dirs, files in os.walk(os.getcwd()):
            # skip directories starting with .
            if any(part.startswith('.') for part in root.split(os.sep)):
                continue
            # Remove directories starting with . from traversal
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            for name in files:
                p = os.path.join(root, name)
                if any(part.startswith('.') for part in p.split(os.sep)):
                    continue
                rels.append(f._relpath(p))
        rels = sorted(set(rels))
    
    # Sammle alle Diffs
    for rel in rels:
        info = get_diff_info(rel)
        if info:
            files_with_diff.append(info)
    
    if not files_with_diff:
        click.secho("[Forge] >> Keine Unterschiede gefunden.", fg='green', bold=True)
        return
    
    if details:
        # Zeige vollständige Details an
        for info in files_with_diff:
            print_diff_details(info)
        click.secho(f"\n[Forge] >> {len(files_with_diff)} Datei(en) mit Unterschieden.", fg='cyan', bold=True)
    else:
        # Zeige Zusammenfassung an
        click.secho("[Forge] Unterschiede:", fg='cyan', bold=True)
        total_added = 0
        total_removed = 0
        for info in files_with_diff:
            print_summary(info)
            total_added += info['added_lines']
            total_removed += info['removed_lines']
        
        click.secho(f"\n[Forge] >> {len(files_with_diff)} Datei(en) | +{total_added} -{total_removed}", fg='cyan', bold=True)


@cli.command()
@click.option('--object', 'object_hash', help='Objekt-Hash zum Anzeigen')
@click.option('--path', 'path_arg', type=click.Path(), help='Indexierter Pfad zum Anzeigen')
def show(object_hash, path_arg):
    """Zeige nur die geänderten Zeilen eines gespeicherten Objekts oder einer indizierten Datei.
    
    Nur für Textdateien. Verwende --object oder --path.
    """
    f = Forge()
    f.ensure_repo()
    index = f._get_index()

    if object_hash:
        obj_file = os.path.join(f.objects_path, object_hash)
        if not os.path.exists(obj_file):
            click.secho(f"[Forge] >> Objekt {object_hash} nicht gefunden.", fg='red')
            return
        with open(obj_file, 'rb') as fh:
            b = fh.read()
        if _is_text_bytes(b):
            click.echo(b.decode('utf-8', errors='replace'))
        else:
            click.secho("[Forge] >> Binärdaten (nicht dargestellt)", fg='yellow')
        return

    if path_arg:
        rel = f._relpath(path_arg)
        obj_hash = index.get(rel)
        if not obj_hash:
            click.secho(f"[Forge] >> {rel} nicht im Index.", fg='red')
            return
        
        # Lese die indexierte (gespeicherte) Version
        obj_file = os.path.join(f.objects_path, obj_hash)
        if not os.path.exists(obj_file):
            click.secho(f"[Forge] >> Objekt {obj_hash} nicht gefunden.", fg='red')
            return
        
        with open(obj_file, 'rb') as fh:
            indexed_content = fh.read()
        
        # Lese die aktuelle Datei
        try:
            with open(os.path.abspath(rel), 'rb') as fh:
                current_content = fh.read()
        except FileNotFoundError:
            click.secho(f"[Forge] >> Datei {rel} nicht gefunden.", fg='red')
            return
        
        # Konvertiere zu Text
        if not _is_text_bytes(indexed_content) or not _is_text_bytes(current_content):
            click.secho("[Forge] >> Binärdaten (nicht dargestellt)", fg='yellow')
            return
        
        indexed_text = indexed_content.decode('utf-8', errors='replace')
        current_text = current_content.decode('utf-8', errors='replace')
        
        # Erzeuge Diff
        indexed_lines = indexed_text.splitlines(keepends=True)
        current_lines = current_text.splitlines(keepends=True)
        
        diff = difflib.unified_diff(
            indexed_lines,
            current_lines,
            fromfile=f"{rel} (indexiert)",
            tofile=f"{rel} (aktuell)",
            lineterm=''
        )
        
        diff_output = list(diff)
        if not diff_output:
            click.secho(f"[Forge] >> Keine Unterschiede in {rel}.", fg='green')
            return
        
        # Zeige nur Diff-Zeilen (mit +/- Präfix)
        for line in diff_output:
            if line.startswith('@@'):
                click.secho(line.rstrip('\n'), fg='cyan')
            elif line.startswith('+'):
                click.secho(line.rstrip('\n'), fg='green')
            elif line.startswith('-'):
                click.secho(line.rstrip('\n'), fg='red')
            elif line.startswith('\\'):
                click.secho(line.rstrip('\n'), fg='yellow')
            else:
                click.echo(line.rstrip('\n'))
        
        return

    click.secho("[Forge] >> Bitte --object HASH oder --path DATEI angeben.", fg='yellow')
