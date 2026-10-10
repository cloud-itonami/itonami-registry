---
name: itonami-system-dynamics-evidence
description: Run an owner-defined stock-flow model for an Itonami operational question and retain measured assumptions and ledger references.
metadata:
  hermes:
    version: 0.1.0
    author: cloud-itonami
    source: https://github.com/kotoba-lang/skill-loop-system-dynamics/tree/7cf1c7eab5a6421eda3b448f9530f741e9114a9e
    compatibility:
      hermes: '*'
      desktop: '*'
---

# itonami-system-dynamics-evidence

1. Resolve the owning model and its stock-flow contract, target and runner. Use the owner's current README invocation and classpath rather than duplicating its scoring rules.
2. Bind one operational question, observation date and seed data. List missing rates or parameters explicitly; do not invent values to make an outcome appear measured.
3. Execute one caller-authorized bounded scenario using the owner runtime. Preserve target, input identity, exit status, output and ledger references in the authorized evidence store.
4. Distinguish observed inputs, assumptions, simulated outcomes and real operational results. Compare scenarios only when their inputs and target contracts are compatible.
5. Report the useful result and uncertainty. Model execution does not authorize scheduling, infrastructure changes or replacing another domain's authority.

Source contracts are pinned in itonami.json and catalogs/sources.json. Runtime implementations and existing profiles remain in their owning repositories.
