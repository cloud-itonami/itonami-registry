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
        self.assertEqual(validate(self.root), (6, 11))
        build(self.root, check=True)

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
        self.mutate('catalogs/tools.json', lambda v: v['tools'][-1]['provider'].update(entry='mcp/missing'))
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


if __name__ == '__main__':
    unittest.main()
