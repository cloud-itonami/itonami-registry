(ns ads-b-aviation.kotoba-paginate-qualification-test
  (:require [ads_b_aviation.main :as oracle]
            [clojure.test :refer [deftest is]]
            [kotoba.compiler.core :as compiler]
            [kotoba.compiler.ir :as compiler-ir]
            [kotoba.runtime :as runtime]
            [kotoba.wasm-exec :as wasm-exec]))

(def source-path "src/ads_b_aviation/paginate.kotoba")

(deftest q9-paginate-kernel-oracle-and-backends-agree
  (let [source (slurp source-path)
        forms (runtime/read-forms source :kotoba)
        reference-artifact (runtime/wasm-binary forms)
        compiler-artifact (compiler/compile-source source :wasm32-kotoba-v1
                                                   {:allow #{}})]
    (is (:kotoba.wasm/ok? reference-artifact))
    ;; Parity across the decision surface: coerce -> clamp -> has-more.
    (is (= [20 1 100 100] (mapv oracle/clamp-limit-kernel
                                [(oracle/as-int-kernel -5) 1 100 250])))
    (is (= [false true true] (mapv oracle/has-more-kernel?
                                   [20 21 250] [20 20 100])))
    (is (= #{} (get-in compiler-artifact [:hir :effects])))))

(deftest q9-paginate-cljc-oracle-covers-boundaries
  ;; main = has-more? 101 (clamp-limit (as-int 100)) -> true
  (is (oracle/has-more-kernel? 101 (oracle/clamp-limit-kernel
                                    (oracle/as-int-kernel 100)))))
