# Slack Clean Room Actor

This actor provides a clean-room, API-compatible implementation of the Slack platform.

## Architecture
- **State:** Backed by Datomic for immutable, time-travel-capable record keeping.
- **Schema:** Defined in `schema/slack.kotoba`.
- **Execution:** Runs in `Py Kotodama WASM`, intercepting inbound REST requests.

## Provenance

Relocated 2026-07-05 from `etzhayyim/root/20-actors/slack-compat` to
`kotoba-lang/com-slack` per the org-taxonomy library-placement rule (any
library/substrate code belongs in `kotoba-lang`, ADR-2606302300), following
the same relocation pattern as `kami-nv-compat` (ADR-2607020130). See
ADR-2607041500 for the full ~1,027-repo migration plan and naming convention.

## Connector

`slack.connector` exposes a client of the **real** Slack API as tools with an
OAuth profile and per-tool scopes — the connector plane of ADR-2608097000.
`slack.main` above is the opposite direction: Slack's API implemented here.

| tool | effect | scope |
|---|---|---|
| `slack_list_channels` | read | `channels:read` |
| `slack_channel_history` | read | `channels:history` |
| `slack_list_users` | read | `users:read` |
| `slack_post_message` | **write** | `chat:write` |

A notifier gets `chat:write` and cannot read the channel it posts to.

### The behaviour worth knowing about

**Slack answers HTTP 200 with `{"ok": false, "error": "..."}`.** A connector
that only checked the status code would normalize `missing_scope` into an empty
channel list, and the caller would conclude the workspace has no channels.
`normalize` turns `ok:false` into an error value carrying Slack's `needed` and
`provided` scopes — the scope an operator actually has to grant.

```sh
nbb --classpath "src:test:../connector/src" run-connector-tests.cljs   # 12 tests, 34 assertions
nbb --classpath "src:../connector/src:../fmt/src" emit-connector-edn.cljs
```
