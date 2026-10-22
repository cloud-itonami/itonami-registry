# mihari MCP

Stdio MCP server for [mihari](https://github.com/cloud-itonami/app-itonami-mihari), the Sentry-compatible itonami dapp also published at https://itonami.cloud/sites/app/mihari/. The tools are pure functions over the text the caller passes:

| tool | does |
|---|---|
| `mihari_ingest_events` | Groups a Sentry envelope, event JSON or `/events/` response into Sentry-shaped issues. Drops IP addresses, request headers, cookies and emails before grouping. |
| `mihari_decide` | Applies mihari's priority rule, and the status transition with its regression flag. |

Nothing is sent to Sentry or anywhere else, and nothing is stored. The decisions come from the same `.cljk` adapter as the browser app. It agrees with the wasm guest `aiueos/mihari_core.cljk` on the repository's 47-row parity table; the guest itself is not loaded here.

## Use from an itonami agent profile

```yaml
mcp_servers:
  mihari:
    command: kbb
    args: ["/absolute/path/to/app-itonami-mihari/bin/mihari-mcp"]
```

The tools appear as `mcp__mihari__mihari_ingest_events` and `mcp__mihari__mihari_decide`. itonami-agent does not start MCP subprocesses on peer runs.

The first launch resolves the pinned `kotoba-lang/text` git dependency into `~/.gitlibs` (network) and a `.nbb/` cache in the checkout. Later launches only read.

Registering this entry enables nothing: a profile owner adds the `mcp_servers` entry.

Status: source-inspected and protocol-tested through the itonami-agent MCP client (`discover`/`call`) on synthetic fixtures. A model-driven agent turn has not been tested.
