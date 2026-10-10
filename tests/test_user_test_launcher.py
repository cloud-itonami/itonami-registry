"""Exercise fail-closed checkout binding without starting kbb or MCP."""
import importlib.util
import json
import os
import sys
sys.dont_write_bytecode = True
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('user_test_launcher',ROOT/'mcp/user-test/launch.py')
launcher=importlib.util.module_from_spec(spec)
spec.loader.exec_module(launcher)

class LauncherTests(unittest.TestCase):
    def test_relative_target_refused(self):
        with self.assertRaisesRegex(ValueError,'Absolute'):
            launcher.resolve(Path('relative'))

    def test_wrong_commit_refused_before_runtime_resolution(self):
        with tempfile.TemporaryDirectory() as tmp:
            target=Path(tmp)
            subprocess.run(['git','init','-q',str(target)],check=True)
            subprocess.run(['git','-C',str(target),'-c','user.name=Registry test','-c','user.email=test@example.invalid','commit','--allow-empty','-qm','fixture'],check=True)
            with self.assertRaisesRegex(ValueError,'revision differs'):
                launcher.resolve(target)

    def test_dirty_pinned_checkout_refused(self):
        # Simulated git responses prove the dirty branch stops before exec/path lookup.
        expected=json.loads((ROOT/'mcp/user-test/manifest.json').read_text())['source'].rsplit('/',1)[1]
        with tempfile.TemporaryDirectory() as tmp, patch.object(launcher.subprocess,'check_output',side_effect=[expected+'\n','?? unrelated-WIP\n']), patch.object(launcher.shutil,'which') as which:
            with self.assertRaisesRegex(ValueError,'Dirty'):
                launcher.resolve(Path(tmp))
            which.assert_not_called()

if __name__=='__main__':unittest.main()
