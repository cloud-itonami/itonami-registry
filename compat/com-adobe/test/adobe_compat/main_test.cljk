(ns adobe-compat.main-test
  "Contract + behavioral test for the adobe-compat L4 actor (cljc port).
  Runs under babashka: `bb test`. Stronger than the py static contract test —
  exercises CRUD / pagination / filtering / expansion / validation against the
  in-memory Datom-log store."
  (:require [clojure.test :refer [deftest is testing run-tests]]
            [adobe-compat.main :as m]))

(def entities ["Project" "File" "Frame" "Component" "Comment" "Export"])

(deftest schema-has-all-entities
  (is (= (set entities) (set m/entities))))

(deftest full-crud-per-entity
  (testing "every entity exposes POST/GET-list/GET-one/PATCH/DELETE"
    (doseq [{:keys [plural]} m/entity-specs]
      (let [base (str "/v1/" plural)
            paths (set (map (juxt :method :path) m/routes))]
        (is (contains? paths ["POST" base]))
        (is (contains? paths ["GET" base]))
        (is (contains? paths ["GET" (str base "/{id}")]))
        (is (contains? paths ["PATCH" (str base "/{id}")]))
        (is (contains? paths ["DELETE" (str base "/{id}")]))))
    (is (= 30 (count m/routes)))))

(deftest create-and-get
  (let [s (m/fresh-store)
        [rec status] (m/handle-create s "Project" {:name "Atlas"})]
    (is (= 201 status))
    (is (= "Atlas" (:name rec)))
    (is (re-find #"^adobe_pro_" (:id rec)))
    (is (= [rec 200] (m/handle-get s "Project" (:id rec) {})))))

(deftest validation-required-and-unknown
  (let [s (m/fresh-store)]
    (testing "missing required field -> 400"
      (is (= 400 (second (m/handle-create s "Project" {})))))
    (testing "unknown field -> 400"
      (is (= 400 (second (m/handle-create s "Project" {:name "x" :bogus 1})))))))

(deftest coercion
  (let [s (m/fresh-store)
        [rec _] (m/handle-create s "File" {:name "a" :version "7"})]
    (is (= 7 (:version rec)))
    (let [[frame _] (m/handle-create s "Frame" {:name "f" :width "12.5"})]
      (is (= 12.5 (:width frame))))
    (let [[c _] (m/handle-create s "Comment" {:body "hi" :resolved "true"})]
      (is (true? (:resolved c))))))

(deftest list-filter-and-paginate
  (let [s (m/fresh-store)]
    (dotimes [i 25] (m/handle-create s "Project" {:name (str "p" i) :teamId (if (even? i) "t1" "t2")}))
    (let [[body _] (m/handle-list s "Project" {})]
      (is (= 20 (:count body)))            ; default limit
      (is (true? (:has_more body)))
      (is (= 25 (:total body))))
    (let [[body _] (m/handle-list s "Project" {:teamId "t1"})]
      (is (= 13 (:total body))))))         ; even i in 0..24 -> 13

(deftest expansion
  (let [s (m/fresh-store)
        [proj _] (m/handle-create s "Project" {:name "P"})
        [file _] (m/handle-create s "File" {:name "F" :version 1 :projectId (:id proj)})
        [got _] (m/handle-get s "File" (:id file) {:expand "projectId"})]
    (is (= proj (:projectId_obj got)))))

(deftest update-and-delete
  (let [s (m/fresh-store)
        [rec _] (m/handle-create s "Project" {:name "old"})
        [upd _] (m/handle-update s "Project" (:id rec) {:name "new"})]
    (is (= "new" (:name upd)))
    (is (= (:id rec) (:id upd)))           ; id immutable
    (is (= 200 (second (m/handle-delete s "Project" (:id rec)))))
    (is (= 404 (second (m/handle-get s "Project" (:id rec) {}))))))

(deftest eavt-fact-emission
  (testing "datomic EAVT mapping preserved: adobe.<Entity>/<field>"
    (let [facts (m/emit-facts "Project" {:id "adobe_pro_x" :name "n"})]
      (is (= "n" (get facts "adobe.Project/name")))
      (is (= "adobe_pro_x" (get facts "adobe.Project/id"))))))

(deftest update-coercion
  ;; CONFIRMED BUG regression: handle-update never ran field values through
  ;; coerce-field the way handle-create does, so updating a :bool/:int/:float
  ;; field with a raw string (plausible from a JSON request body) silently
  ;; stored the wrong type instead of coercing it.
  (let [s (m/fresh-store)
        [rec _] (m/handle-create s "File" {:name "a" :version "7"})
        [updated _] (m/handle-update s "File" (:id rec) {:version "9"})]
    (is (= 9 (:version updated))))
  (let [s (m/fresh-store)
        [rec _] (m/handle-create s "Frame" {:name "f" :width "12.5"})
        [updated _] (m/handle-update s "Frame" (:id rec) {:width "20.5"})]
    (is (= 20.5 (:width updated))))
  (let [s (m/fresh-store)
        [rec _] (m/handle-create s "Comment" {:body "hi" :resolved "true"})
        [updated _] (m/handle-update s "Comment" (:id rec) {:resolved "false"})]
    (is (false? (:resolved updated)))))

(deftest healthz
  (is (= [{:status "ok" :actor "adobe-compat" :tier "L4" :entities entities} 200] (m/healthz))))

#?(:clj (defn -main [& _]
          (let [{:keys [fail error]} (run-tests 'adobe-compat.main-test)]
            (System/exit (if (pos? (+ fail error)) 1 0)))))
