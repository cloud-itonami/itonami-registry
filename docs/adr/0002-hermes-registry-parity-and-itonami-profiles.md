# ADR 0002 Hermes registry parity and Itonami profiles

Status: accepted, 2026-10-14. Amends ADR 0001.

Owner instruction: 「Hermes Profile の対応は Itonami も Itonami profile にしましょう。また Itonami Registry も作って」 — the Itonami Registry as the full equivalent of the Hermes registry, with a type for Itonami profiles.

## Terms (same as Hermes)

Hermes defines the terms in `website/docs/user-guide/profiles.md` and `bot-mode.md`; Itonami takes the same definitions.

| Term | Meaning |
|---|---|
| Profile | The persistent home of an assistant's configuration and data. An **Itonami profile is a Hermes profile**: the same layout (SOUL.md, profile.yaml, config.yaml, skills/, cron/, scripts/) |
| Agent | The running assistant using a profile; the Itonami agent is the Hermes agent (cloud-itonami-app ADR-0143) |
| Bot | A profile presented in the roster (name, avatar, role) with one canonical Bot Chat. Every Bot is a profile; not every profile is a Bot |
| Messaging bot | A platform account (Telegram, Discord, Slack …) connected through a gateway |
| Subagent | A child assistant for one delegated task |

## Decision

1. **A fifth type, `profile`.** This supersedes ADR 0001's "no fifth manifest type".
   - Its manifest (`schemas/itonami/profile.schema.json`) pins a profile folder in its owning repository to one commit.
   - It lists every file with sha256 and size, plus a `sha256-tree` checksum computable from the manifest alone.
   - The files are never copied: ADR 0001's ownership rule stands.
   - The registry refuses credentials, USER.md, MEMORY.md, sessions, logs and state.
   - Every file must also be pinned in `catalogs/sources.json`, and the owner's inventory row records the registration.
   - `itonami.json` grants nothing. Accounts, connector grants, wallet signer and approval policy are rebound by the installer, and cron arrives disabled.
2. **Hermes registry parity.**
   - `categories.json` and `models.json` are generated in the Hermes registry shapes.
   - `models/<provider>.json` is validated against the vendored upstream `models.schema.json`, which is added to provenance. The initial provider is murakumo.
   - The submission flow is pull requests with CI (`CONTRIBUTING.md`, PR template).
3. **Federation of the Hermes registry.**
   - `catalogs/federated/hermes-registry.json` snapshots fathah/hermes-registry's index at a pinned commit: metadata only, upstream checksums kept, `indexSha256` recorded.
   - Identities are qualified as `hermes-registry/<type>/<id>`.
   - CI checks the snapshot against upstream.
4. **A static site and API instead of an app server.**
   - `scripts/build_site.py` writes `index.html` and `api/v1/{index,categories,models,registries}.json`, plus `api/v1/entries/<registry>/<type>/<id>.json`.
   - GitHub Pages publishes them (`pages.yml`).
   - Everything served is a file derived from git, so a client can verify it, and there is no database to trust.

## Consequences

- An Itonami profile can be installed either as an Itonami Bot or, by copying the pinned folder, as a Hermes profile. Both directions keep credentials home.
- One catalog lists Itonami and Hermes entries side by side without copying Hermes content.
- Download counters and server-side search, which the Hermes app has, are not provided.
