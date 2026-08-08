#!/usr/bin/env nbb
;; Regenerate connector.edn from the descriptor.
;;   nbb --classpath "src:../connector/src" emit-connector-edn.cljs
;; connector_test asserts the committed file still matches.
(require '[clojure.pprint :as pp]
         '[connector.declare :as decl]
         '[slack.connector :as c])

(let [fs (js/require "fs")
      edn (with-out-str
            (pp/pprint (decl/declaration c/provider
                                         {:namespace "slack.connector"
                                          :var "provider"
                                          :authority "90-docs/adr/2608097000-connector-plane-one-repo-per-connector.edn"})))]
  (.writeFileSync fs "connector.edn" edn)
  (println "wrote" (count edn) "bytes to connector.edn"))
