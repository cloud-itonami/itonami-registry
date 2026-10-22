# ADR 0004 Dataset source catalogs

Status: accepted for initial publication, 2026-10-22. Builds on ADR 0001 and ADR 0002.

## Context

The cloud-itonami organization holds about 1,900 public repositories. Roughly 330 of them are
keyed data or archive repositories, one per real-world subject: `cloud-itonami-lei-<LEI>`
(public-registry facts and archived policy-text provenance), `cloud-itonami-assoc-<isic>-<iso3>-<abbr>`
(industry association rule catalogs) and `cloud-itonami-municipality-<iso3>-<name>`
(municipal ordinance catalogs). They share one shape per family and change by regeneration, not by
design. Discovering or pinning them today means listing the organization; no index records which commit
of which repository a consumer should read.

ADR 0001 forbids a fifth Hermes manifest type. A dataset is not an agent, skill, MCP, workflow or
profile, so it cannot enter `index.json`.

## Decision

1. Dataset sources are a **supplemental catalog**, like `catalogs/tools.json`: one file per family,
   `catalogs/datasets/{lei,assoc,municipality}.json`, schema `itonami.dataset-sources.v1`
   (`schemas/dataset-sources.schema.json`). They are not in `index.json` and Hermes clients do not read
   them.
2. An entry is a **reference**: owning repository, one pinned 40-hex commit, SPDX license as reported
   by GitHub, subject keys (LEI, ISIC, country) and `sha256` of a fixed per-family file list read from the
   pinned commit. No repository content is copied into the registry. Entries are public and
   `repository-owned`; the owning repository keeps ownership, license and history.
3. `digestStatus` is honest. `verified` means every listed digest was computed from the pinned commit
   object. `unverified` means the commit object was not available to the builder (for example the
   repository was not cloned); such an entry has no digests, and its keys that come from file contents
   (`name`, `jurisdiction`, `isic`, `country`) are omitted rather than guessed. Verification stays open
   until an independent digest check runs.
4. `scripts/build_dataset_catalog.py` regenerates the files from GitHub (read-only GraphQL) plus local
   clones, deterministically for a given `--observed-on`. `validate.py` checks schema, family/count
   agreement, unique ids and repositories, and that `verified` and non-empty `payload` agree.
5. Publication changes nothing in the owning repositories. It does not archive, merge, rename or
   deregister them, and it does not move any consumer to the registry.

## Not decided here

- **Retiring repositories.** Consumers address these repositories directly. For example
  `network-awai/app-hyakka` scans `cloud-itonami-lei-*` directories, and `com-junkawasaki/root` and
  west-manifest reference them. Archiving or consolidating a repository needs each consumer moved to
  pinned-commit resolution first, and consolidation discards per-repository history, so each is a
  separate, separately approved change.
- **Policy-text archives.** The `lei` repositories archive third-party privacy-policy text. The registry
  carries only digests and provenance, never that text. Whether the owning repositories should hold the
  text is outside this registry.
- **Other families.** `isic`, `isco`, `iso` and `iso3166-*` repositories carry governor code, not only
  data, and need a separate review before any catalog shape is chosen.

## Consequences

- A consumer can resolve a subject to a pinned commit and verify file digests without listing the
  organization.
- The catalog is a dated snapshot; a stale commit means "as observed", not "current". Re-run the builder
  to refresh, and review the diff.
- Entries pin the repository default branch at observation time. A later rewrite of that history
  invalidates the pin visibly rather than silently.
