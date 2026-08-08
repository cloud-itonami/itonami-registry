#!/usr/bin/env nbb
;; nbb --classpath "src:test:../connector/src" run-connector-tests.cljs
(require '[clojure.test :as t] 'notion.connector-test)
(let [{:keys [fail error]} (t/run-tests 'notion.connector-test)]
  (js/process.exit (if (pos? (+ fail error)) 1 0)))
