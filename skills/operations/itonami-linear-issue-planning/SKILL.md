---
name: itonami-linear-issue-planning
description: Plan and check Linear issues an operator already exported with the dandori MCP tools, without connecting to Linear.
metadata:
  hermes:
    version: 0.1.0
    author: cloud-itonami
    source: https://github.com/cloud-itonami/app-itonami-dandori/tree/dbe623ba539af93101e2b8bba1cf9b563cb0d0e8
    compatibility:
      hermes: '*'
      desktop: '*'
---

# itonami-linear-issue-planning

1. Confirm the input is an export the operator provided (Linear CSV or GraphQL JSON). Do not call linear.app; dandori has no network access and no credentials.
2. Call `mcp__dandori__dandori_import` with `text` (format `auto` unless the operator names it). Report every `warnings` entry, and the teams with their workflow states and estimate settings.
3. For cycle progress, pass the issues' `state_type` and `estimate` to `mcp__dandori__dandori_cycle_progress`. State the `unestimated_weight` you used and that canceled issues are excluded from scope.
4. Check each estimate with `mcp__dandori__dandori_check_estimate`, using the team's scale, zero and extended settings from the import. List the invalid ones with the `allowed` values.
5. For SLA risk, call `mcp__dandori__dandori_sla_status` with an explicit `now` the operator agreed to. Do not assume the wall clock.
6. If the operator wants a file back, call `mcp__dandori__dandori_export` and hand over the `text`. Say that it was not written to Linear.

The tool contracts are pinned in itonami.json and catalogs/sources.json. The server lives in cloud-itonami/app-itonami-dandori and is enabled only by a profile owner's mcp_servers entry.
