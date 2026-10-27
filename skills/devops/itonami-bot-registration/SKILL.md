---
name: itonami-bot-registration
description: Register an itonami bot agent profile from a Hermes session.
version: 0.1.0
author: Jun Kawasaki, Hermes Agent
license: MIT
platforms:
- macos
- linux
metadata:
  hermes:
    tags:
    - itonami
    - bot
    - profile
    - registration
    - yakuwari
    related_skills:
    - bot-profile-scaffold
    - itonami-business-bots
    version: 0.1.0
    author: Jun Kawasaki, Hermes Agent
    source: https://github.com/kotoba-lang/itonami-agent/tree/491a2bc81e16b24987fac6fc388737fbb73332f6
    compatibility:
      hermes: '*'
      desktop: '*'
---

# itonami bot agent の登録（hermes agent から）

脆弱性スキャン / self-healing 系など「itonami bot」を hermes セッションから
設計・登録する手順。実測は 2026-10-21（itonami-agent コード読解 + registry 実走）。

## When to Use

- 「itonami bot profile として作って / 登録して」という指示
- itonami agent CLI（`bin/itonami-agent`）で走る bot を新設・改造
- manifest/agent-registry.edn への agent 追加
- Don't use for: Hermes cron bot のみ（それは `bot-profile-scaffold`）。
  grok-bots DO 常駐（それは `itonami-business-bots`）。

## 構造（実測の正本）

1. **2 CLI の分離**（kotoba-lang/itonami-agent/AGENTS.md が正本）:
   - itonami agent CLI: profile store `~/.itonami/profiles/<name>/`（`ITONAMI_DIR`）、
     推論は `itonami.edn` `:inference`（murakumo 専用、`:deny-hosts ["openrouter.ai"]`）
   - hermes agent CLI: `~/.hermes/profiles/<name>/`、config.yaml `model:`（openrouter 等）
   - **Hermes profile に murakumo/mishima を使わない。itonami.edn を Hermes は読まない。**
   - 移動: `itonami-agent profile import <p> [--from DIR]`（hermes→itonami）、
     `profile export`（逆。`:scheduler :itonami` なら `gateway.parked` を付けて二重 tick 防止）

2. **profile バンドル**（両 CLI が読む共通フォーマット）:
   `SOUL.md` / `profile.yaml`（description 必須・ASCII のみ）/ `config.yaml` /
   `.env` / `secrets.command` / `yakuwari.edn`（権限の正本）/ `itonami.edn` /
   `cron/jobs.json` / `scripts/` / `skills/`。
   state（sessions/ workspace/ memories/ logs/ cron/output/ 等）は store 個別で移動しない。

3. **itonami.edn**（schema `cloud.itonami.profile.v2`、検証は
   `itonami-agent profile check <p>`、実装 `src/itonami/agent/manifest.cljk`）:
   - 必須: `:itonami/schema` `:profile/id`（`^[a-z0-9][a-z0-9_-]{0,63}$`）/
     `:profile/hermes-compatible true` / `:runtime {:engine :itonami-agent
     :scheduler :hermes|:itonami|:launchd}` / `:placement {:mode :local|:p2p
     :inference-rail :murakumo|:kotoba|:itonami-p2p}` / `:state` map /
     `:bundle {:cid "b…" :files N}` / `:capabilities` vector / `:cron?` bool
   - 推論: `:inference {:rails [:murakumo] :authorities ["api.murakumo.cloud"]
     :deny-hosts ["openrouter.ai"]}`。`:placement :inference-rail` は
     `:inference :rails` の中に無いと error。
   - v2 の org キー（`:agent/kind :org/world :org/path :org/github :org/unit
     :org/layer :invocation :awai/business :ids :authority`）は
     `itonami-agent profile organize <p> --all --registry manifest/agent-registry.edn`
     が registry から投影する。手で書かない。
   - 意思決定語彙: `:autonomous :voice-required :approval-required :blocked`
     （旧語 `:self-executing :propose :forbidden` は warn 付きで読める）。
     yakuwari が読まない語は **fail closed（:blocked）**。

4. **yakuwari.edn が権限の正本**。`itonami.edn` の `:capabilities` は写しで権限を
   与えない。`:authority {:default-decision :approval-required :source :yakuwari
   :ref "yakuwari.edn"}` は organize が投影。yakuwari 無し bot は提案のみ。
   形式（spec 5 項目 + capabilities）:
   `{:yakuwari/id :x :yakuwari/project "org/repo" :yakuwari/objective "1 文"
   :yakuwari/scale {:min 1 :desired 1 :max 1}
   :yakuwari/runners [{:runner :hermes :weight 1}]
   :yakuwari/capabilities [{:capability :code.change :decision :autonomous :note "…"} …]}`
   - capabilities は **map でなく vector**。未記載 = :blocked。

5. **registry 登録** — `manifest/agent-registry.edn`（com-junkawasaki/root）は
   **索引であって権限ではない**。1 entry:
   `{:agent/id "name" :agent/kind :worker|:role-bot|:steward|:unit|:organism
   :agent/runtime :hermes|:cloud-itonami-app :org/world :awai|:kotoba|:etzhayyim|:host
   :org/path [:etzhayyim :awai :cloud-itonami] :org/unit … :org/parent …
   :org/github "cloud-itonami" :invocation :resident|:on-demand
   :posture #{:autonomous} :did "did:key:z6Mk…" :yakuwari/id "name"
   :home {:repo "org/repo"} :source {:repo "org/repo" :via "hermes-profile-repos"}
   :lifecycle :active :description "…"}`
   - 登録は root worktree + branch + PR で（共有 root checkout を直接編集しない）。
   - 権限の grant は manifest/yakuwari.kotoba（fleet/profile-spawn 等）から。
     索引に在るから許可、はしない。

## 手順

1. 既存確認: registry で `:agent/id` / 役割重複を grep（同役割の未稼働 profile が
   無いか。あれば新設でなく実装改善）。`kbb --backend sci scripts/repo-search.cljk <語>`
   と concept-lookup で資産確認（既有 repo を使う）。
2. home repo を決める（`cloud-itonami/ao-bot-fleet` が fleet 系の既定。対象 repo が
   決まればそれ）。`<repo>/hermes/profiles/<name>/` を正本にバンドルを書く。
3. yakuwari.edn（権限表、先に）→ 検証は nbb + kotoba-lang/yakuwari spec
   （bot-profile-scaffold の手順 2、tag reader + em dash の罠に注意）。
4. itonami.edn を v1/v2 骨架で書き `itonami-agent profile check <name>` を通す →
   `profile organize <name> --all --registry manifest/agent-registry.edn --dry-run`
   で投影内容を確認。
5. registry entry を root worktree で追加して PR。merge 後 organize で投影。
6. host へ: `hermes profile create <name> --clone-from <template>`（template は
   同種 profile）→ `itonami-agent profile import <name>` で itonami store へ。
   cron job は profile 個別に登録（`bot-profile-scaffold` の cron 節）。
7. 稼働確定: `itonami-agent profile adopt <name>`（itonami が cron を tick、
   Hermes は parked）または scheduler を hermes のまま。手動 fire 1 回で
   ledger/報告を確認してから常駐へ。

## Pitfalls

- `:bundle :cid` は CIDv1 base32（`b` 始まり）必須。`profile check` が落ちる最頻出。
- `:agent/runtime :cloud-itonami-app` は cloud-itonami-app 上で動く agent のみ
  （現状 8 件は etzhayyim/tamaki）。dapps 上で動かすならこの値 + app 側の
  bot registry への載せが必要。hermes 実行は `:hermes`。
- `did:key:z6Mk…` は ed25519。生成は itonami-agent identity（seed 経由）。
  既存 entry の did を流用しない。
- config.yaml の model を変えると既存 cron job の provider snapshot drift で
  fire が拒否される（`drift_skip`）。job を作り直す。
- 旧 skill と同名の重複登録は二重 cron になる。1b（bot-profile-scaffold）の
  未稼働 profile 走査を必ず回す。

## Verification

- `itonami-agent profile check <name>` が error 0（warn は人が見る）
- `profile organize --dry-run` の投影が registry entry と一致
- registry entry の PR が merge され、`profile check --all` が緑
- 手動 fire 1 回で SOUL の報告書式どおりの出力（未測定を成功と報告していない）
