# Contributing to Itonami Registry

Every entry is a pull request. CI validates it; publication grants nothing and
starts nothing (ADR 0001, ADR 0002).

## Add an Itonami profile

An Itonami profile is a Hermes profile (`SOUL.md`, `profile.yaml`, `config.yaml`,
`skills/<id>/SKILL.md`, `cron/jobs.json`, `scripts/`) committed in the repository
that owns it. Register it, do not copy it:

```bash
python scripts/add_profile.py --checkout ~/github/<org>/<repo> \
  --repository <org>/<repo> --commit <sha> --path hermes/profiles/<name>
python scripts/build_index.py && python scripts/validate.py
```

The script reads the folder from git objects at that commit, refuses credentials,
memories, sessions and state, and writes `profiles/<id>/manifest.json`,
`profiles/<id>/itonami.json` and the file hashes into `catalogs/sources.json`.
The repository must already be in `catalogs/inventory.json`.

## Add a skill, agent, MCP server or workflow

Use the Hermes registry shapes (`SKILL.md` frontmatter; `manifest.json` per
`schemas/hermes/`), add the Itonami side file `itonami.json`, pin every derivation
source in `catalogs/sources.json`, then rebuild the index.

## API entries

`apis/` and `catalogs/api-classification.json` are generated (ADR 0005). Do not edit them by hand:

```bash
python scripts/build_api_catalog.py --clones ~/github/kotoba-lang --refresh   # re-observe pins
python scripts/build_index.py && python scripts/validate.py
```

Origin domains come from the owner's record. Run `python scripts/extract_origin_domains.py --checkout <com-junkawasaki/root clone> --commit <sha>`,
then rerun the generator. Never add a domain by hand or derive one from a name.

To link an API entry to the itonami dapp that implements or consumes the shape, add an item to
`catalogs/api-relations.json` with its evidence (a pinned URL or PR), then rerun the generator
without `--refresh`.

## Federated registries

`catalogs/federated/<id>.json` snapshots another registry's index at one commit
(metadata only). Refresh it with `scripts/federate.py`; CI checks it against
upstream with `--check`.
