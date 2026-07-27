# Agleader Clean Room Actor

Clean-room API-compatible implementation of the agleader physical substrate/core protocol, backed by Datomic and Py Kotodama WASM.

The generated actor schema uses `.kotoba-schema`; bare `.kotoba` is reserved
for canonical capability-safe Kotoba guest/component source.

## Provenance

Relocated 2026-07-04 from `etzhayyim/root/20-actors/agleader-compat` to
`kotoba-lang/com-agleader` per the org-taxonomy library-placement rule (any
library/substrate code belongs in `kotoba-lang`, ADR-2606302300), following
the same relocation pattern as `kami-nv-compat` (ADR-2607020130). See
ADR-2607041500 for the full ~1,027-repo migration plan and naming convention.
