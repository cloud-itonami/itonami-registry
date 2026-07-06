# Reddit Clean Room Actor

Clean-room API-compatible implementation of the reddit platform, backed by Datomic and Py Kotodama WASM.

## Architecture
- **State:** Backed by Datomic for immutable, time-travel-capable record keeping.
- **Schema:** Defined in `schema/reddit.kotoba` — `Subreddit`, `User`, `Post`,
  `Comment`, `Vote`. Id prefixes follow Reddit's own `fullname` convention
  where one exists (`t5_`=subreddit, `t2_`=account, `t3_`=link, `t1_`=comment
  — see [Reddit's API docs](https://www.reddit.com/dev/api#fullnames));
  `Vote` has no real Reddit `thing` type (voting is a verb, `POST /api/vote`,
  not a stored resource) so it gets a made-up prefix here.
- **Execution:** Runs in `Py Kotodama WASM`, intercepting inbound REST requests.
- **Not modeled:** Reddit's own auth surface (`POST /api/v1/access_token`,
  OAuth2 script/installed-app flow) isn't a resource, so it isn't one of the
  generic CRUD routes below — see `src/reddit/main.cljc`'s `routes` comment.

## Provenance

Relocated 2026-07-05 from `etzhayyim/root/20-actors/reddit-compat` to
`kotoba-lang/com-reddit` per the org-taxonomy library-placement rule (any
library/substrate code belongs in `kotoba-lang`, ADR-2606302300), following
the same relocation pattern as `kami-nv-compat` (ADR-2607020130). See
ADR-2607041500 for the full ~1,027-repo migration plan and naming convention.
