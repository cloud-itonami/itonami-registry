---
name: itonami-connector-contract-inspection
description: Inspect host-bound connector descriptors, consent and effects before an agent uses a projected tool.
metadata:
  hermes:
    version: 0.1.0
    author: cloud-itonami
    source: https://github.com/kotoba-lang/connector/tree/bc00554a064e72247ce64004a2497e5f3533aca0
    compatibility:
      hermes: '*'
      desktop: '*'
---

# itonami-connector-contract-inspection

1. Read the selected connector contract and its native tool schema. The connector model projects descriptors supplied by a host; its presence does not establish a transport server.
2. Resolve the actual adapter, caller session, capability binding and effective consent in the target host. Reject missing or mismatched bindings before proposing invocation.
3. Compare requested inputs, expected output and effects with the caller-authorized task. A descriptor or listed capability neither grants access nor proves endpoint availability.
4. If a bounded call is authorized, preserve its native refusal or outcome and record the actual host/runtime revision. Never translate a refused operation into a guessed success.
5. Return the resolved contract, effect boundary and evidence gap. Keep credentials, session data and application policy in the owning host.

Source contracts are pinned in itonami.json and catalogs/sources.json. Runtime implementations and existing profiles remain in their owning repositories.
