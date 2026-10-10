# Remaining candidate review — 2026-10-11

Reviewed the 37 repositories previously marked candidate-owner-review-required or deferred-source-contract. Each current public default head and complete recursive tree was read, and relevant root documentation, native entrypoints/tool definitions and selected skill contracts were inspected. No private source, runtime ledger, credential, profile instance or host configuration is imported. This is a source-scoped review, not exhaustive runtime or security qualification.

The separate [candidate review catalog](../catalogs/candidate-reviews.json) pins every decision to the reviewed commit and original evidence file hashes. The organization-wide tree inventory remains the 2026-10-10 snapshot; its selection decisions and entry registrations are updated from these separately dated reviews. Review decisions do not overwrite the older tree snapshot's commit or pretend that all repositories were re-surveyed today.

| Decision | Owner repositories | Meaning |
|---|---:|---|
| registered | 10 | A reusable procedure, role, native connection or provider reference was added |
| deduplicated | 7 | Repeated bundles/language migration guidance retain canonical ownership |
| source-only | 13 | Host-bound libraries, clients or generated tables remain source references |
| deferred | 5 | Specific source/license/transport/verification blockers remain |
| already-owned | 2 | Existing plugin provider and this registry itself are not imported again |

## Added set

Nine skills and five role scaffolds generalize useful procedures without copying identity, dated numeric results, hardcoded account details or profile state.

| Skill | Source owner | Optional role scaffold |
|---|---|---|
| itonami-scheduled-report-review | codec-primitives | scheduled-report-reviewer |
| itonami-ioc-ledger-curation | yabai-actor | source-ledger-curator |
| itonami-knowledge-publication-receipts | app-bpmn | — |
| itonami-measured-proposal-handoff | ao-arbitrage | — |
| itonami-declarative-config-evidence | ao-assistant | — |
| itonami-selective-regression-pins | suji | simulation-pin-reviewer |
| itonami-compute-allocation-observation | zap-proxy | compute-allocation-observer |
| itonami-resident-business-observation | cloud-itonami-isic-8121 | resident-business-observer |
| itonami-ui-host-evidence | devtools | — |

These preserve useful distinctions: a delivered report versus verified claims; feed listing versus threat attribution; Git persistence versus byte readback versus serving root; draft versus publisher delivery; unreadable config versus satisfied policy; selective break evidence versus copied model numbers; declared capacity versus measured demand; held/backoff versus dead resident; and planned UI events versus actual host observations. Owner authorization and effective runtime policy bind any process, network, persistence, publication or UI effect.

## Native connections and tool references

Added **mcp/itonami-fleet-catalog** from the current cloud-itonami-app `bin/itonami-mcp` launcher. This guest-Wasm host publishes **fleet_search only**. The older JVM adapter's fleet_call, business/payment tools and session bindings must not be projected onto this connection. Search reads a bundled actor directory; an endpoint in that directory is not a health receipt or invocation grant. The owner-built `target/amu/mcp_main.wasm`, a positive guest main, catalog and host dependencies are prerequisites. Compiled guest startup, client interpolation and successful discovery remain **untested**; no source checkout is claimed to be an operational install.

Added three provider-qualified Hermes plugin references from **zap-proxy**: `zap_scan`, `zap_scan_active`, `zap_scan_rules`. Native descriptions and schemas are extracted as Python AST literals and retain upstream MIT attribution. The configured target-origin gate and active allow_active requirement are runtime constraints; an allowlist does not establish caller authorization or target ownership. Passive probing still sends HTTP traffic; active probing sends diagnostic payloads. No handler was imported, scanner started, target configured or network scan performed. Use the pinned owner plugin/runtime, explicitly resolve `ZAP_PROXY_REPO` to its canonical owner checkout (the source has an old compatibility default), and inspect its current dependencies before invocation. These references are discovery metadata, not a plugin installer or runtime grant.

The resulting registry contains **39 entries**: 21 skills, 13 agent templates, three MCP connections and two inert workflows; **19 native provider tool references** supplement them. All agent scaffolds keep empty toolsets and carry no identity or schedule. Existing profiles remain in their owning repositories.

## Deliberate deferrals

- **shinkansen:** the advertised stdio implementation emits a non-JSON readiness banner on stdout and exposes lake_dispatch with an R0 no-app refusal. No LICENSE is present at the reviewed head. Transport framing, loader dependencies, source licensing and host dispatch binding require owner resolution before installable registration. No compatibility shim that hides this boundary is shipped.
- **app-classifieds:** local executable demo exists, but source publication licensing is absent and native/generated descriptor consistency remains unresolved. Demo search is not live marketplace access or transaction qualification.
- **com-unity-api-services / com-unity-ads:** respect the canonical provider owner and README's schema-only/non-executable boundary until authenticated verification. A dry-run adapter is not a receipt-backed operational connector.
- **kotodama-mcp:** provider manifests are integration inputs; each actual provider requires its own executable transport and dependencies. Do not infer one monolithic server.

Host-bound app/daemon/agent tool implementations, portable devtools, compiler encoding wrappers, client proxies and generated command tables remain with their owners. Copied bundles are deduplicated; source instructions involving shared-checkout resets, runtime configuration writes or frozen measured constants were not copied into reusable skills. kotoba-registry still owns github-forest and github-forest-maintenance, and no new local entry duplicates either.

## Verification boundary

Offline schemas check manifests, sidecars, public inventory coverage, dependency/checksum freshness and review decisions/provenance. Integrity tests exercise malformed counts, mutable evidence links, authority escalation and external duplicates. New skills pass skill-creator frontmatter checks. GitHub immutable readback verifies registered derivation inputs and all reviewed candidate file identities; native ZAP descriptors are compared without executing handlers. The existing Murakumo discovery probe still sends zero valid tools/call. None of these checks proves startup, live scans, resident firing, host UI effects or physical/runtime qualification of the new entries.
