# com-unity-api-services

Repository identity is the reverse DNS form of the canonical Unity campaign
management API host, `services.api.unity.com`. The `unity-ads` MCP service and
the existing `unity_ads` schema namespace remain stable protocol identifiers.

Clean-room API-compatible implementation of the unity_ads vertical monopoly, backed by Datomic and Py Kotodama WASM.

## Responsibility and maturity

This repository is the intended domain boundary for Unity Ads API access,
browser fallback, authentication, capability discovery, provider-native errors
and a `unity-ads.*` MCP server. Cross-network campaign policy and budget
approval belong to `cloud-itonami-isic-7310` / `gftdcojp/cloud-itonami`.

Current maturity is **schema-only**. It must not be presented as an operational
Unity Ads connector until authenticated read and receipt-backed mutation tests
exist.

The repository now includes a dry-run-first unity-ads MCP adapter for the
services.api.unity.com/advertise/v1 API. Live use requires a Unity service
account with Advertise API Campaigns Editor, organization ID, app ID and
account currency. It remains non-executable until authenticated verification.
