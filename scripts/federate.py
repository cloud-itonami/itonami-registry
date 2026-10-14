#!/usr/bin/env python3
"""Snapshot a federated registry's index at one commit (ADR 0002).

    python scripts/federate.py --checkout ~/github/fathah/hermes-registry \
        --id hermes-registry --repository fathah/hermes-registry [--commit <sha>] [--check]

Writes catalogs/federated/<id>.json: the upstream index entries (metadata
only, with their upstream checksums) under registry-qualified identities
`<id>/<type>/<entry id>`, plus the sha256 of the upstream index.json at that
commit. No upstream entry files are copied; a consumer resolves each entry's
folder in that registry at the pinned commit and verifies its checksum there.
"""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KEEP = ['id', 'type', 'name', 'version', 'description', 'author', 'license', 'tags',
        'category', 'source', 'compatibility', 'path', 'checksum', 'icon']


def git(checkout, *args):
    return subprocess.run(['git', '-C', str(checkout), *args], check=True, capture_output=True).stdout


def snapshot(checkout, registry_id, repository, commit_ref):
    commit = git(checkout, 'rev-parse', commit_ref + '^{commit}').decode().strip()
    raw = git(checkout, 'show', f'{commit}:index.json')
    index = json.loads(raw)
    entries = index['entries'] if isinstance(index, dict) else index
    rows = []
    for e in sorted(entries, key=lambda e: (e['type'], e['id'])):
        row = {k: e[k] for k in KEEP if e.get(k) is not None}
        row['qualifiedId'] = f"{registry_id}/{e['type']}/{e['id']}"
        rows.append(row)
    return {
        'schemaVersion': 'itonami.federated-index.v1',
        'registry': {'id': registry_id, 'repository': repository, 'commit': commit,
                     'index': f'https://raw.githubusercontent.com/{repository}/{commit}/index.json',
                     'indexSha256': hashlib.sha256(raw).hexdigest(),
                     'license': 'MIT (upstream)', 'copied': 'metadata only'},
        'count': len(rows),
        'entries': rows,
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--checkout', required=True)
    p.add_argument('--id', required=True)
    p.add_argument('--repository', required=True)
    p.add_argument('--commit', default='origin/HEAD')
    p.add_argument('--check', action='store_true')
    a = p.parse_args()
    target = ROOT / 'catalogs/federated' / f'{a.id}.json'
    if a.check:
        prior = json.loads(target.read_text())
        a.commit = prior['registry']['commit']
    value = snapshot(Path(a.checkout).expanduser(), a.id, a.repository, a.commit)
    text = json.dumps(value, ensure_ascii=False, indent=2) + '\n'
    if a.check:
        if target.read_text() != text:
            raise SystemExit(f'{target} differs from {a.repository} at {a.commit}')
        print(f'{target.name} matches {a.repository}@{a.commit[:7]}')
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text)
    print(f"federated {value['count']} entries from {a.repository}@{value['registry']['commit'][:7]}")


if __name__ == '__main__':
    main()
