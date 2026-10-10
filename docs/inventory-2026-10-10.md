# Organization inventory and registry selection — 2026-10-10

This expansion adds 18 reusable entries to the initial six: 11 skills, six agent role scaffolds and one MCP connection. The total is 24 entries and 15 native provider tool references. Original profiles, measurements, identities, runtime configuration and credentials remain in the owning repositories.

## Coverage

| Organization | GitHub repositories | Public detailed records | Private aggregate only | Full public recursive trees | Empty default branch |
|---|---:|---:|---:|---:|---:|
| kotoba-lang | 2,786 | 2,752 | 34 | 2,751 | 1 |
| cloud-itonami | 1,924 | 1,862 | 62 | 1,862 | 0 |
| Total | 4,710 | 4,614 | 96 | 4,613 | 1 |

The survey enumerated GitHub organization repositories, each default head, root entries and profile directory names. Committed local recursive trees were used only when their revision equaled the observed default head. The other 725 public trees were read recursively from the pinned GitHub API; none was truncated or unreadable. Repository/branch observations form a bounded multi-request snapshot, not an atomic global transaction. Local WIP, untracked source and damaged metadata were preserved. Private names and contents are omitted from published artifacts; private-source candidates were excluded from this public set.

[catalogs/inventory.json](../catalogs/inventory.json) contains one row per public repository, scan basis, default commit, selected filename markers, disposition and registered entry/sourceCommit relationships. Skill files, profile SOUL paths, MCP-looking implementations, plugin manifests and tool definitions are filename candidates. **A complete filename survey is not a semantic audit of every source file or a runtime qualification.** A no-marker disposition does not assert that a repo has no reusable behavior. Thirty further filename-candidate owners remain in the catalog for semantic review; they are not silently turned into executable entries.

Profile instances and physics-domain records are retained by reference rather than multiplied into hundreds of nearly identical bots. Copied operational skill bundles and upstream forks are not bulk imported. A curated sourceCommit may be older than the survey's default commit; it pins the actual derivation input and its file hash, not the current runtime state.

## Added entries

| Owner source | Reusable skills | Bot role |
|---|---|---|
| ao-bot-fleet | repository maturity evidence; provider capability observation | repo-maturity-steward; provider-capability-observer |
| loop-data-source | data source reconciliation | research-corpus-curator |
| app-mail-relay | sealed inbox metadata observation | sealed-inbox-observer |
| ao-hiraku | learning material draft gates | learning-material-author |
| ao-repo-steward | — | independent-evidence-reviewer |
| user-test | portable study/run evidence | user-test MCP connection, four native tool references |
| murakumo | content-addressed receipts | initial web-plane connection retained |
| connector | host connector contract inspection | — |
| symbol-index | definition/caller inspection for scoped review | — |
| skill-guest-authoring | guest admission/execution evidence | — |
| skill-loop-system-dynamics | operational model evidence | — |

These are target-bound Itonami procedures, not copies of general language/SDK documentation. Each entry declares pinned provenance, inputs, outputs, effects and a blocked-by-default authority binding. Agent scaffolds contain no identity, enabled toolsets, schedule or materializer. Skills that can run a collector or write a result require the caller-selected command, scope and artifact location.

## Deferred and external boundaries

- **kotoba-registry:** github-forest MCP and github-forest-maintenance remain external pinned entries. No competing forest maintenance or registry authority is introduced.
- **cloud-itonami-app:** runtime artifact, session and capability-dependent resident adapter; do not publish a fixed toolset or an unqualified launcher from a leftover adapter.
- **connector:** host-injected portable projection, not a standalone transport server. Only its operational inspection procedure is registered.
- **kotodama-mcp / Unity provider contracts:** server-shaped documentation and schema-only surfaces need an actual executable adapter and dependency/auth evidence before installable registration.
- **shinkansen:** adapter/library contracts need target binding and runtime evidence; absent dispatch attachment is not a working application integration.
- **ses / shinshi:** observed MCP client proxies are not registered as servers.
- **app-classifieds:** a new public stdio demo was found in the remote tree survey. Its native descriptors differ from generated discovery JSON (including observedAt and proposal description), and no LICENSE was present at the snapshot. Keep it as a source candidate until those publication/client contracts are resolved. Its stdio search reads two fixed examples, not a live marketplace; no deployment or transaction claim is made here.

The user-test MCP is an honest source-inspected scaffold. Its native tools validate/plan/evaluate supplied contracts; they do not operate browsers or produce new participant evidence. The clean-checkout launcher refusal paths are tested. JVM/kbb startup, installed dependency compatibility and a successful client connection remain untested. No live tools were invoked or client settings changed.

## Verification

Offline validation checks Hermes manifests, supplemental contracts, source identities, checksums, dependency resolution, public inventory coverage and registration/source relationships. Mutation tests cover source/schema drift, missing providers, authority escalation, external duplicates, symlinks and inventory drift. All new SKILL.md files pass skill-creator's frontmatter check. Source file digests are verified at their immutable GitHub revisions. The existing Murakumo MCP probe is scoped to its own provider and still checks eight descriptors without valid dispatch. No source profile or runtime instance is installed or modified by publication.
