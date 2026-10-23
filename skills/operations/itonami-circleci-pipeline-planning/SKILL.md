---
name: itonami-circleci-pipeline-planning
description: Check a CircleCI config.yml and explain which jobs a branch or tag would run, in what order, with the kumitate MCP tools; summarize run records and JUnit reports the operator holds. Nothing runs and nothing connects to CircleCI.
metadata:
  hermes:
    version: 0.1.0
    author: cloud-itonami
    source: https://github.com/cloud-itonami/app-itonami-kumitate/tree/c4331fada15b590bc7489ad42e33e898d206d867
    compatibility:
      hermes: '*'
      desktop: '*'
---

# itonami-circleci-pipeline-planning

1. Confirm the input is a config.yml the operator provided (version 2.1). Do not fetch it from a repository or from circleci.com; kumitate has no network access beyond its own loopback listener.
2. Call `mcp__kumitate__kumitate_validate` with `config`. Report each `errors` entry with its `code` and `path`. For `config/orb-unresolved` or `config/function-unresolved`, say that orbs and functions are external code that kumitate does not fetch; do not guess what they do.
3. For a plan, ask which branch or tag the pipeline is for, and which pipeline parameters it gets. Call `mcp__kumitate__kumitate_plan` with `config`, `branch` or `tag`, and `parameters`. Present the workflows that run, the job levels (what runs in parallel), and every skipped job with its `reason`. Repeat every `plan/*-unresolved` warning: those decisions need a value that was not given.
4. If the operator wants the expanded config, call `mcp__kumitate__kumitate_process` and hand over `yaml`. If they want the API v2 objects, call `mcp__kumitate__kumitate_api_shapes`. Say that the ids are derived and that nothing was sent to CircleCI.
5. To run the jobs themselves, call `mcp__kumitate__kumitate_local_plan` and give the steps. The operator runs them on their own machine. Do not run them yourself.
6. For past runs, pass the downloaded API v2 JSON or kumitate.runs.v1 text to `mcp__kumitate__kumitate_runs`. Pass JUnit XML texts (one a run) to `mcp__kumitate__kumitate_junit`. Report the failed and flaky jobs and tests.

The tool contracts are pinned in itonami.json and catalogs/sources.json. The server lives in cloud-itonami/app-itonami-kumitate. The owner starts it, and it is enabled only by a profile owner's `mcp_servers` entry.
