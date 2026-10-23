import hashlib
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import profile_status
from profile_tree import tree_checksum

ENV = {**os.environ, 'GIT_AUTHOR_NAME': 't', 'GIT_AUTHOR_EMAIL': 't@example.invalid',
       'GIT_COMMITTER_NAME': 't', 'GIT_COMMITTER_EMAIL': 't@example.invalid',
       'GIT_CONFIG_GLOBAL': os.devnull, 'GIT_CONFIG_SYSTEM': os.devnull}


def git(cwd, *args):
    r = subprocess.run(['git', '-C', str(cwd), *args], capture_output=True, text=True, env=ENV)
    assert r.returncode == 0, (args, r.stderr)
    return r.stdout.strip()


class StatusTests(unittest.TestCase):
    """Real git repositories in a temp dir, read through file:// like a remote."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        (self.base / 'remote').mkdir()
        self.template = f'file://{self.base}/remote/{{repo}}.git'

    def repo(self, slug):
        """A working repo for org/name plus a bare 'remote' that it pushes to."""
        work = self.base / 'work' / slug.replace('/', '__')
        work.mkdir(parents=True)
        git(work, 'init', '-q', '-b', 'main')
        bare = self.base / 'remote' / f'{slug}.git'
        bare.parent.mkdir(parents=True, exist_ok=True)
        git(self.base, 'init', '-q', '--bare', '-b', 'main', str(bare))
        git(bare, 'config', 'uploadpack.allowFilter', 'true')
        git(bare, 'config', 'uploadpack.allowAnySHA1InWant', 'true')
        git(work, 'remote', 'add', 'origin', str(bare))
        return work

    def commit(self, work, files, msg='c', remove=()):
        for rel, text in files.items():
            p = work / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text)
        for rel in remove:
            git(work, 'rm', '-rq', rel)
        git(work, 'add', '-A')
        git(work, 'commit', '-q', '-m', msg)
        git(work, 'push', '-q', 'origin', 'HEAD:main', '--force')
        return git(work, 'rev-parse', 'HEAD')

    def entry(self, pid, slug, commit, path, files):
        listed = [{'path': rel, 'sha256': hashlib.sha256(t.encode()).hexdigest()}
                  for rel, t in files.items()]
        return {'id': pid, 'repository': slug, 'commit': commit, 'path': path,
                'checksum': tree_checksum(listed)}

    def classify(self, entries, homes=None):
        cache = self.base / 'cache'
        recs = profile_status.run(entries, cache, self.template, 2, homes)
        return {r['id']: r for r in recs}

    def test_the_four_states_and_their_reasons(self):
        soul = {'SOUL.md': 'soul v1', 'config.yaml': 'cfg'}
        pp = lambda pid: f'hermes/profiles/{pid}/'
        prof = lambda pid, files: {pp(pid) + k: v for k, v in files.items()}

        # current: nothing changed
        w = self.repo('org/same')
        c = self.commit(w, prof('a', soul))
        e_same = self.entry('a', 'org/same', c, 'hermes/profiles/a', soul)

        # current although the tree differs: a file the registry never pins was added
        w = self.repo('org/unpinned')
        c = self.commit(w, prof('b', soul))
        self.commit(w, {'hermes/profiles/b/memories/notes.md': 'private'})
        e_unpinned = self.entry('b', 'org/unpinned', c, 'hermes/profiles/b', soul)

        # behind: the pinned files changed
        w = self.repo('org/changed')
        c = self.commit(w, prof('c', soul))
        self.commit(w, prof('c', {'SOUL.md': 'soul v2'}))
        e_changed = self.entry('c', 'org/changed', c, 'hermes/profiles/c', soul)

        # behind: the profile moved to hermes/profiles/<id>
        w = self.repo('org/moved')
        c = self.commit(w, {'agents/d/SOUL.md': 'soul v1', 'agents/d/config.yaml': 'cfg'})
        self.commit(w, prof('d', soul), remove=['agents'])
        e_moved = self.entry('d', 'org/moved', c, 'agents/d', soul)

        # behind: the same profile is on the default branch, but the pinned commit
        # lives on a side branch that was never merged
        w = self.repo('org/offbranch')
        self.commit(w, prof('e', soul))
        git(w, 'checkout', '-q', '-b', 'side')
        c = self.commit(w, {'NOTES.md': 'side only'})
        git(w, 'push', '-q', 'origin', 'side')
        git(w, 'checkout', '-q', 'main')
        self.commit(w, {'README.md': 'y'})
        e_off = self.entry('e', 'org/offbranch', c, 'hermes/profiles/e', soul)

        # withdrawn: the profile is gone from the tip
        w = self.repo('org/gone')
        c = self.commit(w, prof('f', soul))
        self.commit(w, {'README.md': 'no profile now'}, remove=['hermes'])
        e_gone = self.entry('f', 'org/gone', c, 'hermes/profiles/f', soul)

        # unreachable: no such repository
        e_norepo = self.entry('g', 'org/does-not-exist', 'a' * 40, 'hermes/profiles/g', soul)

        # unreachable: the repository exists but does not contain the pinned commit
        w = self.repo('org/nocommit')
        self.commit(w, prof('h', soul))
        e_nocommit = self.entry('h', 'org/nocommit', 'b' * 40, 'hermes/profiles/h', soul)

        r = self.classify([e_same, e_unpinned, e_changed, e_moved, e_off, e_gone, e_norepo, e_nocommit])
        states = {k: v['state'] for k, v in r.items()}
        self.assertEqual({'a': 'current', 'b': 'current', 'c': 'behind', 'd': 'behind',
                          'e': 'behind', 'f': 'withdrawn', 'g': 'unreachable',
                          'h': 'unreachable'}, states)
        self.assertIn('same tree', r['a']['reason'])
        self.assertIn('outside the pin', r['b']['reason'])
        self.assertIn('differ', r['c']['reason'])
        self.assertIn('moved to hermes/profiles/d', r['d']['reason'])
        self.assertIn('not on the default branch', r['e']['reason'])
        self.assertIn('no profile at', r['f']['reason'])
        self.assertIn('not fetchable', r['g']['reason'])
        self.assertIn('not in the repository', r['h']['reason'])

    def test_a_moved_profile_with_the_same_files_is_still_behind(self):
        # The pin names a path the owner no longer uses; the registry entry is stale
        # even though the checksum would match.
        soul = {'SOUL.md': 's'}
        w = self.repo('org/mv')
        c = self.commit(w, {'old/p/SOUL.md': 's'})
        self.commit(w, {'hermes/profiles/p/SOUL.md': 's'}, remove=['old'])
        r = self.classify([self.entry('p', 'org/mv', c, 'old/p', soul)])
        self.assertEqual('behind', r['p']['state'])
        self.assertIn('same files', r['p']['reason'])

    def test_home_binding_is_reported(self):
        soul = {'SOUL.md': 's'}
        w = self.repo('org/home')
        c = self.commit(w, {'hermes/profiles/x/SOUL.md': 's'})
        e = self.entry('x', 'org/home', c, 'hermes/profiles/x', soul)
        self.assertTrue(self.classify([e], {'x': 'org/home'})['x']['homeMatches'])
        self.assertFalse(self.classify([e], {'x': 'org/elsewhere'})['x']['homeMatches'])
        self.assertIsNone(self.classify([e], {})['x']['homeMatches'])

    def test_summary_counts_every_state(self):
        recs = [{'state': s, 'reason': 'r'} for s in ('current', 'current', 'behind', 'withdrawn', 'unreachable')]
        text = profile_status.summary(recs)
        self.assertIn('current=2, behind=1, withdrawn=1, unreachable=1', text)

    def test_the_real_manifests_load(self):
        entries = profile_status.load_entries(ROOT)
        self.assertGreater(len(entries), 800)
        self.assertEqual({'id', 'repository', 'commit', 'path', 'checksum'}, set(entries[0]))


if __name__ == '__main__':
    unittest.main()
