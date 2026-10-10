---
name: itonami-guest-admission-evidence
description: Separate guest admission, execution and capability qualification when reviewing a bot code artifact.
metadata:
  hermes:
    version: 0.1.0
    author: cloud-itonami
    source: https://github.com/kotoba-lang/skill-guest-authoring/tree/13da2065276e7f98ffcb4876b5ce346ab8d77b71
    compatibility:
      hermes: '*'
      desktop: '*'
---

# itonami-guest-admission-evidence

1. Read fresh owner surface-status records and the selected capability kit. Retain each record's as-of date and disposition; permanent constraints differ from backend implementation gaps.
2. Select the exact artifact, export, argument contract and backend. Qualification keys differ by kit, so do not transfer a result from one kit or backend to another.
3. Perform the caller-authorized admission check using the owning toolchain and preserve its native verdict. Admitted means accepted by that check, not successfully executed.
4. When separately authorized, execute the actual export with meaningful inputs in the intended runtime and record value, refusal, runtime and artifact identities.
5. Report admission, execution and deployment evidence independently. Missing physical or production receipts remain unqualified; route any implementation change to its owner.

Source contracts are pinned in itonami.json and catalogs/sources.json. Runtime implementations and existing profiles remain in their owning repositories.
