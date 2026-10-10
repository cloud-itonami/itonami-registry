---
name: itonami-compute-allocation-observation
description: Assess compute allocation from fresh capacity, egress, disk and contention measurements before proposing a bounded pilot.
metadata:
  hermes:
    version: 0.1.0
    author: cloud-itonami
    source: https://github.com/kotoba-lang/zap-proxy/tree/f0c18361293ddde8203f63e5786e5bb033b6429b
    compatibility:
      hermes: '*'
      desktop: '*'
---

# itonami-compute-allocation-observation

Bind the selected nodes, workload and observation budget. Read fresh owner capacity and demand receipts; historical node names, concurrency figures and storage sizes in a runbook are not current fleet facts.

Check actual egress, available disk/memory and competing resident processes before proposing model acquisition or placement. Peak loading/quantization memory can exceed final quantized weight size. A smaller on-disk artifact does not establish that acquisition will fit.

Separate advertised throughput from successful measured throughput, queue latency, failures and concurrency. Reuse existing trustworthy measurement receipts before sending another expensive benchmark. Any probe must stay within the caller-authorized runtime and resource budget.

Propose one bounded pilot with explicit demand, effect scope and success criterion, keeping CI and other owner workloads' policies intact. Return observed bottlenecks and uncertainty. This skill changes no route, schedule, allocation or running process.

Pinned derivation inputs are in itonami.json and catalogs/sources.json; owner runtimes and profiles are referenced, not imported.
