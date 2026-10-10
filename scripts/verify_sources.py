#!/usr/bin/env python3
"""Read immutable GitHub files and compare provenance; requires authenticated gh."""
import base64
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def fetch(repository, commit, path):
    response = json.loads(subprocess.check_output(
        ['gh', 'api', f'repos/{repository}/contents/{path}?ref={commit}'], timeout=30))
    if response.get('encoding') != 'base64':
        raise ValueError(f'Unsupported source encoding: {path}')
    return base64.b64decode(response['content'])


if __name__ == '__main__':
    sources = json.loads((ROOT / 'catalogs/sources.json').read_text())['sources']
    checked = 0
    for source in sources:
        for file in source['files']:
            data = fetch(source['repository'], source['commit'], file['path'])
            if hashlib.sha256(data).hexdigest() != file['sha256']:
                raise ValueError(f"Source mismatch: {source['id']}/{file['path']}")
            checked += 1
    provenance = json.loads((ROOT / 'schemas/hermes/provenance.json').read_text())
    for file in provenance['files']:
        data = fetch(provenance['repository'], provenance['commit'], file['upstreamPath'])
        if hashlib.sha256(data).hexdigest() != file['sha256']:
            raise ValueError(f"Upstream schema mismatch: {file['path']}")
    local = json.loads((ROOT / 'index.json').read_text())['entries']
    identities = {e['type'] + '/' + e['id'] for e in local}
    for registry in json.loads((ROOT / 'catalogs/external-registries.json').read_text())['registries']:
        upstream = json.loads(fetch(registry['repository'], registry['commit'], 'index.json'))
        upstream_ids = {e['type'] + '/' + e['id'] for e in upstream['entries']}
        if identities & upstream_ids:
            raise ValueError('Local catalog duplicates external entries')
        if not set(registry['entries']) <= upstream_ids:
            raise ValueError('External entry reference does not resolve')
    print(f'GitHub readback verified {checked} source files, {len(provenance["files"])} schemas and external references')
