# Intercom Clean Room Actor

This actor provides a clean-room, API-compatible implementation of the Intercom platform.

## Architecture
- **State:** Backed by Datomic for immutable, time-travel-capable record keeping.
- **Schema:** Defined in `schema/intercom.kotoba`.
- **Execution:** Runs in `Py Kotodama WASM`, intercepting inbound REST requests.

## Provenance

Relocated 2026-07-04 from `etzhayyim/root/20-actors/intercom-compat` to
`kotoba-lang/com-intercom` per the org-taxonomy library-placement rule (any
library/substrate code belongs in `kotoba-lang`, ADR-2606302300), following
the same relocation pattern as `kami-nv-compat` (ADR-2607020130). See
ADR-2607041500 for the full ~1,027-repo migration plan and naming convention.
