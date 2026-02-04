#!/usr/bin/env python3
import os
import hashlib
import json
import click
import shutil
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

    def ensure_repo(self):
        if not os.path.exists(self.base_path):
            click.secho("Fehler: Kein Repository gefunden. Schmiede ein neues Repository mit 'forge init'.")
            exit(1)

    def _hash_file(self, data):
        return hashlib.sha1(data.encode()).hexdigest()

    def _get_index(self):
        if os.path.exists(self.index_path):
            with open(self.index_path, "r") as f: 
                return json.load(f)
        return {}

    def _save_index(self, index):
        with open(self.index_path, "w") as file:
            json.dump(index, file)

# --- CLI Definition mit Click ---

@click.group()
def cli():
    """Forge - Version Control"""
    pass

@cli.command()
def init():
    """Initialisiert eines neuen Repository."""
    f = Forge()
    if os.path.exists(f.base_path):
        click.secho("[Forge] >> Repository existiert bereits.", fg="red", bold=True)

    else:
        for path in [f.base_path, f.objects_path, f.commits_path]:
            os.makedirs(path, exist_ok=True)
        click.secho("[Forge] >> Repository erfolgreich initalisiert", fg="green", bold=True)

@cli.command()
@click.argument('files', nargs=-1, type=click.Path(exists=True))
def add(files):
    """Fügt Dateien zum Repository hinzu."""
    f = Forge()
    f.ensure_repo()
    index = f._get_index()
    for file in files:
        with open(file, "r") as stream:
            content = stream.read()
            file_hash = f._hash_file(content)
            with open(os.path.join(f.objects_path, file_hash), "w") as obj:
                obj.write(content)
            index[file] = file_hash
    f._save_index(index)
    click.secho(f"[Forge] >> {len(files)} Datei(en) hinzugefügt.", fg="green", bold=True)

@cli.command()
@click.argument('message', type=str, required=True)
def commit(message):
    """Erstellt einen Snapshot mit einer Nachricht."""
    f = Forge()
    f.ensure_repo()
    index = f._get_index()
    if not index:
        click.secho("[Forge] >> Keine Dateien für einen Snapshot.", fg="red", bold=True)
        return
    commit_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "message": message,
        "files": index
    }
    commit_hash = f._hash_file(json.dumps(commit_data))
    with open(os.path.join(f.commits_path, commit_hash), "w") as cfile:
        json.dump(commit_data, cfile, indent=4)
    click.secho(f"[Forge] >> Commit {commit_hash[:7]} gespeichert.", fg="green", bold=True)

# ... (vorheriger Code bleibt gleich)

@cli.command()
def status():
    """Zeigt den aktuellen Zustand der Schmiede."""
    f = Forge()
    f.ensure_repo()
    index = f._get_index()
    
    
    if not index:
        click.secho("[Forge] >> Repository ist leer.", fg="red", bold=True)
        return
    
    click.secho("--- Repository ---", fg="green")

    for file, f_hash in index.items():
        click.secho(f"{file} -> {f_hash[:7]}", fg="yellow")

@cli.command()
@click.argument('remote_path', type=click.Path())
def push(remote_path):
    """Überträgt alle Daten in ein Remote-Verzeichnis.

    Robustheit: überspringt fehlende lokale Ordner (z. B. wenn keine Objekte vorhanden sind)."""
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
    """
    Hole Dateien aus Remote-Repository
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
    """
    Setze Repository auf Snapshot mit bestimmter Nachricht zurück.
    """
    f = Forge()
    f.ensure_repo()

    matches = []
    for c_hash in os.listdir(f.commits_path):
        with open(os.path.join(f.commits_path, c_hash), "r") as cfile:
            data = json.load(cfile)
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
    for file_path, obj_hash in chosen_data.get('files', {}).items():
        obj_file = os.path.join(f.objects_path, obj_hash)
        if not os.path.exists(obj_file):
            click.secho(f"[Forge] >> Objekt {obj_hash} für {file_path} fehlt.", fg="red")
            continue
        dir_name = os.path.dirname(file_path)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)
        with open(obj_file, "r") as o, open(file_path, "w") as out:
            out.write(o.read())

    # Index aktualisieren
    f._save_index(chosen_data.get('files', {}))
    click.secho(f"[Forge] >> Repository auf Snapshot {chosen_hash[:7]} ('{chosen_data.get('message', '')}') zurückgesetzt.", fg="green", bold=True)

@cli.command()
def log():
    """Listet alle bisherigen Snapshots auf."""
    f = Forge()
    f.ensure_repo()
    commits = os.listdir(f.commits_path)
    if not commits:
        click.secho("[Forge] >> Keine Snapshots vorhanden.", fg="red", bold=True)
        return

    click.secho("--- Snapshots ---", fg="green")
    for c_hash in sorted(commits, reverse=True): # Sortierung nach Name/Zeit-Sim
        with open(os.path.join(f.commits_path, c_hash), "r") as cfile:
            data = json.load(cfile)
            click.secho(f"[{c_hash[:7]}] {data['timestamp']} | {data['message']}", fg="blue", bold=True)
    
    click.secho("--- xxx ---", fg="green")

if __name__ == "__main__":
    cli()