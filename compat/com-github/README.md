# Github Clean Room Actor

This actor provides a clean-room, API-compatible implementation of the Github platform.

It also owns `github.workflow`, the portable library/harness shared by local
business applications. The contract normalizes Organization, Repository,
Projects v2, Issues, Pull Requests, checks, workflows and Actions runs into a
single repo-scoped snapshot. HTTP and authentication are injected, so the same
code runs against a GitHub App, `gh api`, a Worker, or deterministic fixtures.

```clojure
(require '[github.workflow :as gh])
(def snapshot (gh/execute-plan request-fn {:owner "kotoba-lang" :repo "demo"}))
(gh/health snapshot)
```

Deterministic end-to-end harness:

```sh
kbb -M:harness fixtures/demo.edn kotoba-lang demo
```

Mutating capabilities are named separately from read capabilities. Consumers
must place issue/PR/project writes and workflow dispatch behind their own human
approval/governor; this library does not silently turn reads into writes.

Committed public organization profiles live under `resources/organizations/`.
The `gftdcojp` profile uses business domain `gftd.co.jp` and operator contact
`jun@gftd.group`; credentials and tokens never belong in these profiles.

## Connector

`github.connector` exposes this client as **tools with an OAuth profile and
per-tool scopes**, so an agent can be granted part of GitHub rather than all of
it — the connector plane of ADR-2608097000. `connector.edn` declares the
contract without loading any Clojure.

| | |
|---|---|
| `github.main` | the clean-room actor — GitHub's API implemented *here* |
| `github.workflow` | a client that normalizes one repository into a snapshot |
| `github.connector` | a client exposed as tools, grantable scope by scope |

`workflow` and `connector` are both clients and deliberately not layered on
each other: `workflow` answers one fixed question by fetching a plan, a
connector answers whatever the tool was called with. They share the origin and
nothing else.

Seven tools; only `github_create_issue` writes, and only it needs `repo` write
access to be exercised. `github_get_authenticated_user` asks for `read:user`
alone, so a deployment that only identifies the account never holds `repo`.
GitHub's OAuth Apps do not verify PKCE and the descriptor says so rather than
sending a challenge nobody checks.

```sh
kbb --backend sci --classpath "src:test:../connector/src" run-connector-tests.cljk   # 13 tests, 50 assertions
kbb --backend sci --classpath "src:../connector/src" emit-connector-edn.cljk         # regenerate connector.edn
```

## Architecture
- **State:** Backed by Datomic for immutable, time-travel-capable record keeping.
- **Schema:** Defined in `schema/github.kotoba`.
- **Execution:** Runs in `Py Kotodama WASM`, intercepting inbound REST requests.

## Provenance

Relocated 2026-07-04 from `etzhayyim/root/20-actors/github-compat` to
`kotoba-lang/com-github` per the org-taxonomy library-placement rule (any
library/substrate code belongs in `kotoba-lang`, ADR-2606302300), following
the same relocation pattern as `kami-nv-compat` (ADR-2607020130). See
ADR-2607041500 for the full ~1,027-repo migration plan and naming convention.
