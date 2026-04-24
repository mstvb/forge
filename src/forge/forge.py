#!/usr/bin/env python3
import os
import hashlib
import json
import click
import shutil
import difflib
from datetime import datetime

# Global quiet flag controlled by CLI
QUIET = False

def secho(message, fg=None, bold=False, err=False, force=False):
    """Wrapper around click.secho that respects the global QUIET flag.

    Set `force=True` to print even when quiet.
    """
    if QUIET and not force:
        return
    click.secho(message, fg=fg, bold=bold, err=err)


def _hash_file(data):
    """Backward-compatible: hash a text string (UTF-8). Prefer _hash_bytes."""
    if isinstance(data, bytes):
        return hashlib.sha1(data).hexdigest()
    return hashlib.sha1(str(data).encode("utf-8")).hexdigest()


def _hash_bytes(data: bytes) -> str:
    return hashlib.sha1(data).hexdigest()


def relpath(path: str) -> str:
    """Normalize a path to be relative to repo root, with forward slashes for stability."""
    p = os.path.relpath(path, start=os.getcwd())
    return p.replace("\\", "/")


def abspath(rel: str) -> str:
    return os.path.abspath(rel)


def _read_json(path: str, default):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return default


def _write_json(path: str, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=True)


class Forge:
    """
    """
    def __init__(self, base_path: str = '.forge'):
        self.base_path = base_path
        self.objects_path = os.path.join(self.base_path, "objects")
        self.commits_path = os.path.join(self.base_path, "commits")
        self.index_path = os.path.join(self.base_path, "index")
        self.head_path = os.path.join(self.base_path, "HEAD")
        self.tags_path = os.path.join(self.base_path, "tags")
        self.branches_path = os.path.join(self.base_path, "branches")

    def ensure_repo(self):
        if not os.path.exists(self.base_path):
            secho("Error: No Repository found. Create new Repository with 'forge init'.", fg='red', force=True)
            exit(1)
        # Ensure subdirectories exist for robustness
        os.makedirs(self.objects_path, exist_ok=True)
        os.makedirs(self.commits_path, exist_ok=True)
        os.makedirs(self.tags_path, exist_ok=True)
        os.makedirs(self.branches_path, exist_ok=True)

    def get_index(self):
        return _read_json(self.index_path, {})

    def save_index(self, index):
        # ensure keys normalized
        norm = {relpath(k): v for k, v in index.items()}
        _write_json(self.index_path, norm)

    def read_head(self):
        try:
            with open(self.head_path, "r", encoding="utf-8") as f:
                return f.read().strip() or None
        except FileNotFoundError:
            return None

    def write_head(self, commit_hash: str):
        with open(self.head_path, "w", encoding="utf-8") as f:
            f.write(commit_hash + "\n")

    def read_commit(self, commit_hash: str):
        path = os.path.join(self.commits_path, commit_hash)
        return _read_json(path, None)

    def write_commit(self, commit_hash: str, data: dict):
        path = os.path.join(self.commits_path, commit_hash)
        _write_json(path, data)

# --- CLI Definition mit Click ---

@click.group()
@click.option('--quiet', '-q', is_flag=True, help='suppress non-essential output')
@click.pass_context
def cli(ctx, quiet):
    """Forge - Version Control"""
    global QUIET
    QUIET = quiet
    ctx.ensure_object(dict)
    ctx.obj['quiet'] = quiet

@cli.command()
def init():
    """Initialisiert eines neuen Repository."""
    f = Forge()
    if os.path.exists(f.base_path):
        secho("[Forge] >> Repository already exists", fg="yellow", bold=True)

    else:
        for path in [f.base_path, f.objects_path, f.commits_path, f.tags_path, f.branches_path]:
            os.makedirs(path, exist_ok=True)
        # create empty HEAD and index
        with open(f.head_path, "w", encoding="utf-8") as _:
            _.write("")
        f.save_index({})
        secho("[Forge] >> Repository successfully initialized", fg="green", bold=True)

@cli.command()
@click.option('--all', 'add_all', is_flag=True, help='all data added')
@click.argument('files', nargs=-1, type=click.Path(exists=True))
def add(add_all, files):
    """Add Files to Repository (Index)."""
    f = Forge()
    f.ensure_repo()
    index = f.get_index()

    # Sammle Kandidaten
    candidates = []
    if add_all:
        for root, dirs, fnames in os.walk(os.getcwd()):
            # .forge ignorieren
            if f.base_path in root:
                continue
            # dirs filtern: .forge auslassen
            dirs[:] = [d for d in dirs if os.path.join(root, d) != os.path.abspath(f.base_path)]
            for name in fnames:
                path = os.path.join(root, name)
                if f.base_path in path:
                    continue
                candidates.append(path)
    candidates.extend(files)

    added = 0
    for path in candidates:
        if os.path.isdir(path):
            continue
        if f.base_path in os.path.abspath(path):
            continue
        try:
            with open(path, 'rb') as stream:
                content = stream.read()
        except FileNotFoundError as e:
            secho(f"[Forge] >> Cannot read {e} from {path}", fg='red')
            continue
        file_hash = _hash_bytes(content)
        obj_path = os.path.join(f.objects_path, file_hash)
        if not os.path.exists(obj_path):
            with open(obj_path, 'wb') as obj:
                obj.write(content)
        index[relpath(path)] = file_hash
        added += 1

    f.save_index(index)
    secho(f"[Forge] >> {added} Data added", fg="green", bold=True)

@cli.command()
@click.argument('message', type=str, required=True)
def commit(message):
    """Creates a Snapshot with a message."""
    f = Forge()
    f.ensure_repo()
    index = f.get_index()
    if not index:
        secho("[Forge] >> No Data for a Snapshot.", fg="red", bold=True)
        return
    parent = f.read_head()
    commit_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "message": message,
        "parent": parent,
        "files": index,
    }
    # stabile Hash-Bildung
    commit_hash = hashlib.sha1(json.dumps(commit_data, sort_keys=True).encode("utf-8")).hexdigest()
    f.write_commit(commit_hash, commit_data)
    f.write_head(commit_hash)
    secho(f"[Forge] >> Commit {commit_hash[:7]} saved.", fg="green", bold=True)

# ... (vorheriger Code bleibt gleich)

@cli.command()
def status():
    """Shows the current state: staged, changed, deleted, untracked."""
    f = Forge()
    f.ensure_repo()
    index = f.get_index()

    staged = []
    modified = []
    deleted = []
    untracked = []

    secho("--- Show Status ---", fg="green", bold=True)

    # Check indexed files against working tree
    for rel, obj_hash in index.items():
        abs_path = abspath(rel)
        if not os.path.exists(abs_path):
            deleted.append(rel)
            continue
        try:
            with open(abs_path, 'rb') as fh:
                data = fh.read()
        except FileNotFoundError:
            continue
        h = _hash_bytes(data)
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
            rel = relpath(path)
            if rel not in index:
                untracked.append(rel)

    if not any([staged, modified, deleted, untracked]):
        secho("[Forge] >> No Tasks. Directory is clean.", fg="green", bold=True)
        return

    if staged:
        secho("Staged:", fg='green', bold=True)
        for p in sorted(staged):
            secho(f"  {p}")
    if modified:
        secho("Changed:", fg='yellow', bold=True)
        for p in sorted(modified):
            secho(f"  {p}")
    if deleted:
        secho("Deleted:", fg='red', bold=True)
        for p in sorted(deleted):
            secho(f"  {p}")
    if untracked:
        secho("Untracked:", fg='blue', bold=True)
        for p in sorted(untracked):
            secho(f"  {p}")

@cli.command()
@click.argument('remote_path', type=click.Path())
def push(remote_path):
    """Share files to Remote-Repository (e.g. on a shared drive).

    Durability: all objects and commits are copied to the remote, but local repository remains unchanged."""
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
        
    secho(f"[Forge] >> Repository successfully moved to {remote_path}", fg="green", bold=True)

@cli.command()
@click.argument('remote_path', type=click.Path(exists=True))
def pull(remote_path):
    """
    Pull files from Remote-Repository (e.g. on a shared drive) to local.
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
                
    secho("[Forge] >> New Data successfully pulled.", fg="green", bold=True)


@cli.command()
def log():
    """List the Commit-History along HEAD (latest first)."""
    f = Forge()
    f.ensure_repo()
    head = f.read_head()

    chain = []
    visited = set()
    current = head
    while current and current not in visited:
        visited.add(current)
        data = f.read_commit(current)
        if not data:
            break
        chain.append((current, data))
        current = data.get('parent')

    if not chain:
        # Fallback: keine HEAD gesetzt, zeige vorhandene Commits unsortiert
        commits = os.listdir(f.commits_path) if os.path.exists(f.commits_path) else []
        if not commits:
            secho("[Forge] >> No Snapshots exist", fg="red", bold=True)
            return
        secho("--- Snapshots ---", fg="green", bold=True)
        for c_hash in sorted(commits, reverse=True):
            data = f.read_commit(c_hash)
            if not data:
                continue
            secho(f"[{c_hash[:7]}] {data.get('timestamp','?')} | {data.get('message','')}" , fg="blue", bold=True)
        return

    secho("--- Historie ---", fg="green", bold=True)
    for c_hash, data in chain:
        secho(f"[{c_hash[:7]}] {data.get('timestamp','?')} | {data.get('message','')}", fg="blue", bold=True)

@cli.command()
@click.argument('name', required=False)
@click.argument('commit', required=False)
@click.option('--delete', is_flag=True, help='Delete a Tag')
@click.option('--list', 'list_tags', is_flag=True, help='List all Tags')
def tag(name, commit, delete, list_tags):
    """Create, delete or show tags (Release-Tags).

    Without options `tag` lists all available tags. With `name` a tag is created,
    defaulting to the current HEAD.
    """
    f = Forge()
    f.ensure_repo()
    os.makedirs(f.tags_path, exist_ok=True)
    if list_tags:
        tags = sorted(os.listdir(f.tags_path))
        if not tags:
            secho("No Tags exists.", fg='yellow')
            return
        for t in tags:
            path = os.path.join(f.tags_path, t)
            try:
                with open(path, 'r', encoding='utf-8') as fh:
                    h = fh.read().strip()
            except FileNotFoundError as e:
                h = '?'
            secho(f"{t} -> {h}")
        return
    if delete:
        if not name:
            secho('Please enter Tag-Name to delete.', fg='red', bold=True)
            return
        p = os.path.join(f.tags_path, name)
        if os.path.exists(p):
            os.remove(p)
            secho(f"Tag '{name}' deleted.", fg='red', bold=True)
        else:
            secho(f"Tag '{name}' not found", fg='red', bold=True)
        return
    # create tag
    if not name:
        secho('Please enter Tag-Name', fg='green', bold=True)
        return
    target = commit or f.read_head()
    if not target:
        secho('No Commit (HEAD) exists.', fg='red', bold=True)
        return
    p = os.path.join(f.tags_path, name)
    with open(p, 'w', encoding='utf-8') as fh:
        fh.write(target + '\n')
    secho(f"Tag '{name}' to {target[:7]} set", fg='green', bold=True)

@cli.command()
@click.argument('name', required=False)
@click.option('--create', 'create', is_flag=True, help='create new branch')
@click.option('--delete', 'delete', is_flag=True, help='delete a branch')
@click.option('--checkout', 'checkout', is_flag=True, help='switch to branch')
@click.option('--list', 'list_branches', is_flag=True, help='show branches')
def branch(name, create, delete, checkout, list_branches):
    """Branch-Management: create/list/delete/checkout.

    Branches are simple pointers to commits. With `--create` a new branch is created at the current HEAD.
     `--checkout` switches HEAD to the branch. `--delete` removes a branch.
     Without options `branch` lists all available branches, marking the current one with `*`.
    """
    f = Forge()
    f.ensure_repo()
    os.makedirs(f.branches_path, exist_ok=True)
    head_branch_file = os.path.join(f.base_path, 'HEAD_BRANCH')
    if list_branches:
        branches = sorted(os.listdir(f.branches_path))
        current = None
        try:
            with open(head_branch_file, 'r', encoding='utf-8') as fh:
                current = fh.read().strip() or None
        except FileNotFoundError:
            current = None
        if not branches:
            secho('No Branches exists.', fg='red', bold=True)
            return
        for b in branches:
            mark = '*' if b == current else ' '
            p = os.path.join(f.branches_path, b)
            try:
                with open(p, 'r', encoding='utf-8') as fh:
                    h = fh.read().strip()
            except FileNotFoundError:
                h = '?'
            secho(f"{mark} {b} -> {h}")
        return
    if delete:
        if not name:
            secho('Please enter Branch-Name to delete.', fg='yellow', bold=True)
            return
        p = os.path.join(f.branches_path, name)
        if os.path.exists(p):
            os.remove(p)
            secho(f"Branch '{name}' deleted.", fg='red', bold=True)
        else:
            secho(f"Branch '{name}' not found.", fg='red', bold=True)
        return
    if create:
        if not name:
            secho('Please enter Branch-Name to create', fg='yellow', bold=True)
            return
        target = f.read_head()
        if not target:
            secho('No HEAD-Commit to commit.', fg='red')
            return
        p = os.path.join(f.branches_path, name)
        with open(p, 'w', encoding='utf-8') as fh:
            fh.write(target + '\n')
        secho(f"Branch '{name}' on {target[:7]} created", fg='green', bold=True)
        return
    if checkout:
        if not name:
            secho('Please enter Branch-Name to checkout.', fg='yellow', bold=True)
            return
        p = os.path.join(f.branches_path, name)
        if not os.path.exists(p):
            secho(f"Branch '{name}' not found.", fg='red', bold=True)
            return
        with open(p, 'r', encoding='utf-8') as fh:
            target = fh.read().strip()
        if not target:
            secho('Branch has no Commit.', fg='red', bold=True)
            return
        f.write_head(target)
        with open(head_branch_file, 'w', encoding='utf-8') as fh:
            fh.write(name + '\n')
        secho(f"Switch to Branch '{name}' ({target[:7]}).", fg='green', bold=True)
        return
    # Default: show hint
    secho('Use Actions: --list, --create, --delete, --checkout', fg='yellow')


@cli.command()
@click.option('--yes', is_flag=True, help='submit')
@click.option('--dry-run', is_flag=True, help='show deleted files')
@click.option('--backup-dir', type=click.Path(), help='optional directory to backup .forge')
def reset(yes, dry_run, backup_dir):
    """Delete Repository Data and initialize new Repository.

    Attention: All Repository-Data in .forge delete. 
    Use with --dry-run to show deleted files or --backup-dir to backup before delete.
    """
    f = Forge()
    if not os.path.exists(f.base_path):
        secho('No Repositorys found.', fg='red', bold=True)
        return

    to_remove = [f.objects_path, f.commits_path, f.index_path, f.head_path, f.tags_path, f.branches_path]

    if dry_run:
        secho('Dry run — removed paths:', fg='green', bold=True)
        for p in to_remove:
            secho(f' - {p}')
        return

    if not yes:
        if QUIET:
            secho('Aborted: use --yes, to submit the query.', fg='red')
            return
        if not click.confirm('Attention: All Repository-Data in .forge delete. Continue?'):
            secho('Aborted.', fg='yellow')
            return

    if backup_dir:
        if os.path.exists(backup_dir):
            secho(f'Backup on {backup_dir} already exists', fg='red', bold=True)
            return
        try:
            shutil.copytree(f.base_path, backup_dir)
            secho(f'Backup from {f.base_path} to {backup_dir} created', fg='green', bold=True)
        except Exception as e:
            secho(f'Error when create Backups: {e}', fg='red')
            return

    # Entferne das Repository-Verzeichnis komplett und initialisiere neu
    try:
        shutil.rmtree(f.base_path)
    except Exception as e:
        secho(f'Error when delete {f.base_path}: {e}', fg='red', bold=True)
        return

    # Neu anlegen
    os.makedirs(f.base_path, exist_ok=True)
    for path in [f.objects_path, f.commits_path, f.tags_path, f.branches_path]:
        os.makedirs(path, exist_ok=True)
    # create empty HEAD and index
    with open(f.head_path, 'w', encoding='utf-8') as _:
        _.write('')
    f.save_index({})
    secho('Repository restored and initalized', fg='green', bold=True)


@cli.command()
@click.option('--cached', is_flag=True, help='remove from Index, not from disk')
@click.argument('paths', nargs=-1, type=click.Path())
def rm(cached, paths):
    """Remove files from the index and optionally from the filesystem."""
    f = Forge()
    f.ensure_repo()
    if not paths:
        secho("[Forge] >> No Path", fg='red', bold=True)
        return
    index = f.get_index()
    removed = 0
    for p in paths:
        rel = relpath(p)
        if rel in index:
            del index[rel]
            removed += 1
            if not cached:
                abs_p = abspath(rel)
                if os.path.exists(abs_p) and os.path.isfile(abs_p):
                    try:
                        os.remove(abs_p)
                    except Exception as e:
                        secho(f"[Forge] >> Cannot {abs_p} delete {e}", fg='red', bold=True)
        else:
            secho(f"[Forge] >> {rel} not in Index.", fg='red', bold=True)
    f.save_index(index)
    secho(f"[Forge] >> {removed} Path(s) removed", fg='green', bold=True)


def _is_text_bytes(b: bytes) -> bool:
    try:
        b.decode('utf-8')
        return True
    except Exception as e:
        return False


@cli.command()
@click.option('--all', 'restore_all', is_flag=True, help='all indexed files restored')
@click.argument('paths', nargs=-1, type=click.Path())
def restore(restore_all, paths):
    """Restore files from the index (from objects)."""
    f = Forge()
    f.ensure_repo()
    index = f.get_index()

    targets = []
    if restore_all or not paths:
        targets = list(index.keys())
    else:
        for p in paths:
            rel = relpath(p)
            if rel in index:
                targets.append(rel)
            else:
                secho(f"[Forge] >> {rel} not in Index.", fg='yellow')

    restored = 0
    for rel in targets:
        obj_hash = index.get(rel)
        if not obj_hash:
            continue
        obj_file = os.path.join(f.objects_path, obj_hash)
        if not os.path.exists(obj_file):
            secho(f"[Forge] >> Object {obj_hash} not found for {rel}.", fg='red')
            continue
        abs_path = abspath(rel)
        os.makedirs(os.path.dirname(abs_path) or '.', exist_ok=True)
        with open(obj_file, 'rb') as src, open(abs_path, 'wb') as dst:
            dst.write(src.read())
        restored += 1
    secho(f"[Forge] >> {restored} Data restored", fg='green', bold=True)


@cli.command()
@click.argument('paths', nargs=-1, type=click.Path())
def diff(paths):
    """Shows differences between working directory and index."""
    f = Forge()
    f.ensure_repo()
    index = f.get_index()

    def show_diff_for(rel):
        abs_path = abspath(rel)
        obj_hash = index.get(rel)
        if obj_hash is None:
            # untracked: show as added
            if not os.path.exists(abs_path):
                return
            with open(abs_path, 'rb') as fh:
                b = fh.read()
            if not _is_text_bytes(b):
                secho(f"Binary File {rel}", fg='yellow')
                return
            text = b.decode('utf-8', errors='replace').splitlines(keepends=False)
            ud = difflib.unified_diff([], text, fromfile=f"a/{rel}", tofile=f"b/{rel}")
            click.echo('\n'.join(ud))
            return
        obj_file = os.path.join(f.objects_path, obj_hash)
        if not os.path.exists(obj_file):
            secho(f"[Forge] >> Object {obj_hash} not found for {rel}.", fg='red')
            return
        with open(obj_file, 'rb') as fh:
            ob = fh.read()
        if not os.path.exists(abs_path):
            # deleted in working tree
            if _is_text_bytes(ob):
                a = ob.decode('utf-8', errors='replace').splitlines(False)
                ud = difflib.unified_diff(a, [], fromfile=f"a/{rel}", tofile=f"b/{rel}")
                click.echo('\n'.join(ud))
            else:
                secho(f"Binary File {rel} deleted", fg='yellow')
            return
        with open(abs_path, 'rb') as fh:
            wb = fh.read()
        if not _is_text_bytes(ob) or not _is_text_bytes(wb):
            if ob != wb:
                secho(f"Binary File {rel} differs", fg='yellow')
            return
        a = ob.decode('utf-8', errors='replace').splitlines(False)
        b = wb.decode('utf-8', errors='replace').splitlines(False)
        if a == b:
            return
        ud = difflib.unified_diff(a, b, fromfile=f"a/{rel}", tofile=f"b/{rel}")
        click.echo('\n'.join(ud))

    if paths:
        rels = [relpath(p) for p in paths]
    else:
        # default: all indexed files
        rels = sorted(set(list(index.keys())))
        # plus untracked files
        for root, dirs, files in os.walk(os.getcwd()):
            if f.base_path in root:
                continue
            dirs[:] = [d for d in dirs if os.path.join(root, d) != os.path.abspath(f.base_path)]
            for name in files:
                p = os.path.join(root, name)
                if f.base_path in p:
                    continue
                rels.append(relpath(p))
        rels = sorted(set(rels))

    for rel in rels:
        show_diff_for(rel)


@cli.command()
@click.option('--object', 'object_hash', help='shows content of an object by hash')
@click.option('--path', 'path_arg', type=click.Path(), help='shows content of an object by indexed path')
def show(object_hash, path_arg):
    """Shows content of an object or an indexed path (text files)."""
    f = Forge()
    f.ensure_repo()
    index = f.get_index()

    if object_hash:
        obj_file = os.path.join(f.objects_path, object_hash)
        if not os.path.exists(obj_file):
            secho(f"[Forge] >> {object_hash} not found", fg='red')
            return None
        with open(obj_file, 'rb') as fh:
            b = fh.read()
        if _is_text_bytes(b):
            click.echo(b.decode('utf-8', errors='replace'))
        else:
            secho("[Forge] >> Binary Data", fg='yellow')
        return None

    if path_arg:
        rel = relpath(path_arg)
        obj_hash = index.get(rel)
        if not obj_hash:
            secho(f"[Forge] >> {rel} not in Index.", fg='red', bold=True)
            return None
        return show.callback(object_hash=obj_hash, path_arg=None)  # type: ignore

    secho("[Forge] >> Use --object or --path", fg='yellow')
    return None
