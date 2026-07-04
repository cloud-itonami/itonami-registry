# Dpu Smartnic Clean Room Actor (Clojure / Datomic)

Clean-room DPU / SmartNIC data-path accelerator design actor in portable Clojure (`.cljc`) over the **kotoba Datom log** (content-addressed EAVT Datalog, Datomic-isomorphic — ADR-2605262130 + ADR-2605312345). CRUD + validation behind a `DatomPort` DI seam; production adapter = kotoba-kqe, tests = `in-memory-datom`. No external managed DB.

```
bb --classpath src:tests -e "(require 'dpu_smartnic.actor-test) (clojure.test/run-tests 'dpu_smartnic.actor-test)"
```

## Provenance

Relocated 2026-07-04 from `etzhayyim/root/20-actors/dpu_smartnic-compat` to
`kotoba-lang/com-dpu-smartnic` per the org-taxonomy library-placement rule (any
library/substrate code belongs in `kotoba-lang`, ADR-2606302300), following
the same relocation pattern as `kami-nv-compat` (ADR-2607020130). See
ADR-2607041500 for the full ~1,027-repo migration plan and naming convention.
