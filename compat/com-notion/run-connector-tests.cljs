#!/usr/bin/env nbb
;; nbb --classpath "src:test:../connector/src" run-connector-tests.cljs
(require '[clojure.test :as t] 'notion.connector-test 'notion.main-test)
(let [{:keys [fail error]} (t/run-tests 'notion.connector-test 'notion.main-test)]
  (js/process.exit (if (pos? (+ fail error)) 1 0)))
