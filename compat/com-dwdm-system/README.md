# Dwdm System Clean Room Actor (Clojure / Datomic)

Clean-room DWDM optical line system / 光電融合 transport actor in portable Clojure (`.cljc`) over the **kotoba Datom log** (content-addressed EAVT Datalog, Datomic-isomorphic — ADR-2605262130 + ADR-2605312345). CRUD + validation behind a `DatomPort` DI seam; production adapter = kotoba-kqe, tests = `in-memory-datom`. No external managed DB.

```
bb --classpath src:tests -e "(require 'dwdm_system.actor-test) (clojure.test/run-tests 'dwdm_system.actor-test)"
```

## Provenance

Relocated 2026-07-04 from `etzhayyim/root/20-actors/dwdm_system-compat` to
`kotoba-lang/com-dwdm-system` per the org-taxonomy library-placement rule (any
library/substrate code belongs in `kotoba-lang`, ADR-2606302300), following
the same relocation pattern as `kami-nv-compat` (ADR-2607020130). See
ADR-2607041500 for the full ~1,027-repo migration plan and naming convention.
