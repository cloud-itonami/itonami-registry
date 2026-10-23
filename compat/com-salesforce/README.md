# Salesforce Clean Room Actor

This actor provides a clean-room, API-compatible implementation of the Salesforce CRM platform.

## Architecture
- **State:** Backed by Datomic for immutable, time-travel-capable record keeping.
- **Schema:** Defined in `schema/sforce.kotoba` (translates Salesforce standard objects like Account, Contact, Opportunity).
- **Execution:** Runs in `Py Kotodama WASM`, intercepting inbound REST requests and SOQL queries.

## Provenance

Relocated 2026-07-05 from `etzhayyim/root/20-actors/salesforce-compat` to
`kotoba-lang/com-salesforce` per the org-taxonomy library-placement rule (any
library/substrate code belongs in `kotoba-lang`, ADR-2606302300), following
the same relocation pattern as `kami-nv-compat` (ADR-2607020130). See
ADR-2607041500 for the full ~1,027-repo migration plan and naming convention.
