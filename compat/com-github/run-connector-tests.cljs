#!/usr/bin/env nbb
;; nbb --classpath "src:test:../connector/src" run-connector-tests.cljs
;;
;; Separate from `clojure -M:test`: the connector namespaces are portable .cljc
;; over an nbb-friendly kernel, while this repository's other tests
;; (github.workflow.harness) are JVM. One runner for both would need a JVM to
;; check a namespace that does not require one.
(require '[clojure.test :as t] 'github.connector-test 'github.main-test 'github.workflow-test)
(let [{:keys [fail error]} (t/run-tests 'github.connector-test 'github.main-test 'github.workflow-test)]
  (js/process.exit (if (pos? (+ fail error)) 1 0)))
