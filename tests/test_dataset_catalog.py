import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build_dataset_catalog import FAMILIES, edn_string
from validate import validate_datasets


class DatasetCatalogTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copytree(ROOT / 'catalogs/datasets', self.root / 'catalogs/datasets')
        (self.root / 'schemas').mkdir()
        shutil.copy(ROOT / 'schemas/dataset-sources.schema.json', self.root / 'schemas')

    def mutate(self, family, change):
        p = self.root / 'catalogs/datasets' / f'{family}.json'
        doc = json.loads(p.read_text())
        change(doc)
        p.write_text(json.dumps(doc))

    def refused(self, family, change):
        self.mutate(family, change)
        with self.assertRaises(Exception):
            validate_datasets(self.root)

    def test_published_catalogs(self):
        validate_datasets(self.root)

    def test_unpinned_commit_refused(self):
        self.refused('lei', lambda d: d['entries'][0].update(commit='main'))

    def test_nonpublic_refused(self):
        self.refused('assoc', lambda d: d['entries'][0].update(visibility='private'))

    def test_verified_without_digest_refused(self):
        def change(d):
            d['entries'][0]['payload'] = []
            d['entries'][0]['digestStatus'] = 'verified'
        self.refused('municipality', change)

    def test_digest_without_status_refused(self):
        def change(d):
            e = next(x for x in d['entries'] if x['digestStatus'] == 'verified')
            e['digestStatus'] = 'unverified'
        self.refused('lei', change)

    def test_duplicate_id_refused(self):
        def change(d):
            d['entries'].append(dict(d['entries'][0]))
            d['count'] += 1
        self.refused('assoc', change)

    def test_entry_in_wrong_family_refused(self):
        self.refused('lei', lambda d: d['entries'][0].update(id='assoc/' + d['entries'][0]['id'].split('/')[1]))

    def test_secret_like_payload_path_refused(self):
        self.refused('lei', lambda d: d['entries'][0]['payload'].append({'path': '../secrets.edn', 'sha256': '0' * 64}))

    def test_count_mismatch_refused(self):
        self.refused('municipality', lambda d: d.update(count=d['count'] + 1))


class BuilderTests(unittest.TestCase):
    def test_edn_string(self):
        text = '{:name-en "A \\"B\\" Co" :isic "0126"}'
        self.assertEqual(edn_string(text, ':name-en'), 'A "B" Co')
        self.assertEqual(edn_string(text, ':isic'), '0126')
        self.assertIsNone(edn_string(text, ':country'))

    def test_repo_patterns(self):
        lei = FAMILIES['lei']['repo']
        self.assertTrue(lei.match('cloud-itonami-lei-2138003319y7nm75fg53'))
        self.assertFalse(lei.match('cloud-itonami-lei-corporate-tos-catalog'))
        self.assertTrue(FAMILIES['assoc']['repo'].match('cloud-itonami-assoc-6492-eu-emf'))
        self.assertFalse(FAMILIES['municipality']['repo'].match('cloud-itonami-municipality-'))


if __name__ == '__main__':
    unittest.main()
