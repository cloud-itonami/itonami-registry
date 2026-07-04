#!/usr/bin/env bash
# gpu_accelerator-compat — clj/bb test suite (clean-room compat actor; self-contained deps.edn project).
# Runs from the actor dir with its own src:tests classpath so it joins the fleet green-check.
set -euo pipefail
cd "$(dirname "$0")"
exec bb --classpath src:tests -e '(require (quote clojure.test) (quote gpu_accelerator.actor-test))(let [r (apply clojure.test/run-tests (quote [gpu_accelerator.actor-test]))](System/exit (if (zero? (+ (:fail r) (:error r))) 0 1)))'
