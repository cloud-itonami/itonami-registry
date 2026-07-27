(ns amadeus-alt-a.kotoba-qualification-test
  (:require [amadeus_alt_a.main :as oracle]
            [clojure.test :refer [deftest is]]
            [kotoba.compiler.core :as compiler]
            [kotoba.compiler.ir :as compiler-ir]
            [kotoba.runtime :as runtime]
            [kotoba.wasm-exec :as wasm-exec]))

(def source-path "src/amadeus_alt_a/page_limit.kotoba")

(deftest q9-page-limit-oracle-and-backends-agree
  (let [source (slurp source-path)
        forms (runtime/read-forms source :kotoba)
        reference-artifact (runtime/wasm-binary forms)
        compiler-artifact (compiler/compile-source source :wasm32-kotoba-v1
                                                   {:allow #{}})
        reference-result (wasm-exec/run-main
                          (:kotoba.wasm/binary reference-artifact) [])
        compiler-result (compiler-ir/execute (:kir compiler-artifact) 'main [])]
    (is (:kotoba.wasm/ok? reference-artifact))
    (is (= 100 (oracle/page-limit 250)
           reference-result compiler-result))
    (is (= #{} (get-in compiler-artifact [:hir :effects])))))

(deftest q9-cljc-oracle-covers-boundaries
  (is (= [20 20 1 20 100]
         (mapv oracle/page-limit [-1 0 1 20 250]))))
