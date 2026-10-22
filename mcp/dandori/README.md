# dandori MCP

Stdio MCP server for [dandori](https://github.com/cloud-itonami/app-itonami-dandori), the Linear-compatible itonami dapp also published at https://itonami.cloud/sites/app/dandori/. The tools are pure functions over the data the caller passes:

| tool | does |
|---|---|
| `dandori_import` | Normalizes a Linear CSV or GraphQL JSON export into teams and Linear-shaped issues. |
| `dandori_export` | Writes normalized issues back as Linear CSV or GraphQL JSON. import → export → import round-trips on the repository fixtures. |
| `dandori_cycle_progress` | Computes completed scope per mille, excluding canceled issues and weighting unestimated ones. |
| `dandori_check_estimate` | Checks an estimate against Linear's scales (exponential, fibonacci, linear, tShirt), with the zero and extended options. |
| `dandori_sla_status` | Reports ok, medium-risk, high-risk or breached for SLA timestamps. |

Nothing is sent to Linear or anywhere else, and nothing is stored. The decisions come from the same `.cljk` adapter as the browser app. It agrees with the wasm guest `aiueos/dandori_core.cljk` on the repository's 73-row parity table; the guest itself is not loaded here.

## Use from an itonami agent profile

```yaml
mcp_servers:
  dandori:
    command: kbb
    args: ["/absolute/path/to/app-itonami-dandori/bin/dandori-mcp"]
```

The tools appear as `mcp__dandori__dandori_import` and so on. itonami-agent does not start MCP subprocesses on peer runs.

The first launch resolves the pinned `kotoba-lang/text` git dependency into `~/.gitlibs` (network) and a `.nbb/` cache in the checkout. Later launches only read.

Registering this entry enables nothing: a profile owner adds the `mcp_servers` entry.

Status: source-inspected and protocol-tested through the itonami-agent MCP client (`discover`/`call`) on synthetic fixtures. A model-driven agent turn has not been tested.
