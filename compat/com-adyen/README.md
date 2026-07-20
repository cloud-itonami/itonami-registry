# Adyen Clean Room Actor

This actor provides a clean-room, API-compatible implementation of the Adyen platform.

The generated actor schema uses `.kotoba-schema`; bare `.kotoba` is reserved
for canonical capability-safe Kotoba guest/component source.

## Architecture
- **State:** Backed by Datomic for immutable, time-travel-capable record keeping.
- **Schema:** Defined in `schema/adyen.kotoba`.
- **Execution:** Runs in `Py Kotodama WASM`, intercepting inbound REST requests.

## Provenance

Relocated 2026-07-04 from `etzhayyim/root/20-actors/adyen-compat` to
`kotoba-lang/com-adyen` per the org-taxonomy library-placement rule (any
library/substrate code belongs in `kotoba-lang`, ADR-2606302300), following
the same relocation pattern as `kami-nv-compat` (ADR-2607020130). See
ADR-2607041500 for the full ~1,027-repo migration plan and naming convention.
