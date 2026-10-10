# Registry maintenance

Read llms.txt, llms-full.txt and docs/adr/0001-registry-ownership.md. Keep existing bot profiles in their owning repositories. Do not synchronize, activate or grant permissions as a consequence of publishing entries.

Preserve Hermes manifest and SKILL.md shapes. Keep Itonami extension fields in itonami.json and catalogs/. Generate index.json with scripts/build_index.py and check with --check. Run schema validation and integrity tests before publication. New entries require pinned source references, clear authority and honest runtime validation status.

Keep kotoba-registry entries as external references, never duplicate entries. Credentials, logs, sessions, memories, machine-specific configuration and ledger contents must not enter this repository. All local repositories and scratch belong under the user-authorized github forest. Preserve unrelated WIP.
