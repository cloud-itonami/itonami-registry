## Entry
- Type: profile / agent / skill / mcp / workflow
- Owner repository and pinned commit:

## Checks
- [ ] `python scripts/validate.py`
- [ ] `python scripts/build_index.py --check`
- [ ] `python -m unittest discover -s tests`
- [ ] No credentials, memories (USER.md / MEMORY.md), sessions, logs or state
- [ ] `itonami.json` grants nothing (`authority.grants: false`, `default: blocked`)
- [ ] For a profile: added with `scripts/add_profile.py` (files stay in the owning repository)
