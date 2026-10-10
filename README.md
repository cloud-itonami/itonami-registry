# Itonami Registry

Reusable bot role templates, operational skills, MCP connection definitions and workflow recipes for Itonami agents. Actual bot profiles remain owned by their existing GitHub repositories. Registry publication grants no execution authority, changes no running profile and activates no scheduler.

## Initial entries (retained)

| Type | ID | Purpose |
|---|---|---|
| agent | fleet-health-auditor | Measured bot and cron fleet review |
| agent | physical-ai-evidence-bot | Domain simulation evidence and bounded improvement |
| skill | itonami-cron-health-audit | Correlate cron records, scheduler logs and final output |
| workflow | fleet-health-review | Collect, classify and report fleet evidence |
| workflow | evidence-measured-improvement | Bind a domain premise, measure and propose one improvement |
| mcp | murakumo-web | Connection definition for the owner-installed web-plane server |

The physical-AI agent includes ISIC 7020 and ISCO 2421 parameter examples. Templates are partial scaffolds; they have no profile identity, credentials, enabled tools or cron jobs. Each target repository binds its parameters and policy before use. The ISCO example preserves the source's hypothetical physical premise.

## Discover and consume

Start at [llms.txt](llms.txt), then [llms-full.txt](llms-full.txt). The public discovery endpoint is https://raw.githubusercontent.com/cloud-itonami/itonami-registry/main/index.json. Resolve the registry to one immutable commit and verify the complete selected folder checksum before use.

Skills use SKILL.md frontmatter; MCPs, agents and workflows use Hermes manifest shapes. itonami.json contains supplemental inputs, effects and authority requirements. Wildcard Hermes/desktop version fields express no declared version filter; only catalog format has been checked. Runtime installation compatibility has not been qualified. workflow.json uses an Itonami recipe schema and requires a compatible reader; it is not a proven Hermes executable workflow.

[catalogs/tools.json](catalogs/tools.json) indexes eight Murakumo MCP tools, four portable user-test MCP tools and three plugin-hermes tools, with provider identity and input contracts. [catalogs/sources.json](catalogs/sources.json) records pinned derivation inputs and file hashes. Tool discovery is not a successful live invocation.

## Ownership and federation

[kotoba-registry](https://github.com/kotoba-lang/kotoba-registry) remains the Kotoba extension catalog. Its github-forest MCP and github-forest-maintenance skill are referenced in catalogs/external-registries.json, not copied. Registry-qualified identities prevent collisions. Federation requires a consumer that understands the external registry descriptor.

Source code, per-bot SOUL/config/cron definitions and domain policies stay in the owning repositories. Sessions, credentials, runtime state and ledgers stay in their application homes. This registry is separate from west pins and from signed CID-pinned language package admission.

## Maintain

Use Python 3.11 or later in an isolated environment and install requirements.txt, then:

```text
python scripts/validate.py
python scripts/build_index.py
python scripts/build_index.py --check
python -m unittest discover -s tests
```

For release verification with authenticated GitHub CLI, run `python scripts/verify_sources.py`. To reproduce the bounded MCP discovery probe, run `python scripts/probe_mcp.py --checkout /absolute/path/to/kotoba-lang/murakumo`; it reads the pinned script with Git and sends no valid tool invocation. The existing checkout is not modified.

index.json is generated. CI validates schemas, checks catalog freshness, source references, entry integrity and dependencies, and rejects duplicated external entries. Change the version when an entry changes. Keep immutable source references and describe the actual validation boundary.

See [ADR 0001](docs/adr/0001-registry-ownership.md) and [validation receipt](docs/validation.json). New authored registry content and tooling are MIT; the source repositories retain their own licenses. Upstream profiles and runtime implementations have not been copied. Vendored Hermes schemas retain their MIT attribution in NOTICE.

## Organization inventory and expansion

The 2026-10-10 inventory covers 4,710 GitHub repositories across both organizations. The public [machine-readable inventory](catalogs/inventory.json) contains 4,614 repositories: every nonempty public default branch has a complete recursive filename survey; one repository has an empty default branch. Private repositories are counted only (96); their names and contents are omitted. Filename markers are candidates, not semantic or runtime qualification. See [coverage and selection decisions](docs/inventory-2026-10-10.md).

The catalog now has **24 entries**: 12 skills, 8 agent templates, 2 MCP connections and 2 inert workflows, plus **15 provider-qualified tool references**. Added roles cover repository maturity, provider capabilities, research corpora, sealed inbox observation, learning material drafts and independent evidence review. Added skills also cover portable user tests, content-addressed receipts, host connector contracts, definition inspection, guest admission and system-dynamics evidence. These are Itonami operational adaptations; upstream implementation and generic language skills retain their owners.

The user-test connection is source-inspected and has a checked fail-closed launcher; its target runtime is not qualified. The Murakumo discovery probe sends zero valid tool calls and performs no live network operation. The inventory includes candidate and deferred decisions; neither these records nor publication enables a profile or tool.
