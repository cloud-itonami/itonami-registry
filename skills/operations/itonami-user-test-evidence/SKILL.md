---
name: itonami-user-test-evidence
description: Prepare and evaluate portable user-test studies while separating human, synthetic and recipe evidence.
metadata:
  hermes:
    version: 0.1.0
    author: cloud-itonami
    source: https://github.com/kotoba-lang/user-test/tree/a4bad00dd3a2a5a0671afb6dc7e6046f1cef30af
    compatibility:
      hermes: '*'
      desktop: '*'
---

# itonami-user-test-evidence

1. Read the pinned user-test study contract and validate the supplied study with the owner runtime. Planning and validation operate on contracts; they do not recruit participants or operate a browser.
2. Produce an executor-neutral plan and bind the approved executor, observation scope and consent boundary in the owning host.
3. Record each run's immutable observed outcomes and classify it as human, synthetic or recipe. Missing execution remains missing, not a successful test.
4. Evaluate actual outcomes and retain issue-shaped findings and source run references. Aggregate each evidence class separately, including failures and unmeasured journeys.
5. Keep personas, screenshots, transcripts and identifiers host-local. Export only permitted opaque references and aggregates; report the executor and evidence limits.

Source contracts are pinned in itonami.json and catalogs/sources.json. Runtime implementations and existing profiles remain in their owning repositories.
