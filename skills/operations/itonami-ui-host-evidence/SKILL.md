---
name: itonami-ui-host-evidence
description: Bind portable UI automation plans to actual host snapshots, execution transcripts and screenshot receipts.
metadata:
  hermes:
    version: 0.1.0
    author: cloud-itonami
    source: https://github.com/kotoba-lang/devtools/tree/888b6cf681690443ef86d49313cb2ef5a1c4ec01
    compatibility:
      hermes: '*'
      desktop: '*'
---

# itonami-ui-host-evidence

Read the current devtools element/scene, plan, transcript and screenshot-artifact contracts. Select the actual host adapter; the portable library does not capture pixels or inject events by itself.

Bind the target session/page, element identity and observation time. Resolve a target against a fresh semantic snapshot and distinguish visible/enabled elements from unmatched or stale targets. Preserve host-specific capability refusals.

Execute only the caller-authorized host operations and record step status, native outcomes and actual screenshot references where needed. A synthetic input value or planned click is not an executed event; screenshot format/dimensions metadata is not pixel evidence.

Evaluate the requested UI result from the actual host outputs, retain accessibility findings and missing observations, and store private session artifacts only in the authorized host evidence store. Export permitted opaque references or aggregates. Report plan, execution and observed result separately.

Pinned derivation inputs are in itonami.json and catalogs/sources.json; owner runtimes and profiles are referenced, not imported.
