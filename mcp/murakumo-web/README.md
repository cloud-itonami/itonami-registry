# Murakumo Web MCP

The server implementation stays in the pinned kotoba-lang/murakumo repository. Install that checkout with its documented dependencies; do not download a single script and assume the whole runtime is installed. Supply Node.js, kbb and the owner-managed web-plane configuration.

Replace ${MURAKUMO_REPO} in manifest.args with the chosen checkout's absolute path. Pass node and that script path to the client's native stdio MCP configuration. The registry does not interpolate configuration or modify any client settings.

initialize, ping and tools/list can inspect the protocol without calling the fleet. Tool calls can access nodes, send queries to third parties, store fetched artifacts, retry remote writes, or provision remote configuration. In particular web_sync and web_provision are writes. Use a client-enforced allowlist appropriate to the owner's authorization; the manifest does not provide a read-only mode. Credentials remain in the runtime's existing operator-managed storage, never in the registry or tool arguments.

The published validation receipt covers initialization and tool discovery only. It does not establish kbb execution, node health, fetching, artifact storage or live provisioning.
