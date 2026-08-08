# Notion Clean Room Actor

This actor provides a clean-room, API-compatible implementation of the Notion platform.

## Architecture
- **State:** Backed by Datomic for immutable, time-travel-capable record keeping.
- **Schema:** Defined in `schema/notion.kotoba`.
- **Execution:** Runs in `Py Kotodama WASM`, intercepting inbound REST requests.

## Provenance

Relocated 2026-07-05 from `etzhayyim/root/20-actors/notion-compat` to
`kotoba-lang/com-notion` per the org-taxonomy library-placement rule (any
library/substrate code belongs in `kotoba-lang`, ADR-2606302300), following
the same relocation pattern as `kami-nv-compat` (ADR-2607020130). See
ADR-2607041500 for the full ~1,027-repo migration plan and naming convention.

## Connector

`notion.connector` exposes a client of the **real** Notion API as tools —
the connector plane of ADR-2608097000. `notion.main` above is the opposite
direction: Notion's API implemented here.

| tool | effect |
|---|---|
| `notion_search` | read |
| `notion_get_page` | read |
| `notion_get_block_children` | read |
| `notion_query_database` | read |
| `notion_create_page` | **write** |

### Notion has no scopes, and this connector says so

Notion's authorization endpoint takes no `scope` parameter: what an integration
may touch is fixed when it is created and by which pages a person shares with
it. The descriptor declares `:scopes? false`, no tool declares a scope, and
`connector.validate` **rejects** one declared anyway — a consent screen printing
scopes Notion will ignore is worse than one printing none.

The cost is worth stating plainly: **a Notion grant cannot be narrowed by this
plane.** Enabling `notion_search` and enabling `notion_create_page` request
exactly the same access, and there is a test asserting that. The narrowing that
does exist lives in Notion — page-by-page sharing and the integration's
capabilities — and an operator has to do it there.

Two other Notion behaviours are encoded rather than left to callers: the token
endpoint accepts only `client_secret_basic`, and the `Notion-Version` header is
pinned (omitting it lets the server pick, which is how a normalizer starts
silently reading a different shape). A page's title is found by property
**type**, never by the name `Name`, which whoever built the database can rename.

```sh
nbb --classpath "src:test:../connector/src" run-connector-tests.cljs   # 12 tests, 36 assertions
nbb --classpath "src:../connector/src" emit-connector-edn.cljs
```
