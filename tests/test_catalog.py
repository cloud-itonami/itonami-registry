import hashlib
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build_index import build, checksum
from validate import validate


class IntegrityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'registry'
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns('.git', '__pycache__', '.venv'))

    def mutate(self, path, change):
        p = self.root / path
        value = json.loads(p.read_text())
        change(value)
        p.write_text(json.dumps(value))

    def test_published_catalog(self):
        self.assertEqual(validate(self.root), (46, 19))
        build(self.root, check=True)

    def test_nonpublic_source_refused(self):
        def change(v):
            source = v['sources'][-1]
            source['repository'] = 'kotoba-lang/not-in-public-survey'
            for f in source['files']:
                f['url'] = "https://github.com/" + source['repository'] + "/blob/" + source['commit'] + "/" + f['path']
            # This unused provenance still must not expose a private source.
            source['id'] = 'unused-source'
        # Add an unused source, so reference resolution still passes first.
        def append(v):
            import copy
            temporary = {'sources': [copy.deepcopy(v['sources'][0])]}
            change(temporary)
            v['sources'].append(temporary['sources'][0])
        self.mutate('catalogs/sources.json', append)
        with self.assertRaisesRegex(ValueError, 'Non-public'):
            validate(self.root)

    def test_targeted_source_cannot_claim_private_visibility(self):
        self.mutate('catalogs/targeted-public-sources.json', lambda v: v['sources'][0].update(visibility='private'))
        with self.assertRaises(Exception):
            validate(self.root)

    def test_targeted_source_must_pin_registered_owner(self):
        self.mutate('catalogs/targeted-public-sources.json', lambda v: v['sources'][0].update(commit='0'*40))
        with self.assertRaisesRegex(ValueError, 'matching pinned'):
            validate(self.root)

    def test_targeted_registration_must_match_entry_provenance(self):
        self.mutate('catalogs/targeted-public-sources.json', lambda v: v['sources'][0]['registrations'][0].update(sourceCommit='0'*40))
        with self.assertRaisesRegex(ValueError, 'registration provenance'):
            validate(self.root)

    def test_candidate_review_count_mismatch_fails(self):
        self.mutate('catalogs/candidate-reviews.json', lambda v: v['counts'].update(registered=0))
        with self.assertRaisesRegex(ValueError, 'Candidate review decision count'):
            validate(self.root)

    def test_candidate_evidence_cannot_use_mutable_url(self):
        self.mutate('catalogs/candidate-reviews.json', lambda v: v['reviews'][0]['evidence'][0].update(url='https://example.invalid/main'))
        with self.assertRaisesRegex(ValueError, 'Candidate evidence URL'):
            validate(self.root)

    def test_inventory_count_mismatch_fails(self):
        self.mutate('catalogs/inventory.json', lambda v: v['summary']['kotoba-lang'].update(publicRepositories=0))
        with self.assertRaisesRegex(ValueError, 'Inventory coverage'):
            validate(self.root)

    def test_inventory_registration_provenance_fails(self):
        def change(v):
            row = next(r for r in v['repositories'] if r['registrations'])
            row['registrations'][0]['sourceCommit'] = '0' * 40
        self.mutate('catalogs/inventory.json', change)
        with self.assertRaisesRegex(ValueError, 'Inventory registration provenance'):
            validate(self.root)

    def test_checksum_matches_hermes_vectors(self):
        folder = Path(self.temp.name) / 'vector'
        folder.mkdir()
        (folder / 'b').write_bytes(b'two')
        (folder / 'a').write_bytes(b'one')
        self.assertEqual(checksum(folder), 'sha256:' + hashlib.sha256(b'a\0one\0b\0two\0').hexdigest())

    def test_changed_artifact_invalidates_index(self):
        (self.root / 'agents/fleet-health-auditor/AGENT.md').write_text('Changed prompt')
        with self.assertRaisesRegex(ValueError, 'Stale index'):
            build(self.root, check=True)

    def test_unresolved_workflow_dependency_fails(self):
        self.mutate('workflows/fleet-health-review/manifest.json', lambda v: v['requires'].append('agent/missing'))
        with self.assertRaisesRegex(ValueError, 'Unresolved dependency'):
            validate(self.root)

    def test_missing_tool_provider_fails(self):
        self.mutate('catalogs/tools.json', lambda v: next(t for t in v['tools'] if t['provider']['kind'] == 'mcp')['provider'].update(entry='mcp/missing'))
        with self.assertRaisesRegex(ValueError, 'Unresolved MCP provider'):
            validate(self.root)

    def test_source_commit_must_be_immutable(self):
        self.mutate('catalogs/sources.json', lambda v: v['sources'][0].update(commit='main'))
        with self.assertRaises(ValueError):
            validate(self.root)

    def test_schemas_cannot_drift_from_provenance(self):
        p = self.root / 'schemas/hermes/agent.schema.json'
        p.write_text(p.read_text() + '\n')
        with self.assertRaisesRegex(ValueError, 'Vendored schema changed'):
            validate(self.root)

    def test_registry_cannot_grant_authority(self):
        self.mutate('agents/fleet-health-auditor/itonami.json', lambda v: v['authority'].update(grants=True))
        with self.assertRaises(Exception):
            validate(self.root)

    def test_duplicate_external_entry_fails(self):
        self.mutate('catalogs/external-registries.json', lambda v: v['registries'][0]['entries'].append('agent/fleet-health-auditor'))
        with self.assertRaisesRegex(ValueError, 'Duplicates an externally owned entry'):
            validate(self.root)

    def test_symlinks_cannot_escape_entry_folder(self):
        (self.root / 'agents/fleet-health-auditor/escape').symlink_to(self.root / 'README.md')
        with self.assertRaisesRegex(ValueError, 'Symlinks'):
            build(self.root, check=True)

    # ADR 0002: Itonami profiles are pinned references, never copies.
    def test_profile_files_are_never_copied(self):
        (self.root / 'profiles/itonami-eng/SOUL.md').write_text('# copied\n')
        with self.assertRaisesRegex(ValueError, 'must not copy profile files'):
            validate(self.root)

    def test_profile_tree_checksum_is_checked(self):
        self.mutate('profiles/itonami-eng/manifest.json',
                    lambda v: v['profile']['files'][0].update(sha256='0' * 64))
        with self.assertRaisesRegex(ValueError, 'tree checksum'):
            validate(self.root)

    def test_profile_cannot_carry_owner_memory(self):
        def change(v):
            v['profile']['files'].append({'path': 'MEMORY.md', 'sha256': '0' * 64, 'bytes': 1})
        self.mutate('profiles/itonami-eng/manifest.json', change)
        with self.assertRaisesRegex(ValueError, 'Not a registry profile file'):
            validate(self.root)

    def test_profile_files_must_be_pinned_in_sources(self):
        from profile_tree import tree_checksum

        def change(v):
            v['profile']['files'][0]['sha256'] = '1' * 64
            v['profile']['checksum'] = tree_checksum(v['profile']['files'])
        self.mutate('profiles/itonami-eng/manifest.json', change)
        with self.assertRaisesRegex(ValueError, 'not pinned'):
            validate(self.root)

    def test_categories_and_models_follow_the_hermes_shape(self):
        categories = json.loads((self.root / 'categories.json').read_text())
        self.assertIn('profile', [t['type'] for t in categories['types']])
        models = json.loads((self.root / 'models.json').read_text())
        self.assertEqual(['murakumo'], [p['id'] for p in models['providers']])


class ProfileFilePolicyTests(unittest.TestCase):
    def test_itonami_definition_files_allowed(self):
        from profile_tree import allowed
        for rel in ['SOUL.md', 'profile.yaml', 'config.yaml', 'cron/jobs.json',
                    'skills/itonami-x/SKILL.md', 'scripts/run.py', 'README.md',
                    'itonami.edn', 'yakuwari.edn']:
            self.assertTrue(allowed(rel), rel)

    def test_secret_and_state_files_refused(self):
        from profile_tree import allowed
        for rel in ['.env', 'auth.json', 'secrets.edn', 'MEMORY.md', 'USER.md',
                    'state.db', 'gateway_state.json', 'workspace/x.json',
                    'memories/note.md', 'sessions/run.json', 'logs/run.log',
                    'cache/x', 'cron/executions.db', 'cron/itonami-runs.jsonl']:
            self.assertFalse(allowed(rel), rel)


if __name__ == '__main__':
    unittest.main()
