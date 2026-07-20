;; Node-native (non-JVM, no Chicory) verification that customer.wasm --
;; kotoba.launcher's real `wasm emit` output for schema/customer.kotoba --
;; actually links and runs via the browser-native kgraph host-import port
;; (kotoba-lang/wasm-webcomponent's src/kgraph.js), the same import surface
;; wasm-webcomponent/test/verify-kgraph.mjs exercises against
;; kotoba-lang/kotoba's own JVM/Chicory fixture (ADR-2607198200).
;;
;; Assumes this repo (kotoba-lang/com-stripe) and kotoba-lang/wasm-webcomponent
;; are checked out as sibling paths under the same orgs/kotoba-lang/ parent
;; (the west manifest layout). Run from this directory: nbb verify_customer_wasm.cljs
(ns verify-customer-wasm
  (:require ["fs" :as fs]
            ["path" :as path]))

(def script-dir (path/dirname *file*))

(def kgraph-url
  (str "file://" (path/join script-dir ".." ".." "wasm-webcomponent" "src" "kgraph.js")))

(def wasm-path
  (path/join script-dir "customer.wasm"))

(def heap-base 2048)

(defn read-result [exports written]
  (let [buf (js/Uint8Array. (.-buffer (.-memory exports)) heap-base written)]
    (.decode (js/TextDecoder. "utf-8") buf)))

(-> (js/import kgraph-url)
    (.then
     (fn [kgraph-mod]
       (let [kgraphHostImports (.-kgraphHostImports kgraph-mod)
             bytes (fs/readFileSync wasm-path)
             store #js []
             memoryBox #js {}
             imports (kgraphHostImports store memoryBox)]
         (-> (js/WebAssembly.instantiate bytes #js {:kotoba imports})
             (.then
              (fn [result]
                (let [exports (.-exports (.-instance result))]
                  (set! (.-memory memoryBox) (.-memory exports))
                  ((aget exports "create-customers"))
                  (println "store after create-customers:" (js/JSON.stringify store))
                  (let [written ((aget exports "get-customer") heap-base 256)]
                    (println "get-customer(stripe_cus_0001) ->" (read-result exports written)))
                  (let [written ((aget exports "list-customers") heap-base 256)]
                    (println "list-customers() ->" (read-result exports written)))
                  (println "OK: customer.wasm (kotoba wasm emit output) ran end-to-end via native WebAssembly + kgraph.js -- no JVM/Chicory involved"))))
             (.catch (fn [e] (println "FAIL (instantiate/run):" (.-message e)) (js/process.exit 1)))))))
    (.catch (fn [e] (println "FAIL (import kgraph.js):" (.-message e)) (js/process.exit 1))))
