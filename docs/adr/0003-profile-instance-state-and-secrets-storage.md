# ADR 0003 Profile instance storage: definitions, state, secrets

Status: accepted, 2026-10-18. Builds on ADR 0001 and ADR 0002.

Owner instruction: 「個別の実体となる profile は どこに保存するのがいいかな? itonami profile で公開で動いているのは, 別にセッションも公開でいいんだけど..., 個人で itonami bot profile を立てて、動かす人は... 暗号化して, datalad, ipfs pinかなー?」 — confirmed with 「yes」 to recording the split here.

## Decision

A profile instance is three layers with different storage, not one folder in one
place. Where a layer goes depends on whether the owner publishes it.

| Layer | Contents | Published instance | Personal instance |
|---|---|---|---|
| Definitions | `SOUL.md`, `profile.yaml`, `config.yaml`, `cron/jobs.json`, `skills/`, `scripts/`, `itonami.edn`, `yakuwari.edn` | owning repository `hermes/profiles/<name>/`, pinned by a `profile` entry here (ADR 0002) | the owner's own git repository; registered here only if the owner publishes it |
| State | `sessions/`, `logs/`, `memories/`, `workspace/`, ledgers | any ordinary data plane the owner chooses (a data directory in the owning repository, a datalake); the registry still refuses sessions and logs | DataLad dataset: git-annex content with a B2 remote, encrypted annex; the encrypted annex object may be pinned on IPFS / the kotobase bytes plane |
| Secrets | API keys, tokens, wallet signers | credential store only | credential store only |

1. **Definitions are git, small and pinned.** A registry `profile` entry pins one
   commit of the owning repository and verifies files by sha256 and `sha256-tree`
   (ADR 0002). Registration grants nothing; the installer rebinds accounts,
   grants and schedule. A personal definition the owner does not publish is not
   registered — the registry is an index, not a mandatory home.
2. **State never enters the registry**, and never mixes into definition
   repositories. Small semantic EDN stays git-tracked in its owning dataset;
   bulk and personal state is a DataLad dataset (git-annex + B2 is the standing
   large-binary route). Personal state uses an encrypted annex and may pin the
   encrypted objects on IPFS / the kotobase bytes plane (`ipfs://` identity,
   `https://{cid}.ipfs.kotobase.net` bytes) for distribution and durability.
3. **Secrets enter no repository and no annex, not even encrypted.** The
   credential store is the source of truth; `secrets.edn` carries references
   only. This holds for the encrypted-annex path as well: encryption at rest is
   not a licence to commit credentials.

## Properties the personal path must keep

- **Encrypted annex hides bodies, not metadata.** File names, sizes, structure
  and update cadence stay observable. If the fact that a person runs a profile
  is itself sensitive, pseudonymise annex paths and keep the mapping under a
  separate key.
- **IPFS publication is ciphertext only, and non-deterministic.** Publishing
  plaintext pins it effectively forever. Deterministic encryption (same
  plaintext, same CID) correlates holders of the same profile; use per-user and
  per-file keys with random nonces so CIDs do not join users.
- **Content addressing is not access control.** Anyone who learns a CID can
  fetch it from any pinning gateway. The only controls are which pins exist and
  who holds the key, so key lifecycle *is* access control, and destroying the
  key is the deletion mechanism (crypto erasure).

## Layout

```
<owning repo>/hermes/profiles/<name>/   # definitions only; registry pin target
profiles-state/                         # DataLad dataset (encrypted annex for personal)
  <name>/sessions/ logs/ memories/ workspace/ ledger/
secrets -> credential store             # never in the dataset
```

A runtime on the aiueos VM materialises definitions from one pinned registry
commit (checksum-verified), fetches state from the annex remotes, and holds no
secrets of its own.

## Consequences

- A published bot may share its sessions openly on a data plane; that is the
  owner's disclosure choice and does not relax the registry's refusal of
  sessions, logs, credentials and state.
- This ADR decides destinations; it migrates nothing. Existing host runtime
  state (tens of gigabytes of sessions, logs and ledgers) is operational record
  and is not bulk-deleted before its destinations and verification exist.
- Personal definitions follow the same three-layer split: if the definition
  itself is private, keep it in a private repository or in the encrypted annex —
  do not register it here.
