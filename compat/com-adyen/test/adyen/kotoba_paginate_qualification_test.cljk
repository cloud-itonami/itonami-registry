(ns adyen.kotoba-paginate-qualification-test
  (:require [adyen.main :as oracle]
            [clojure.test :refer [deftest is]]
            [kotoba.compiler.core :as compiler]
            [kotoba.compiler.ir :as compiler-ir]
            [kotoba.runtime :as runtime]
            [kotoba.wasm-exec :as wasm-exec]))

(def source-path "src/adyen/paginate.kotoba")

(deftest q9-paginate-kernel-oracle-and-backends-agree
  (let [source (slurp source-path)
        forms (runtime/read-forms source :kotoba)
        reference-artifact (runtime/wasm-binary forms)
        compiler-artifact (compiler/compile-source source :wasm32-kotoba-v1
                                                   {:allow #{}})]
    (is (:kotoba.wasm/ok? reference-artifact))
    (is (= 1 (wasm-exec/run-main (:kotoba.wasm/binary reference-artifact) [])))
    ;; test-kernel is the kotoba-side bool parity probe over the full
    ;; decision surface: coerce -> has-more across boundary cases.
    (is (= 1 (compiler-ir/execute (:kir compiler-artifact) 'test-kernel [])))
    (is (= #{} (get-in compiler-artifact [:hir :effects])))))

(deftest q9-paginate-kernel-cljc-oracle-covers-boundaries
  (is (= [0 0 7] (mapv oracle/as-int-kernel [-5 0 7])))
  (is (= [false true true true]
         (mapv oracle/has-more-kernel? [20 21 250 101] [20 20 100 100]))))
