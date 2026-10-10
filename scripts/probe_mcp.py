#!/usr/bin/env python3
"""Probe pinned MCP discovery only; no valid tools/call is sent."""
import argparse
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--checkout', required=True, type=Path, help='Existing kotoba-lang/murakumo checkout; only git show reads are used')
    args = parser.parse_args()
    source = next(s for s in json.loads((ROOT / 'catalogs/sources.json').read_text())['sources'] if s['id'] == 'web')
    file = next(f for f in source['files'] if f['path'] == 'scripts/web_mcp.mjs')
    script = subprocess.check_output(['git', '-C', str(args.checkout), 'show', f"{source['commit']}:{file['path']}"], timeout=10)
    if hashlib.sha256(script).hexdigest() != file['sha256']:
        raise ValueError('Pinned MCP source digest mismatch')
    messages = [
        {'jsonrpc': '2.0', 'id': 1, 'method': 'initialize', 'params': {'protocolVersion': '2024-11-05', 'capabilities': {}, 'clientInfo': {'name': 'itonami-registry-probe', 'version': '0.1.0'}}},
        {'jsonrpc': '2.0', 'method': 'notifications/initialized'},
        {'jsonrpc': '2.0', 'id': 2, 'method': 'tools/list'},
        {'jsonrpc': '2.0', 'id': 3, 'method': 'ping'},
        {'jsonrpc': '2.0', 'id': 4, 'method': 'tools/call', 'params': {'name': 'nonexistent', 'arguments': {}}},
        {'jsonrpc': '2.0', 'id': 5, 'method': 'tools/call', 'params': {'name': 'web_fetch', 'arguments': {}}},
    ]
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / 'web_mcp.mjs'
        path.write_bytes(script)
        output = subprocess.run(['node', str(path)], input=''.join(json.dumps(m) + '\n' for m in messages), capture_output=True, text=True, timeout=10, check=True)
    replies = {m['id']: m for m in map(json.loads, output.stdout.splitlines())}
    assert len(replies) == 5 and replies[1]['result']['serverInfo']['name'] == 'murakumo-web'
    assert replies[1]['result']['protocolVersion'] == '2024-11-05'
    assert replies[3]['result'] == {} and replies[4]['error']['code'] == -32602
    assert replies[5]['result']['isError'] is True
    expected = {t['name']: t for t in json.loads((ROOT / 'catalogs/tools.json').read_text())['tools'] if t['provider'].get('entry') == 'mcp/murakumo-web'}
    observed = {t['name']: t for t in replies[2]['result']['tools']}
    assert expected.keys() == observed.keys()
    for name, descriptor in observed.items():
        assert expected[name]['inputSchema'] == descriptor['inputSchema']
        assert expected[name]['description'] == descriptor['description']
    print(f'Pinned MCP initialization, notifications, ping, refusal and {len(observed)} tool descriptors passed; zero live calls')
