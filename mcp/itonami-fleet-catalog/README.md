# Itonami fleet catalog MCP

The current pinned bin/itonami-mcp is the guest-Wasm stdio host. It declares **fleet_search only**; fleet_call and the leftover JVM resident business/payment tools are not on this connection. Searches read bundled directory metadata, not the network. An endpoint value is not a health measurement or invocation grant.

Separately prepare the pinned owner checkout with its kbb/Node dependencies, owner-built target/amu/mcp_main.wasm and resources/itonami-fleet-catalog.edn. The guest loader requires a positive guest main before opening stdio; a source checkout alone is insufficient. Resolve ITONAMI_APP_REPO before configuring the client. Do not replace owner artifact admission/build receipts with the registry source hash.

This is a source-inspected connection scaffold. Compiled guest startup, client interpolation, successful tools/list and live behavior have not been tested. No resident store, client configuration, profile or scheduler is changed by catalog publication. The descriptor in catalogs/tools.json is pinned to this launcher, not to the older JVM adapter.
