# Portable user-test MCP

This is a source-inspected connection scaffold, with four native tool contracts in catalogs/tools.json. Validation and planning produce contracts; evaluation scores supplied outcomes. The owning runtime does not operate a browser or recruit participants. The host owns private evidence and must preserve human, synthetic and recipe evidence classes.

Install the pinned public user-test checkout and its deps.edn :mcp dependencies separately, with a JVM-capable kbb. Resolve USER_TEST_ENTRY to this checksum-verified artifact folder and USER_TEST_REPO to the clean absolute owner checkout before configuring the client. The Python launcher refuses a wrong revision or dirty tracked/untracked files, then sets the owner's working directory and execs kbb -M:mcp. It does not install dependencies or change files. Dependency resolution by the owning runtime may access the network; provision the target appropriately.

The launcher refusal paths and source/schema integrity are checked. Successful MCP startup, client interpolation and target behavior have not been tested. Do not infer browser, participant consent or runtime authority from this catalog.
