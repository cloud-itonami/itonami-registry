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
clojure -M:harness fixtures/demo.edn kotoba-lang demo
```

Mutating capabilities are named separately from read capabilities. Consumers
must place issue/PR/project writes and workflow dispatch behind their own human
approval/governor; this library does not silently turn reads into writes.

Committed public organization profiles live under `resources/organizations/`.
The `gftdcojp` profile uses business domain `gftd.co.jp` and operator contact
`jun@gftd.group`; credentials and tokens never belong in these profiles.

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
