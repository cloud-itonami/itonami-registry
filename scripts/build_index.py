#!/usr/bin/env python3
"""Generate the Hermes discovery index from reviewed entry folders."""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]


def checksum(folder):
    digest = hashlib.sha256()
    paths = sorted(folder.rglob('*'))
    if any(p.is_symlink() for p in paths):
        raise ValueError(f'Symlinks are not registry artifacts: {folder}')
    for path in paths:
        if path.is_file():
            digest.update(path.relative_to(folder).as_posix().encode())
            digest.update(b'\0')
            digest.update(path.read_bytes())
            digest.update(b'\0')
    return 'sha256:' + digest.hexdigest()


def frontmatter(path):
    text = path.read_text()
    if not text.startswith('---\n'):
        raise ValueError(f'Missing skill frontmatter: {path}')
    parts = text.split('---', 2)
    if len(parts) != 3:
        raise ValueError(f'Unterminated skill frontmatter: {path}')
    value = yaml.safe_load(parts[1])
    if not isinstance(value, dict):
        raise ValueError(f'Invalid skill metadata: {path}')
    return value


def entries(root=ROOT):
    result = []
    for file in sorted((root / 'skills').glob('*/*/SKILL.md')):
        meta = frontmatter(file)
        h = meta['metadata']['hermes']
        entry = {k: h[k] for k in ['version', 'author', 'source', 'compatibility']}
        entry.update(id=meta['name'], type='skill', name=meta['name'],
                     description=meta['description'], category=file.parent.parent.name)
        if entry['id'] != file.parent.name:
            raise ValueError(f'Skill folder differs from identity: {file}')
        entry.update(path=file.parent.relative_to(root).as_posix(), checksum=checksum(file.parent))
        result.append(entry)
    for kind, directory in [('mcp', 'mcp'), ('agent', 'agents'), ('workflow', 'workflows')]:
        for file in sorted((root / directory).glob('*/manifest.json')):
            meta = json.loads(file.read_text())
            if meta['type'] != kind or meta['id'] != file.parent.name:
                raise ValueError(f'Manifest type or folder differs from identity: {file}')
            entry = {key: meta[key] for key in ['id', 'type', 'name', 'version', 'description', 'author', 'source', 'compatibility']}
            for key in ['license', 'tags']:
                if key in meta:
                    entry[key] = meta[key]
            entry.update(path=file.parent.relative_to(root).as_posix(), checksum=checksum(file.parent))
            result.append(entry)
    result.sort(key=lambda e: (e['type'], e['id']))
    identities = [e['type'] + '/' + e['id'] for e in result]
    if len(set(identities)) != len(identities):
        raise ValueError('Duplicate entry identity')
    return result


def build(root=ROOT, check=False):
    target = root / 'index.json'
    prior = json.loads(target.read_text()) if target.exists() else None
    catalog = entries(root)
    if check:
        if not prior or prior.get('schemaVersion') != '1' or prior.get('count') != len(catalog) or prior.get('entries') != catalog:
            raise ValueError('Stale index; run python scripts/build_index.py')
        return prior
    generated = prior['generated'] if prior and prior.get('entries') == catalog else datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
    output = {'schemaVersion': '1', 'generated': generated, 'count': len(catalog), 'entries': catalog}
    target.write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n')
    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    print(f"{'Verified' if args.check else 'Indexed'} {build(check=args.check)['count']} entries")
