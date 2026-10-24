# ADR 0008: A profile that holds real data lives in its own repository

Status: proposed — 2026-10-24

## Context

A profile entry (ADR 0002) pins `repository`, `commit`, `path` and a checksum. Nothing
requires the repository to hold one profile. Measured on 2026-10-24: 897 entries in 759
repositories; 733 repositories hold one profile and 26 hold 164 between them (`isic` 21,
`cloud-itonami-app` 19, `amu` 15, `ao-repo-steward` 13, `ao-assistant` 10, `ao-bot-fleet` 9,
`murakumo` 9, `isco` 8, `kotobase` 7, `kotoba` 5, `giemon` 5, and others with 2 to 4).

Consolidating repositories lowers the cost of managing and syncing them. It also removes
the unit that carries a profile's history, review, access and archive. A profile that holds
real data needs that unit; a fleet that is maintained as one organization does not.

State is separate (ADR 0003): sessions, logs, memories and ledgers stay out of the registry
and out of definition repositories. Hermes keeps its sessions in a per-profile sqlite file,
`~/.hermes/profiles/<p>/state.db`, on the host. This ADR does not move that.

## Decision

1. **Rule.** A profile that holds real data lives in its own repository: one profile, one
   repository, with `hermes/profiles/<id>/` at the root (the layout of
   `scripts/hermes-profile-repo.cljk`).
2. **Holding real data** means at least one of: the owner's definition of the profile is
   edited by people or agents on its own schedule; it carries domain data, datasets or
   receipts as part of its definition; it has its own access, release or archive decision;
   other registry entries or bindings depend on its history.
3. **Exceptions are declared, not assumed.** A repository may hold several profiles only
   when it is listed in `catalogs/shared-profile-repositories.json` with a `kind` and a
   `reason`:
   - `fleet`: profiles that operate as one organization (for example the `ao-*` fleets),
     are released together, and share their skills and rules.
   - `maintainer`: a repository whose profiles are generated or maintained by one tool or
     one owner as a set.
4. **Repositories without profiles are free to consolidate.** The rule concerns profile
   repositories only. Repositories with no profile and no registry entry may be merged into a
   monorepo (the JUN-355 option A set).
5. **Moving a profile keeps its checksum** (ADR 0007 rule 4), so splitting a shared
   repository or merging a profile into a fleet is verified, not trusted.

## Registry check

`scripts/profile_status.py --shared-only` reads only the manifests and the declaration; it
needs no network and no cache. `--findings-out FILE` writes the findings as JSON in either
mode. The codes:

| Code | Meaning |
|---|---|
| `shared-repository` | A repository holds two or more profiles and is not declared. This is the finding to resolve: split it, or declare it with a reason. |
| `shared-repository-declared` | Declared `fleet` or `maintainer`. Reported with its reason; not a problem. |
| `declaration-without-sharing` | Declared, but holds one profile or fewer. The declaration is stale. |
| `declaration-unknown-repository` | Declared, but no entry names the repository. |

`scripts/validate.py` checks only that the declaration file is well formed (schema, kinds,
a non-empty reason, no duplicates). Findings never fail validation and never edit a manifest
or an owner's repository.

## Consequences

- The declaration file ships empty, so today all 26 shared repositories are reported as
  `shared-repository`. Declaring the fleets (`ao-*` and similar) is the owner's decision and
  a separate change; this ADR does not guess which are fleets.
- The sqlite session store is untouched. A fleet repository shares definitions, not state.
- The status model (ADR 0007) is unchanged: findings are a second, offline view over the same
  manifests.
- Not decided here: splitting any shared repository, and how the Itonami agent CLI stores its
  sessions (its `~/.itonami/` layout is not yet verified).
