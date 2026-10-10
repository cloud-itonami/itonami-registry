# Supplemental discovery

These files supplement the Hermes-format index. tools.json identifies tools by provider and native input schema; it is not a tool installer or an authority grant. sources.json pins derivation inputs, with hashes of the original files, not copies of profiles. external-registries.json describes immutable references that need a federation-aware consumer. Generic Hermes clients are not expected to consume these Itonami extensions.

 inventory.json surveys public default-branch filename markers and records selected/deferred ownership decisions. Its snapshot commit differs from a curated entry sourceCommit when that entry intentionally retains an earlier pinned derivation. Private repositories appear only as aggregate counts. Full tree survey does not mean every source file was semantically reviewed.
