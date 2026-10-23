#!/usr/bin/env python3
"""Generate compat/index.json from compat/<slug>/ and catalogs/compat-sources.json (ADR 0005)."""
import argparse
import json

from build_index import ROOT, checksum


def entries(root=ROOT):
    sources = json.loads((root / 'catalogs/compat-sources.json').read_text())['sources']
    result = []
    for src in sources:
        folder = root / 'compat' / src['slug']
        m = json.loads((folder / 'manifest.json').read_text())
        verified = m.get('verified') or {}
        result.append({
            'id': src['slug'], 'type': 'compat', 'name': m.get('title', src['slug']),
            'handle': m.get('handle'), 'description': m.get('description', ''),
            'tier': m.get('tier'), 'runtime': m.get('runtime'), 'wasmCid': m.get('wasmCid'),
            'verifiedSource': verified.get('source'), 'verifiedAt': verified.get('verifiedAt'),
            'source': f"https://github.com/{src['repository']}/tree/{src['commit']}",
            'path': f"compat/{src['slug']}", 'checksum': checksum(folder),
        })
    result.sort(key=lambda e: e['id'])
    return result


def build(root=ROOT, check=False):
    catalog = entries(root)
    target = root / 'compat/index.json'
    value = {'schemaVersion': '1', 'count': len(catalog), 'entries': catalog}
    text = json.dumps(value, ensure_ascii=False, indent=2) + '\n'
    if check:
        if not target.exists() or target.read_text() != text:
            raise ValueError('Stale compat index; run python scripts/build_compat_index.py')
    else:
        target.write_text(text)
    return len(catalog)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--check', action='store_true')
    a = p.parse_args()
    print(f"{'Verified' if a.check else 'Indexed'} {build(check=a.check)} compat entries")
