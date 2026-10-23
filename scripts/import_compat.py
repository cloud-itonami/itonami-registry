#!/usr/bin/env python3
"""Import kind=compat repositories into compat/<slug>/ (ADR 0006).

    python scripts/import_compat.py --source-root ~/github/kotoba-lang

Each tree is read from git objects at the checkout's HEAD, so uncommitted work
is never imported. .git/ and .github/ are not carried (no CI definitions);
symlinks and credential/state files are refused and recorded. The pinned
repository, commit and exclusions go to catalogs/compat-sources.json.
"""
import argparse
import io
import json
import shutil
import subprocess
import tarfile
from pathlib import Path

from profile_tree import FORBIDDEN_NAMES

ROOT = Path(__file__).resolve().parents[1]
ORG = 'kotoba-lang'
REFUSED_SUFFIXES = ('.db', '.sqlite', '.jsonl', '.pem', '.key')


def git(repo, *args):
    return subprocess.run(['git', '-C', str(repo), *args], check=True, capture_output=True).stdout


def refused(name):
    base = name.rsplit('/', 1)[-1]
    return base in FORBIDDEN_NAMES or base.startswith(('._', '.env')) or base.lower().endswith(REFUSED_SUFFIXES)


def discover(source_root):
    for repo in sorted(p for p in source_root.iterdir() if (p / 'manifest.json').is_file() and (p / '.git').exists()):
        try:
            if json.loads((repo / 'manifest.json').read_text()).get('kind') == 'compat':
                yield repo
        except ValueError:
            continue


def import_one(repo, root):
    commit = git(repo, 'rev-parse', 'HEAD').decode().strip()
    pushed = bool(git(repo, 'branch', '-r', '--contains', commit).strip())
    target = root / 'compat' / repo.name
    if target.exists():
        shutil.rmtree(target)
    skipped = {'ci': [], 'symlink': [], 'refused': []}
    with tarfile.open(fileobj=io.BytesIO(git(repo, 'archive', commit))) as tar:
        for member in tar:
            name = member.name.rstrip('/')
            if not name or name == '.':
                continue
            if name == '.github' or name.startswith('.github/'):
                skipped['ci'].append(name)
            elif member.issym() or member.islnk():
                skipped['symlink'].append(name)
            elif member.isfile() and refused(name):
                skipped['refused'].append(name)
            elif member.isdir():
                (target / name).mkdir(parents=True, exist_ok=True)
            elif member.isfile():
                dest = target / name
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(tar.extractfile(member).read())
                dest.chmod(0o755 if member.mode & 0o111 else 0o644)
    return {'slug': repo.name, 'repository': f'{ORG}/{repo.name}', 'commit': commit,
            'pushed': pushed, 'skipped': {k: sorted(v) for k, v in skipped.items() if v}}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--source-root', required=True)
    a = p.parse_args()
    rows = [import_one(r, ROOT) for r in discover(Path(a.source_root).expanduser())]
    out = {'schemaVersion': 'itonami.compat-sources.v1', 'organization': ORG, 'count': len(rows), 'sources': rows}
    (ROOT / 'catalogs/compat-sources.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
    print(f'imported {len(rows)} compat trees; unpushed commits: {sum(not r["pushed"] for r in rows)}')


if __name__ == '__main__':
    main()
