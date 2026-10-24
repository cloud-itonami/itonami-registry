# dougaka MCP

Stdio MCP server for [dougaka](https://github.com/cloud-itonami/app-itonami-dougaka), the timeline-to-ffmpeg-plan itonami dapp also published at https://itonami.cloud/app/dougaka/. The tools are pure functions over the text the caller passes:

| tool | does |
|---|---|
| `dougaka_validate` | Validates a timeline JSON (scene count 1..24, every scene has a frame, estimated duration within 120s). Returns named errors. |
| `dougaka_plan` | Builds the render plan: ordered segments with frame/voice/text, width/height/fps, bgm, plus a display-only ffmpeg script. |

Nothing is encoded, sent or stored. The decisions come from the same `.cljk` adapter as the browser app. It agrees with the wasm guest `aiueos/dougaka_core.cljk` on the repository's 21-row parity table; the guest itself is not loaded here.

## Use from an itonami agent profile

```yaml
mcp_servers:
  dougaka:
    command: kbb
    args: ["/absolute/path/to/app-itonami-dougaka/bin/dougaka-mcp"]
```

The tools appear as `mcp__dougaka__dougaka_validate` and `mcp__dougaka__dougaka_plan`. itonami-agent does not start MCP subprocesses on peer runs.

The first launch resolves the pinned `kotoba-lang/text` git dependency into `~/.gitlibs` (network) and a `.nbb/` cache in the checkout. Later launches only read.

Registering this entry enables nothing: a profile owner adds the `mcp_servers` entry.

Status: source-inspected and protocol-tested over stdio with raw JSON-RPC on synthetic fixtures plus a kbb stdio integration test. A model-driven agent turn has not been tested.
