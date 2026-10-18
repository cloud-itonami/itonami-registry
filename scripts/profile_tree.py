"""Shared helpers for Itonami profile entries (ADR 0002)."""
import hashlib

# A profile is a Hermes profile home. Only these are registry material: the
# definitions an owner commits. Credentials, memories, sessions, logs and
# state never are (AGENTS.md), so anything else in the folder is refused.
# itonami.edn and yakuwari.edn are Itonami definitions (profile manifest and
# authority declarations, ADR 0002/0003), not state or secrets.
PROFILE_FILE_PATTERNS = ('SOUL.md', 'profile.yaml', 'config.yaml', 'cron/jobs.json',
                         'skills/', 'scripts/', 'README.md', 'itonami.edn', 'yakuwari.edn')
FORBIDDEN_NAMES = ('.env', 'auth.json', 'state.db', 'USER.md', 'MEMORY.md', 'secrets.edn',
                   'gateway_state.json')


def allowed(rel):
    name = rel.rsplit('/', 1)[-1]
    if name in FORBIDDEN_NAMES or rel.startswith(('memories/', 'sessions/', 'logs/', 'cache/')):
        return False
    return any(rel == p or (p.endswith('/') and rel.startswith(p)) for p in PROFILE_FILE_PATTERNS)


def tree_checksum(files):
    """sha256 over (path NUL sha256-hex NUL)* in path order: verifiable from
    the manifest alone, and from the files once fetched."""
    digest = hashlib.sha256()
    for f in sorted(files, key=lambda f: f['path'].split('/')):
        digest.update(f['path'].encode() + b'\0' + f['sha256'].encode() + b'\0')
    return 'sha256-tree:' + digest.hexdigest()
