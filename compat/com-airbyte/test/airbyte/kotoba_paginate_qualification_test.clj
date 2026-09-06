(ns airbyte.kotoba-paginate-qualification-test
  (:require [airbyte.main :as oracle]
            [clojure.test :refer [deftest is]]
            [kotoba.compiler.core :as compiler]
            [kotoba.compiler.ir :as compiler-ir]
            [kotoba.runtime :as runtime]
            [kotoba.wasm-exec :as wasm-exec]))

(def source-path "src/airbyte/paginate.kotoba")

(deftest q9-paginate-kernel-oracle-and-backends-agree
  (let [source (slurp source-path)
        forms (runtime/read-forms source :kotoba)
        reference-artifact (runtime/wasm-binary forms)
        compiler-artifact (compiler/compile-source source :wasm32-kotoba-v1
                                                   {:allow #{}})]
    (is (:kotoba.wasm/ok? reference-artifact))
    ;; main = has-more? 101 (clamp-limit (as-int 100)) -> 1 (true, i64-valued)
    (is (= 1 (wasm-exec/run-main (:kotoba.wasm/binary reference-artifact) [])
             (compiler-ir/execute (:kir compiler-artifact) 'main [])))
    ;; test-kernel is the kotoba-side bool parity probe over the full
    ;; decision surface: coerce -> clamp -> has-more across boundary cases.
    ;; The KIR executor materializes the (and ...) as its i64 truth (1).
    (is (= 1 (compiler-ir/execute (:kir compiler-artifact) 'test-kernel [])))
    (is (= #{} (get-in compiler-artifact [:hir :effects])))
    ;; Parity against the retained cljc oracle twins.
    (is (= [20 1 100 100] (mapv oracle/clamp-limit
                               [(oracle/as-int-kernel -5) 1 100 250])))
    (is (= [false true true] (mapv oracle/has-more-kernel? [20 21 250] [20 20 100])))
    (is (oracle/has-more-kernel? 101 (oracle/clamp-limit (oracle/as-int-kernel 100))))))
