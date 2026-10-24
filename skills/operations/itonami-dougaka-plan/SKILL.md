---
name: itonami-dougaka-plan
description: Build an ffmpeg render plan from a timeline JSON an operator already holds with the dougaka MCP tools, without encoding or generating anything.
metadata:
  hermes:
    version: 0.1.0
    author: cloud-itonami
    source: https://github.com/cloud-itonami/app-itonami-dougaka/tree/6606a317649572183eac7b6585e215ecc379618b
    compatibility:
      hermes: '*'
      desktop: '*'
---

# itonami-dougaka-plan

1. Confirm the input is data the operator provided (a timeline JSON with scenes/assets/lines). Do not fetch footage, voices or music; dougaka has no network access and no credentials.
2. Call `mcp__dougaka__dougaka_validate` with `text`. Report every `errors` entry. If `ok` is false, stop and explain which scene frames are missing — do not guess a plan.
3. When valid, call `mcp__dougaka__dougaka_plan` with `text` (and `aspect` when the operator names portrait or landscape). Report the `summary` and the segment count.
4. Hand over the `ffmpeg` script as the assembly recipe. Say that it is display-only: nothing was encoded, and the operator runs it on their own machine with their own ffmpeg.
5. Say that the plan shape matches the dougaka production service's render plan, not its encoding or generation. Say that nothing was sent or stored.

The tool contracts are pinned in itonami.json and catalogs/sources.json. The server lives in cloud-itonami/app-itonami-dougaka and is enabled only by a profile owner's mcp_servers entry.
