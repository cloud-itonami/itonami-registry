# kumitate MCP

MCP server (Streamable HTTP, JSON responses) for [kumitate](https://github.com/cloud-itonami/app-itonami-kumitate), the CircleCI-compatible itonami dapp. kumitate is written in Kotoba and built only with the Amu selfhost compiler, as a loaderless static image for aarch64-linux or x86_64-linux.

The tools are pure functions over the data the caller passes:

| tool | does |
|---|---|
| `kumitate_validate` | Checks a config.yml (2.1): YAML, structure, parameters, executors, commands, jobs and workflows. Every refusal has a named code. Orbs and `functions:` are refused as unresolved; nothing is fetched. |
| `kumitate_plan` | The processed pipeline for a branch or tag and pipeline parameters: the workflows that run, matrix jobs expanded, filters and when/unless decided, the requires DAG with levels, and parallel jobs and containers. |
| `kumitate_process` | The processed config as YAML, like `circleci config process`. |
| `kumitate_api_shapes` | The CircleCI API v2 Pipeline, Workflow and Job objects the pipeline would show when created. Ids are derived; nothing is sent to circleci.com. |
| `kumitate_local_plan` | Each job's steps in DAG order, for running them yourself. kumitate runs nothing. |
| `kumitate_runs` | Reads run records (API v2 items pages, or kumitate.runs.v1) and summarizes: statuses, failed jobs, success rate and mean duration per job, and flaky jobs. |
| `kumitate_runs_export` | Writes a run record as kumitate.runs.v1 or as API v2 items pages. Reading the result again gives the same record. |
| `kumitate_junit` | Aggregates JUnit XML reports: failing, flaky and slowest tests. DOCTYPE is refused. |

Nothing is sent anywhere, nothing is stored, and no job runs.

## Start the server

The owner builds the image (the repository README, "Kotoba gate") and starts it:

```sh
KEXE_ALLOW=37,38,39,43,44,46,47 KEXE_CAP_RESOURCES_43=127.0.0.1:8787 ./kumitate-aarch64-linux.elf serve 127.0.0.1:8787
```

The runtime opens only the granted address. The server answers `POST /mcp`. It refuses an `Origin` that is not localhost with 403, and returns 405 for GET and DELETE.

## Use from an itonami agent profile

```yaml
mcp_servers:
  kumitate:
    url: http://127.0.0.1:8787/mcp
```

The tools appear as `mcp__kumitate__kumitate_plan` and so on. A stdio transport is not available yet: the native runtime has no stdin (kotoba-lang/amu#1516).

Registering this entry enables nothing. A profile owner adds the `mcp_servers` entry.

Status: protocol-tested through itonami-agent's HTTP MCP client on fixture input, and the gate and fixtures pass on both targets. A model-driven agent turn has not been tested.
