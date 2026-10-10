---
name: itonami-scheduled-report-review
description: Verify claims in a delivered scheduled report against actual output, measurements and claimed artifact writes.
metadata:
  hermes:
    version: 0.1.0
    author: cloud-itonami
    source: https://github.com/kotoba-lang/codec-primitives/tree/a1cef880461d869e4ae2289c43e5f4da8e3e0f5e
    compatibility:
      hermes: '*'
      desktop: '*'
---

# itonami-scheduled-report-review

Read the actual delivered output and its job/run identity before reviewing the forwarded summary. Check the claims that affect the verdict against their cited artifacts and cheap independent observations. A live reading at a different time is context, not proof that an earlier value was wrong.

If the headline depends on a measurement that has not been reproduced in the relevant cycle, run one representative owner-approved check or mark it unmeasured. Zero loaded tests, empty output, missing artifacts and unavailable runners are not passes. Compare timing with resource contention before calling it a performance regression; matching counts alone do not prove semantic correctness.

Verify any claimed runbook or ledger write by reading the persisted artifact. Report correct, needs correction or unmeasured, with the evidence checked and remaining gaps. Correct only caller-authorized report artifacts; credential, provider and scheduler problems go to their owners. Do not silently create a missing baseline.

Pinned derivation inputs are in itonami.json and catalogs/sources.json; owner runtimes and profiles are referenced, not imported.
