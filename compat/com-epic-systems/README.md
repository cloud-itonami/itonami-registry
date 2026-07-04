# Epic-systems Clean Room Actor

This actor provides a clean-room, API-compatible implementation of the Epic-systems platform.

## Architecture
- **State:** Backed by Datomic for immutable, time-travel-capable record keeping.
- **Schema:** Defined in `schema/epic-systems.kotoba`.
- **Execution:** Runs in `Py Kotodama WASM`, intercepting inbound REST requests.

## Provenance

Relocated 2026-07-04 from `etzhayyim/root/20-actors/epic-systems-compat` to
`kotoba-lang/com-epic-systems` per the org-taxonomy library-placement rule (any
library/substrate code belongs in `kotoba-lang`, ADR-2606302300), following
the same relocation pattern as `kami-nv-compat` (ADR-2607020130). See
ADR-2607041500 for the full ~1,027-repo migration plan and naming convention.
