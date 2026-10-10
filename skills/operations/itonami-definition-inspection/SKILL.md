---
name: itonami-definition-inspection
description: Inspect definitions and dependents with the owner symbol-index CLI before reviewing an agent repository change.
metadata:
  hermes:
    version: 0.1.0
    author: cloud-itonami
    source: https://github.com/kotoba-lang/symbol-index/tree/fea038bc8c12c0f1074fa09cec7a0f2fcff62cc2
    compatibility:
      hermes: '*'
      desktop: '*'
---

# itonami-definition-inspection

1. Bind the checkout, requested symbol and current owner index status. Inspect the installed CLI version and documented commands before using it.
2. Use symbol-index find with --in and --exact to locate the definition; outline the file or namespace and show the selected definition. Quote paths and symbols as data.
3. Use find --dependents --depth with a bounded depth and closure for the relevant dependency slice. Verify ambiguous matches against the committed source.
4. Preserve exit 0 as hits, exit 1 as observed zero hits and exit 2 as refusal such as a missing or ambiguous root. Zero stale-index hits do not establish absence of callers.
5. Report definition, actual callers and freshness limits. Structural identical markers do not prove byte-identical artifacts; build and prune write index state and require owner authorization.

Source contracts are pinned in itonami.json and catalogs/sources.json. Runtime implementations and existing profiles remain in their owning repositories.
