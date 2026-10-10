#!/usr/bin/env python3
"""Offline catalog, dependency, source and schema checks. Never invokes tools."""
import hashlib
import json
import re
from pathlib import Path
from jsonschema import Draft202012Validator
from referencing import Registry, Resource
from build_index import ROOT, entries, frontmatter


def read(path):
    return json.loads(path.read_text())


def validate(root=ROOT):
    all_files = [p for p in root.rglob('*') if '.git' not in p.parts and '__pycache__' not in p.parts]
    for p in all_files:
        if p.is_symlink():
            raise ValueError(f'Symlink refused: {p}')
        if p.is_file() and (p.name.startswith('._') or p.name == '.env' or p.suffix in ['.db', '.sqlite', '.jsonl']):
            raise ValueError(f'Runtime/secret/cache artifact refused: {p}')
    schemas = [read(p) for p in sorted((root / 'schemas/hermes').glob('*.json')) if p.name != 'provenance.json']
    registry = Registry().with_resources((s['$id'], Resource.from_contents(s)) for s in schemas)
    for schema in schemas:
        Draft202012Validator.check_schema(schema)
    schema_by_type = {k: read(root / f'schemas/hermes/{k}.schema.json') for k in ['agent', 'mcp', 'workflow']}
    ext = read(root / 'schemas/itonami.schema.json')
    Draft202012Validator.check_schema(ext)
    ext_validator = Draft202012Validator(ext)
    sources = read(root / 'catalogs/sources.json')
    ext_validator.validate(sources)
    refs = {s['id']: s for s in sources['sources']}
    if len(refs) != len(sources['sources']):
        raise ValueError('Duplicate source identity')
    for source in refs.values():
        if not re.fullmatch(r'[0-9a-f]{40}', source['commit']):
            raise ValueError('Source commit must be immutable')
        for f in source['files']:
            if not re.fullmatch(r'[0-9a-f]{64}', f['sha256']):
                raise ValueError('Source digest missing')
            if Path(f['path']).is_absolute() or '..' in Path(f['path']).parts:
                raise ValueError('Unsafe source path')
            expected = f"https://github.com/{source['repository']}/blob/{source['commit']}/{f['path']}"
            if f['url'] != expected:
                raise ValueError('Source URL differs from pinned identity')
    provenance = read(root / 'schemas/hermes/provenance.json')
    for f in provenance['files']:
        p = root / f['path']
        if hashlib.sha256(p.read_bytes()).hexdigest() != f['sha256']:
            raise ValueError(f'Vendored schema changed: {p}')
    catalog = entries(root)
    identities = {e['type'] + '/' + e['id'] for e in catalog}
    for e in catalog:
        folder = root / e['path']
        side = read(folder / 'itonami.json')
        ext_validator.validate(side)
        if any(ref not in refs for ref in side['sourceRefs']):
            raise ValueError('Unresolved source reference')
        if e['source'] not in [f"https://github.com/{refs[r]['repository']}/tree/{refs[r]['commit']}" for r in side['sourceRefs']]:
            raise ValueError('Entry source differs from provenance')
        if side['authority']['grants'] is not False or side['authority']['default'] != 'blocked':
            raise ValueError('Registry must not grant runtime authority')
        if side['validation']['live'] is not False:
            raise ValueError('Initial entries must not claim live qualification')
        if e['type'] == 'skill':
            meta = frontmatter(folder / 'SKILL.md')
            for k in ['name', 'description']:
                if not isinstance(meta.get(k), str) or not meta[k]:
                    raise ValueError('Skill identity missing')
        else:
            m = read(folder / 'manifest.json')
            Draft202012Validator(schema_by_type[e['type']], registry=registry).validate(m)
            for dep in m.get('requires', []) + [d['id'] for d in m.get('dependencies', [])]:
                if dep not in identities:
                    raise ValueError(f'Unresolved dependency: {dep}')
            if e['type'] in ['agent', 'workflow']:
                p = folder / m['entry']
                if Path(m['entry']).is_absolute() or '..' in Path(m['entry']).parts or not p.is_file():
                    raise ValueError('Entry file absent or unsafe')
            if e['type'] == 'workflow':
                ext_validator.validate(read(folder / m['entry']))
                for step in read(folder / m['entry'])['steps']:
                    if any(dep not in identities for dep in step.get('uses', [])):
                        raise ValueError('Unresolved workflow step dependency')
            if e['type'] == 'agent':
                if m.get('tools') != []:
                    raise ValueError('Initial agent scaffolds must not enable tools')
                import yaml
                config = yaml.safe_load((folder / 'templates/hermes/config.yaml').read_text())
                if config.get('toolsets') != []:
                    raise ValueError('Profile scaffold enables tools')
                for example in side.get('examples', []):
                    ext_validator.validate(read(folder / example))
        if any(dep not in identities for dep in side.get('dependsOn', [])):
            raise ValueError('Unresolved supplemental dependency')
    tools = read(root / 'catalogs/tools.json')
    ext_validator.validate(tools)
    seen = set()
    for t in tools['tools']:
        if t['id'] in seen:
            raise ValueError('Duplicate provider-qualified tool')
        seen.add(t['id'])
        p = t['provider']
        if p['sourceRef'] not in refs or p['path'] not in [f['path'] for f in refs[p['sourceRef']]['files']]:
            raise ValueError('Unresolved tool source')
        if p['kind'] == 'mcp' and p.get('entry') not in identities:
            raise ValueError('Unresolved MCP provider')
        Draft202012Validator.check_schema(t['inputSchema'])
    external = read(root / 'catalogs/external-registries.json')
    ext_validator.validate(external)
    for r in external['registries']:
        if not re.fullmatch(r'[0-9a-f]{40}', r['commit']):
            raise ValueError('External registry must be pinned')
        if identities.intersection(r['entries']):
            raise ValueError('Duplicates an externally owned entry')
    ext_validator.validate(read(root / 'docs/validation.json'))
    inventory = read(root / 'catalogs/inventory.json')
    inventory_schema = read(root / 'schemas/inventory.schema.json')
    Draft202012Validator.check_schema(inventory_schema)
    Draft202012Validator(inventory_schema).validate(inventory)
    repo_names = [r['repository'] for r in inventory['repositories']]
    if any(source['repository'] not in repo_names for source in refs.values()):
        raise ValueError('Non-public or unsurveyed registry source refused')
    if len(set(repo_names)) != len(repo_names):
        raise ValueError('Duplicate inventory repository')
    from collections import Counter
    for org in inventory['scope']:
        rows = [r for r in inventory['repositories'] if r['repository'].startswith(org + '/')]
        summary = inventory['summary'][org]
        if summary['publicRepositories'] != len(rows) or summary['totalRepositories'] != len(rows) + summary['privateRepositoriesOmitted']:
            raise ValueError('Inventory coverage count mismatch')
        if summary['scanStatus'] != dict(Counter(r['scanStatus'] for r in rows)) or summary['dispositions'] != dict(Counter(r['disposition'] for r in rows)):
            raise ValueError('Inventory disposition count mismatch')
    expected_registrations = {(refs[r]['repository'], refs[r]['commit'], e['type'] + '/' + e['id']) for e in catalog for r in read(root / e['path'] / 'itonami.json')['sourceRefs']}
    observed_registrations = {(r['repository'], e['sourceCommit'], e['entry']) for r in inventory['repositories'] for e in r['registrations']}
    if expected_registrations != observed_registrations:
        raise ValueError('Inventory registration provenance mismatch')
    reviews = read(root / 'catalogs/candidate-reviews.json')
    review_schema = read(root / 'schemas/candidate-reviews.schema.json')
    Draft202012Validator.check_schema(review_schema)
    Draft202012Validator(review_schema).validate(reviews)
    if reviews['counts'] != dict(Counter(r['decision'] for r in reviews['reviews'])):
        raise ValueError('Candidate review decision count mismatch')
    review_repos = [r['repository'] for r in reviews['reviews']]
    if len(set(review_repos)) != len(review_repos):
        raise ValueError('Duplicate candidate review owner')
    for review in reviews['reviews']:
        if review['repository'] not in repo_names:
            raise ValueError('Non-public candidate review refused')
        if review['reviewedOn'] != reviews['reviewedOn']:
            raise ValueError('Candidate review date mismatch')
        for file in review['evidence']:
            if Path(file['path']).is_absolute() or '..' in Path(file['path']).parts:
                raise ValueError('Unsafe candidate evidence path')
            expected = f"https://github.com/{review['repository']}/blob/{review['commit']}/{file['path']}"
            if file['url'] != expected:
                raise ValueError('Candidate evidence URL differs from pinned identity')
        if review['decision'] == 'registered' and not any(s['repository'] == review['repository'] and s['commit'] == review['commit'] for s in refs.values()):
            raise ValueError('Registered candidate lacks matching source provenance')
    return len(catalog), len(tools['tools'])


if __name__ == '__main__':
    count, tools = validate()
    print(f'Validated {count} entries and {tools} tool references; no execution performed')
