import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build_compat_index import build
from validate import validate_compat

SLUGS = ['com-circleci', 'com-sentry']


class CompatTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'catalogs').mkdir()
        (self.root / 'compat').mkdir()
        doc = json.loads((ROOT / 'catalogs/compat-sources.json').read_text())
        doc['sources'] = [s for s in doc['sources'] if s['slug'] in SLUGS]
        doc['count'] = len(doc['sources'])
        (self.root / 'catalogs/compat-sources.json').write_text(json.dumps(doc))
        for slug in SLUGS:
            shutil.copytree(ROOT / 'compat' / slug, self.root / 'compat' / slug)
        build(self.root)

    def mutate_sources(self, change):
        p = self.root / 'catalogs/compat-sources.json'
        doc = json.loads(p.read_text())
        change(doc)
        p.write_text(json.dumps(doc))

    def test_published_compat_index(self):
        build(ROOT, check=True)

    def test_valid_subset(self):
        validate_compat(self.root)

    def test_edited_tree_makes_index_stale(self):
        with (self.root / 'compat/com-circleci/README.md').open('a') as f:
            f.write('edit')
        with self.assertRaisesRegex(ValueError, 'Stale'):
            validate_compat(self.root)

    def test_unpinned_commit_refused(self):
        self.mutate_sources(lambda d: d['sources'][0].update(commit='main'))
        with self.assertRaisesRegex(ValueError, 'immutable'):
            validate_compat(self.root)

    def test_unpushed_commit_refused(self):
        self.mutate_sources(lambda d: d['sources'][0].update(pushed=False))
        with self.assertRaisesRegex(ValueError, 'pinned public'):
            validate_compat(self.root)

    def test_ci_metadata_refused(self):
        (self.root / 'compat/com-circleci/.github').mkdir()
        with self.assertRaisesRegex(ValueError, 'CI or git'):
            validate_compat(self.root)

    def test_unlisted_folder_refused(self):
        (self.root / 'compat/com-extra').mkdir()
        with self.assertRaisesRegex(ValueError, 'differ'):
            validate_compat(self.root)


if __name__ == '__main__':
    unittest.main()
