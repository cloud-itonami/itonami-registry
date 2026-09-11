# Fab Lithography Clean Room Actor (Clojure / Datomic)

Clean-room Semiconductor fab / EUV lithography process actor in portable Clojure (`.cljc`) over the **kotoba Datom log** (content-addressed EAVT Datalog, Datomic-isomorphic — ADR-2605262130 + ADR-2605312345). CRUD + validation behind a `DatomPort` DI seam; production adapter = kotoba-kqe, tests = `in-memory-datom`. No external managed DB.

```
kbb --classpath src:tests -e "(require 'fab_lithography.actor-test) (clojure.test/run-tests 'fab_lithography.actor-test)"
```

## Provenance

Relocated 2026-07-04 from `etzhayyim/root/20-actors/fab_lithography-compat` to
`kotoba-lang/com-fab-lithography` per the org-taxonomy library-placement rule (any
library/substrate code belongs in `kotoba-lang`, ADR-2606302300), following
the same relocation pattern as `kami-nv-compat` (ADR-2607020130). See
ADR-2607041500 for the full ~1,027-repo migration plan and naming convention.
