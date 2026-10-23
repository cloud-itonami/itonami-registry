# Serdes Phy Clean Room Actor (Clojure / Datomic)

Clean-room High-speed SerDes PHY design actor in portable Clojure (`.cljc`) over the **kotoba Datom log** (content-addressed EAVT Datalog, Datomic-isomorphic — ADR-2605262130 + ADR-2605312345). CRUD + validation behind a `DatomPort` DI seam; production adapter = kotoba-kqe, tests = `in-memory-datom`. No external managed DB.

```
kbb --classpath src:tests -e "(require 'serdes_phy.actor-test) (clojure.test/run-tests 'serdes_phy.actor-test)"
```

## Provenance

Relocated 2026-07-05 from `etzhayyim/root/20-actors/serdes_phy-compat` to
`kotoba-lang/com-serdes-phy` per the org-taxonomy library-placement rule (any
library/substrate code belongs in `kotoba-lang`, ADR-2606302300), following
the same relocation pattern as `kami-nv-compat` (ADR-2607020130). See
ADR-2607041500 for the full ~1,027-repo migration plan and naming convention.
