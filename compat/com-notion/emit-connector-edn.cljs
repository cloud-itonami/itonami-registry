#!/usr/bin/env nbb
;; nbb --classpath "src:../connector/src" emit-connector-edn.cljs
(require '[clojure.pprint :as pp]
         '[connector.declare :as decl]
         '[notion.connector :as c])

(let [fs (js/require "fs")
      edn (with-out-str
            (pp/pprint (decl/declaration c/provider
                                         {:namespace "notion.connector"
                                          :var "provider"
                                          :authority "90-docs/adr/2608097000-connector-plane-one-repo-per-connector.edn"})))]
  (.writeFileSync fs "connector.edn" edn)
  (println "wrote" (count edn) "bytes to connector.edn"))
