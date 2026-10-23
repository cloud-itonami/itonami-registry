# ADR 0007: A profile entry has a derived status against its owner's repository

Status: proposed — 2026-10-23

## Context

A profile entry (ADR 0002) pins `repository`, `commit`, `path` and a checksum. The
owning repository keeps changing: the owner edits the profile, moves it, removes it, or
merges the repository into another (the `text` libraries into `kotoba-lang/kotoba`,
JUN-203). A pin is immutable, and an archived repository still serves its pinned
commit, so a pin never becomes invalid by itself. What changes is whether the pin still
describes what the owner has.

Measured on 2026-10-23 against each repository's default-branch tip (fetched from the
remote, not read from local checkouts): of the 897 entries, 896 are `current` and 1
(`cljk-finish`, in `cloud-itonami/ao-repo-steward`) is `behind`; none is `withdrawn` or
`unreachable`. The registry is in good shape. The model exists so that this stays
visible, and so that the effect of a consolidation can be measured.

(A first look compared the pins with the local checkouts instead. Those are pinned by
the west manifest and were older than the registry pins, which made roughly two thirds
of the entries look stale. They were not. A status is only meaningful against the
remote tip.)

The operational binding (`:home` in the root `manifest/agent-registry`) and the registry
named the same repository for 889 of the 892 profiles bound in both; 5 registry entries
have no binding. The 3 that differ are `server-operator-crawl`, `whois-org-crawl` and
`wiki-standards-crawl`: their repository was consolidated into `kotoba-lang/kotoba`
(JUN-203), the binding was updated, and the registry still pins `kotoba-lang/text`. The
archived repository still serves the pinned commit, so the entries are `current`. The
move is visible only in the binding comparison, which is why rule 5 below matters.

## Decision

Each entry has a **status**, computed, never edited, against the tip of the source
repository's **default branch**:

| Status | Meaning |
|---|---|
| `current` | The profile at the tip is the pinned one: the same tree at the pinned path, or the same registry checksum over the allowed files (files the registry never pins, such as `memories/`, may differ). The pinned commit is on the default branch. |
| `behind` | The repository has moved on: the pinned files differ at the tip, the profile moved to `hermes/profiles/<id>`, or the pinned commit is not on the default branch. The profile still exists. |
| `withdrawn` | The repository is reachable and has no profile at the pinned path or at `hermes/profiles/<id>` on the default branch. |
| `unreachable` | The repository cannot be fetched, has no default-branch tip, or does not contain the pinned commit. |

Rules:

1. **Derived, not stored in the manifest.** A manifest stays a pin. The status is the
   output of `scripts/profile_status.py` and is a dated observation (`tip`, and the time
   of the run), not part of the entry's identity.
2. **An archived or re-homed repository keeps its status.** If the owner consolidates a
   repository and archives the old one, the old tip is unchanged and the entry stays
   `current`; the move shows up as `homeMatches: false`, not as a change of status.
3. **Nothing is deleted because of a status.** `withdrawn` and `unreachable` entries stay
   in the catalog and the pin stays resolvable; a consumer sees the status and decides.
   Removing an entry is a separate, deliberate act of the owner.
4. **The checksum is location independent** (`scripts/profile_tree.py`: allowed files, by
   path relative to the profile folder), so moving a profile between repositories keeps
   the checksum. A move is verified by the checksum, not by trusting the move.
5. **One home, two views.** The registry's `profile.repository` and the operational
   `:home` must name the same repository. `--homes` reports the disagreements; they are
   findings, not errors, because the binding changes before the registry is re-pinned.
6. **Re-pinning is an explicit act** of the profile's owner (`scripts/add_profile.py`), after
   a release or a move. The registry does not follow the tip, and the sync of a running
   bot is a separate mechanism that does.
7. **A repository move changes two things together**: the `:home` binding and the registry
   pin. A tool that moves a profile's home must do both and check that the checksum is
   unchanged.

## How it is computed

`python3 scripts/profile_status.py --cache DIR [--homes homes.json] [--out FILE]` keeps a
partial bare clone (commits only; trees and blobs on demand) of each source repository in
`DIR`, reads the default-branch tip, and compares. It needs network access and ssh to the
repositories, so it is not part of `validate.py`; a run is recorded where it is needed.

## Consequences

- Stale pins become visible and countable instead of silently wrong.
- A consolidation (several repositories into one) has a measurable effect on the
  registry: the affected entries become `behind` or `withdrawn` until they are re-pinned
  at the new repository, and the checksum shows the profile itself did not change.
- Out of scope: automatic re-pinning, the lifecycle of the running bot, and any execution
  authority (the registry grants none, ADR 0001).
