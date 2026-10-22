---
name: itonami-sentry-error-triage
description: Triage Sentry error data an operator already holds with the mihari MCP tools, without connecting to Sentry.
metadata:
  hermes:
    version: 0.1.0
    author: cloud-itonami
    source: https://github.com/cloud-itonami/app-itonami-mihari/tree/8f2ec46a27910b3ccb082ec7029819e109b37949
    compatibility:
      hermes: '*'
      desktop: '*'
---

# itonami-sentry-error-triage

1. Confirm the input is data the operator provided (an envelope, event JSON or an `/events/` response). Do not fetch from sentry.io; mihari has no network access and no credentials.
2. Call `mcp__mihari__mihari_ingest_events` with `text` (and `project` when known). Report `events_count`, `skipped` item kinds and every `warnings` entry. Do not drop them.
3. For each issue, use the returned `level`, `count` and `userCount`. Call `mcp__mihari__mihari_decide` when the operator states a status change (for example "this was resolved in 1.4.0"), so the regression flag comes from mihari's rule rather than a guess.
4. Order the report by priority (high, medium, low), then by `lastSeen`. For each issue, cite `shortId`, `title`, `culprit` and the counts.
5. Say that the priority is mihari's documented rule on Sentry's vocabulary, not Sentry's internal algorithm. Say that nothing was sent or stored.

The tool contracts are pinned in itonami.json and catalogs/sources.json. The server lives in cloud-itonami/app-itonami-mihari and is enabled only by a profile owner's mcp_servers entry.
