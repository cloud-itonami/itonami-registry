# ADR 0005 API entries: vendor-compatible API shapes

Status: accepted for initial publication, 2026-10-23. Builds on ADR 0001, ADR 0002 and ADR 0004.

Owner instruction (AWAI-59, 2026-10-23): 「今の com-circleci などの compat は itonami registry の本体の api registry として整理して」.
The compat actors in kotoba-lang become the registry's own API registry: a first-class entry type next to profile, agent, skill, MCP,
workflow and model. AWAI-59 keeps kotoba-lang for language and technology work and moves the description of vendor-facing API
repositories here. The repositories themselves stay where they are.

## Context

kotoba-lang holds 1,090 repositories in the AWAI-59 target set: 1,074 `com-*`, 12 with a dotted reverse-domain name and 4 `cloud-*`.
Most `com-*` repositories are clean-room compat actors. Each commits a `manifest.json` (`kind: "compat"`, tier L4 or L5) that
declares:

- entities and a REST route list;
- a DID, a Wasm CID and a runtime;
- for L5 only, `verified.source`: the vendor OpenAPI URL, or a citation, with the vendor resources and enums.

`kotoba-lang/com-circleci` is typical. It has five CircleCI entities, 25 CRUD routes and the CircleCI v2 OpenAPI URL as its source.
It contains no execution of CircleCI behaviour.

Before this ADR, the 2026-10-10 inventory listed these repositories only as `no-selected-registry-marker`. Nothing said which ones
declare an API shape, which shape it is, or at which commit.

## Decision

### 1. A sixth entry type, `api`

ADR 0002 added `profile` as the fifth type. `api` is the sixth. It appears in `index.json`, `categories.json` and the static API
(`api/v1/index.json`, `api/v1/entries/itonami-registry/api/<id>.json`), next to the other types.

An API entry is the shape of a vendor-compatible API, as declared by one source repository at one commit:

- `api.kind`: `compat` (a clean-room actor that reimplements the shape) or `client` (a client of the real vendor API);
- `api.tier`, `api.style`, `api.entities`, `api.routes` (method, path, op) and `api.routeCount`;
- `api.vendorSource` (compat): `verified.source` as stated, with `verifiedAt`, `resources` and `enums`, and
  `basis: claimed-by-source-manifest`;
- `api.upstream` (client): the vendor, API and docs URLs as stated;
- `actor`: handle, DID, runtime, exec, Wasm CID and schema path, with `basis: asserted-by-source-manifest`;
- `pin`: repository, 40-hex commit, public visibility, archive state and `files` (path, sha256, bytes). The files are
  `manifest.json`, plus `openapi.json`, `README.md` and the declared schema file when present. All are read from the pinned commit
  object.

The schema is `schemas/itonami/api.schema.json`. The folder `apis/<id>/` holds only `manifest.json`. The registry copies the listed
manifest fields and never copies the repository's files (ADR 0001).

### 2. Honest status

Every API entry carries a `status` block whose values the schema fixes:

| Field | Value | Meaning |
|---|---|---|
| `shape` | `declared-by-source-manifest` | The shape is what the owning repository says, read at the pin. The registry did not derive it from the vendor. |
| `vendorConformance` | `claimed-by-source` or `not-claimed` | Says only whether the source manifest cites a vendor source (L5 `verified.source`, client `upstream`). L4 entries cite none. A claim is not a conformance test. |
| `runtimeQualified` | `false` | No implementation of the shape has been qualified here. |
| `artifactVerified` | `false` | The Wasm CID and DID are recorded as asserted. The registry has not fetched or checked them. |
| `execution` | `none` | Registration runs nothing and serves no endpoint. |
| `authority` | `grants: false`, `default: blocked` | Registration grants nothing: no credentials, no network operation and no consent. |
| `validation` | `live: false`, `catalog: true` | Only the catalog checks have run. |

The generated L4/L5 routes are CRUD over the declared entities. They describe the actor's surface, not the vendor's full API.

### 3. Relations

- **Compat actor.** The source repository is the compat actor that declares the shape. The entry describes the shape. The actor
  is one candidate implementation, and its runtime is unqualified.
- **Itonami dapps and MCP entries.** `relations.implementedBy` and `relations.consumedBy` list registry identities: `mcp/<id>`,
  `skill/<id>`, `profile/<id>`, `agent/<id>`, `workflow/<id>`, or a federated `<registry>/<type>/<id>`.
  - Use them for an itonami dapp that serves the same shape, or for a dapp that reads data in that shape.
  - Their source of truth is the curated `catalogs/api-relations.json`. Each link there names its evidence and is reviewed in a
    pull request. The generator merges the links into the entries.
  - `validate.py` requires every local target to exist and every external target to belong to a registered registry.
  - A link states the owner's intent. It is not a conformance result, and it adds nothing to any profile.
  - Example: when the CircleCI-compatible dapp (JUN-346, `app-itonami-kumitate`) registers as an MCP entry, its PR adds
    `{"api": "com-circleci", "implementedBy": ["mcp/kumitate"], "evidence": "<pinned URL or PR>"}`.
- **MCP tools are still separate.** An MCP entry's tools stay in `catalogs/tools.json` under their provider. An API entry has no
  tools and is not an MCP server.

### 4. Identity and reverse domain

- **`id` is the owning repository name**, for example `com-circleci`. Pattern: `^[a-z0-9][a-z0-9.-]{0,99}$`.
  - The qualified identity is `itonami-registry/api/<id>`.
  - kotoba-lang origin-plane names already encode the origin: label-reversed domain + subject.
  - The workspace naming rules forbid bulk renames, so these ids are stable in practice. A renamed repository appears under its
    new name at the next refresh.
- **`api.origin` carries the reverse domain only when it is recorded.**
  - The naming rule derives names one way only, from domain to prefix. So the registry never reconstructs a domain from a name:
    `com-google-drive` does not say whether the domain is `google.com` or `google-drive.com`.
  - `origin.status` is `recorded` only when a public, pinned domain record supplies `domain`. In that case `reverseDomain` is its
    labels reversed, for example `com.stripe`.
  - Otherwise the status is `unverified`, and `domain` and `reverseDomain` are absent.
  - `origin.sourceHost` is the host of the cited vendor URL. It is evidence, not the domain record.
  - The public record is `catalogs/origin-domains.json`. See the amendment below.

### 5. Pinning, generation and federation

- **The generator** is `scripts/build_api_catalog.py --clones DIR`, following the ADR 0004 pattern.
  - `--refresh` lists the organization and reads default-branch commits, visibility, archive state and licenses with read-only
    GitHub GraphQL. It records them as pins.
  - Without `--refresh` it reuses the recorded pins. `--check` is therefore reproducible offline while the owning repositories
    keep moving.
  - Files come from the pinned commit object in local clones, never from a working tree. GitHub provides the pin and its
    visibility. Local objects provide the bytes for sha256, without an API call per file.
  - A commit object that is not available locally makes the row `unclassified` (`commit-not-available-locally`). The registry
    never guesses its contents.
- **Ownership of the outputs.** `apis/` and `catalogs/api-classification.json` belong to the generator. `catalogs/api-relations.json`
  is curated.
- **Provenance.** API entries are self-pinned, like ADR 0004 dataset references. They do not go through `catalogs/sources.json`
  or inventory registrations, which remain the provenance path for hand-curated derivations. The dated 2026-10-10 inventory is
  not rewritten.
- **The registry commit pins everything.** Index checksums cover each `apis/<id>/` folder. The manifest's `pin.files` sha256 values
  cover the owner's files at the owner's commit. These are two separate identities, as in ADR 0002.
- **Federation.**
  - Another registry refers to an API entry by registry id, pinned registry commit, `api/<id>` and checksum.
  - A federated registry's API entries keep their own qualified ids (`<registry>/api/<id>`) and never collide with ours.
  - kotoba-registry entries are not duplicated as API entries; the external-duplicate check covers `api/*` identities.

### 6. Classification of the AWAI-59 target set

`catalogs/api-classification.json` (`schemas/api-classification.schema.json`) lists every selected public repository with its
pin. Each row is classified `api`, `skill`, `profile` or `bot`, or left `unclassified` with a reason:

| Reason | Meaning |
|---|---|
| `no-api-manifest` | No `manifest.json` at the pin. The README describes a client library, codec, driver or service surface. READMEs are not parsed into shapes. |
| `dataset-snapshot-no-api-manifest` | A DataLad dataset of an external API's responses (the dotted government and organization repositories). It is data, not a shape. It is a candidate for an ADR 0004 dataset catalog after its own review. |
| `connector-contract-no-api-manifest` | A `connector.edn` with tools and OAuth scopes but no shape manifest. It is a candidate for an MCP or tool reference after review. |
| `malformed-manifest`, `unsupported-manifest-kind`, `manifest-without-api-shape` | The manifest exists but declares no usable shape. It is recorded, not repaired. |
| `registry-marker-needs-review` | A SKILL.md or profile marker exists. Skills and profiles are registered by reviewed PRs (`scripts/add_profile.py`), never by this generator. |
| `private-repository` | Counted only. Names and contents are not published. |

`skill`, `profile` and `bot` are valid classes, but the generator assigns none of them. On 2026-10-23 no selected repository had
a skill, profile or bot marker. A Bot is a profile presented in a roster (ADR 0002), so `bot` also requires a profile registration
first.

`validate.py` checks the following:

- each API entry against the schema, with its source equal to its pin and no copied files;
- that the route count, the conformance claim and every relation agree;
- that classification rows and API entries match one to one, with the same pins;
- that every count matches the rows.

## Not decided here

- Moving, archiving or renaming any repository. Publication changes nothing in kotoba-lang (AWAI-59 forbids bulk renames).
- Catalog shapes for the dataset snapshots, the connector contracts, and the `app-*` repositories that AWAI-59 left on hold.
- Any runtime qualification of a compat actor. That belongs to the actor's repository and its own receipts.

## Consequences

- A consumer can find, from one static file, every vendor-compatible API shape in the organization, with its declared entities,
  routes and vendor source, pinned and verifiable without cloning 1,000 repositories.
- `index.json` roughly doubles. Hermes clients that do not know the `api` type should skip it, as they already skip `profile`.
  `compatibility.hermes` is `none`.
- A refresh is a reviewed diff: run the generator with `--refresh`, then rebuild the index.

## Amendment 1, 2026-10-23: public origin-domain extract

The owner approved publishing the origin-domain record in its least-exposure form.

- **What is published.** `catalogs/origin-domains.json` (`schemas/origin-domains.schema.json`) holds only repository → domain
  pairs. It covers only repositories that are api entries.
  - The pairs are taken from the `:anchors` and `:domains` maps of the owner's record.
  - Everything else in the record stays private: coverage measurements, DNS sweeps, unresolvable notes, migrations and
    duplicates.
- **Provenance.** The extract records the source repository (`com-junkawasaki/root`, private), its commit, and the sha256 of both
  files. `manifest/origin-domains.edn` is the view; `manifest/origin-domains.kotoba` is the authority. Every extracted pair must
  appear in both.
  - It also records the record's own evidence labels: the date of its top-level DNS delegation check, and
    `authorityBindingEvidence: asserted-not-measured`.
  - Anyone holding the source commit can re-derive the extract with `scripts/extract_origin_domains.py --check`.
- **What `recorded` means.** The generator sets `origin.status: recorded` exactly where the extract has a fact. `domain`,
  `reverseDomain` (the domain's labels reversed), `record` and `nameMatchesDomain` come from the extract.
  - The status is `recorded`, not `verified`. The record's binding of a repository to its authority is the owner's assertion;
    only the domain's NS delegation was checked.
  - `nameMatchesDomain: false` marks a repository whose name does not follow its recorded domain, for example `com-b-pipe` →
    `com.bloomberg`. The id stays the repository name (no bulk rename); the reverse domain is the record's.
- **Version.** Curated data merged into an entry, from relations or from the origin extract, adds `.x<sha8>` to its version. A
  change in the overlay therefore changes the version.
- **Coverage on 2026-10-23.**
  - 102 of 1,028 api entries are recorded, 9 of them with names that match the domain. The other 926 remain `unverified`.
  - `com-circleci` is among the unverified entries: the owner's record has no entry for it, and the registry does not derive one.
  - Coverage grows only when the owner's record grows. Rerun the extractor, then the generator.

