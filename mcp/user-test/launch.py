#!/usr/bin/env python3
"""Fail closed before launching the separately installed owner runtime."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess

def resolve(checkout):
    if not checkout.is_absolute() or not checkout.is_dir():
        raise ValueError('Absolute existing owner checkout required')
    manifest = json.loads((Path(__file__).parent/'manifest.json').read_text())
    expected = manifest['source'].rsplit('/',1)[1]
    observed = subprocess.check_output(['git','-C',str(checkout),'rev-parse','HEAD'],text=True,timeout=10).strip()
    if observed != expected:
        raise ValueError('Owner checkout revision differs from pinned source')
    dirty = subprocess.check_output(['git','-C',str(checkout),'status','--porcelain','--untracked-files=all'],text=True,timeout=10)
    if dirty.strip():
        raise ValueError('Dirty owner checkout refused; preserve WIP and use a separate clean checkout')
    command = shutil.which('kbb')
    if not command:
        raise ValueError('Separately installed JVM-capable kbb required')
    return command

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--checkout',type=Path,required=True)
    args=parser.parse_args()
    try:
        command=resolve(args.checkout)
    except (ValueError,subprocess.SubprocessError) as error:
        parser.exit(2, str(error)+'\n')
    os.chdir(args.checkout)
    os.execv(command,[command,'-M:mcp'])
