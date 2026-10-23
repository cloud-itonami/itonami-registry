#!/usr/bin/env python3
"""Write catalogs/origin-domains.json: the public extract of the origin-domain record (ADR 0005 §4).

    extract_origin_domains.py --checkout DIR [--commit SHA] [--check]

The source record (`manifest/origin-domains.edn` in com-junkawasaki/root, a private repository; its
authority is the sibling `origin-domains.kotoba`, of which the .edn is a verified complete view) maps
repositories to the domain their authority actually uses. Only repository -> domain facts are
extracted, and only for repositories that are api entries in this registry (apis/<id>/). Everything
else in the record (coverage measurements, sweeps, unresolvable notes, migrations) stays private.

The files are read from the pinned commit object with git, never from a working tree. Their sha256 is
recorded, so the extract can be re-derived and checked by anyone holding the source commit.
"""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = 'catalogs/origin-domains.json'
SOURCE_REPO = 'com-junkawasaki/root'
VIEW = 'manifest/origin-domains.edn'
AUTHORITY = 'manifest/origin-domains.kotoba'
ORG = 'kotoba-lang'
DOMAIN = re.compile(r'^[a-z0-9]([a-z0-9-]*[a-z0-9])?(\.[a-z0-9]([a-z0-9-]*[a-z0-9])?)+$')


def git_show(checkout, commit, path):
    r = subprocess.run(['git', '-C', str(checkout), 'show', f'{commit}:{path}'], capture_output=True)
    if r.returncode != 0:
        sys.exit(f'{path} not readable at {commit}')
    return r.stdout


def edn_string_map(text, key):
    """The flat {"string" "string"} map under `key` (the record's :anchors / :domains)."""
    m = re.search(re.escape(key) + r'\s*\{([^{}]*)\}', text)
    if not m:
        sys.exit(f'{key} not found in the record')
    body = re.sub(r';[^\n]*', '', m.group(1))
    pairs = re.findall(r'"([^"\\]+)"\s+"([^"\\]+)"', body)
    leftover = re.sub(r'"([^"\\]+)"\s+"([^"\\]+)"', '', body).strip()
    if leftover:
        sys.exit(f'{key} is not a flat string map; refusing to guess')
    return pairs


def edn_scalar(text, key):
    m = re.search(r'^  ' + re.escape(key) + r'\s+(?::([a-z-]+)|"([^"]*)")', text, re.M)  # top level only
    return (m.group(1) or m.group(2)) if m else None


def reverse(domain):
    return '.'.join(reversed(domain.split('.')))


def build(root, checkout, commit):
    view = git_show(checkout, commit, VIEW)
    authority = git_show(checkout, commit, AUTHORITY)
    text = view.decode()
    apis = {p.name for p in (root / 'apis').iterdir() if (p / 'manifest.json').exists()}
    facts = {}
    for section in (':anchors', ':domains'):
        for repo, domain in edn_string_map(text, section):
            if not repo.startswith(ORG + '/') or repo.split('/', 1)[1] not in apis:
                continue
            if not DOMAIN.fullmatch(domain):
                sys.exit(f'Not a registrable domain in the record: {repo} {domain}')
            if repo in facts and facts[repo] != domain:
                sys.exit(f'The record disagrees with itself: {repo}')
            if f'"{repo}"' not in authority.decode():
                sys.exit(f'{repo} is in the .edn view but not in its .kotoba authority')
            facts[repo] = domain
    entries = []
    for repo, domain in sorted(facts.items()):
        rid = repo.split('/', 1)[1]
        rev = reverse(domain)
        entries.append({'api': rid, 'repository': repo, 'domain': domain, 'reverseDomain': rev,
                        'nameMatchesDomain': rid == rev.replace('.', '-') or rid.startswith(rev.replace('.', '-') + '-')})
    return {
        'schemaVersion': 'itonami.origin-domains.v1',
        'note': ('Public extract of the origin-domain record: for api entries only, the registrable domain '
                 'the authority behind a repository actually uses. The record is the owner\'s; it was '
                 'checked for NS delegation, but the binding of each repository to its authority is the '
                 'owner\'s assertion, not a measurement. Absence here means unrecorded, not wrong.'),
        'source': {'repository': SOURCE_REPO, 'visibility': 'private', 'commit': commit,
                   'files': [{'path': VIEW, 'sha256': hashlib.sha256(view).hexdigest(), 'role': 'view'},
                             {'path': AUTHORITY, 'sha256': hashlib.sha256(authority).hexdigest(), 'role': 'authority'}],
                   'schema': edn_scalar(text, ':schema'),
                   'recordDnsCheckedAt': edn_scalar(text, ':dns-checked-at'),
                   'authorityBindingEvidence': edn_scalar(text, ':authority-binding-evidence'),
                   'extracted': 'repository -> domain pairs from :anchors and :domains whose repository is an api entry; nothing else'},
        'count': len(entries),
        'entries': entries,
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description='Extract catalogs/origin-domains.json (ADR 0005)')
    ap.add_argument('--checkout', type=Path, required=True, help='a local clone of com-junkawasaki/root')
    ap.add_argument('--commit', help='source commit (default: the commit recorded in the extract, else the checkout HEAD)')
    ap.add_argument('--root', type=Path, default=ROOT)
    ap.add_argument('--check', action='store_true')
    a = ap.parse_args(argv)
    path = a.root / OUT
    commit = a.commit
    if not commit and path.exists():
        commit = json.loads(path.read_text())['source']['commit']
    if not commit:
        commit = subprocess.run(['git', '-C', str(a.checkout), 'rev-parse', 'HEAD'], capture_output=True, text=True, check=True).stdout.strip()
    text = json.dumps(build(a.root, a.checkout, commit), ensure_ascii=False, indent=2) + '\n'
    if a.check:
        if not path.exists() or path.read_text() != text:
            sys.exit(f'{OUT} is stale; run scripts/extract_origin_domains.py')
    else:
        path.write_text(text)
    print(f"{'Verified' if a.check else 'Wrote'} {OUT} at {SOURCE_REPO}@{commit[:12]}: {json.loads(text)['count']} api origins")


if __name__ == '__main__':
    main()
