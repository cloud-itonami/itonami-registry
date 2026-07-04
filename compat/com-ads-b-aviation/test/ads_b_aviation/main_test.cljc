(ns ads_b_aviation.main-test
  "Contract + behavioral test for the ads_b_aviation-compat L4 actor (cljc port).
  Runs under babashka: `bb test`. Stronger than the py static contract test —
  exercises CRUD / pagination / filtering / expansion / validation against the
  in-memory Datom-log store."
  (:require [clojure.test :refer [deftest is testing run-tests]]
            [ads_b_aviation.main :as m]))

(def entities ["Object" "Position" "Observation" "Scene" "Float" "Station"])

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
        [rec status] (m/handle-create s "Object" {:designator "A1234" :type "Aircraft"})]
    (is (= 201 status))
    (is (= "A1234" (:designator rec)))
    (is (re-find #"^adsbavia_obj_" (:id rec)))
    (is (= [rec 200] (m/handle-get s "Object" (:id rec) {})))))

(deftest validation-required-and-unknown
  (let [s (m/fresh-store)]
    (testing "missing required field -> 400"
      (is (= 400 (second (m/handle-create s "Object" {})))))
    (testing "unknown field -> 400"
      (is (= 400 (second (m/handle-create s "Object" {:designator "x" :type "y" :bogus 1})))))))

(deftest coercion
  (let [s (m/fresh-store)
        [rec _] (m/handle-create s "Position" {:lat "12.5" :lon "-122.3" :objectId "obj1"})]
    (is (= 12.5 (:lat rec)))
    (is (= -122.3 (:lon rec)))
    (let [[scene _] (m/handle-create s "Scene" {:satellite "Sentinel" :cloudCover "45.7"})]
      (is (= 45.7 (:cloudCover scene))))
    (let [[float _] (m/handle-create s "Float" {:lat "37.1" :lon "140.5" :parkDepthM "3000.0"})]
      (is (= 37.1 (:lat float)))
      (is (= 3000.0 (:parkDepthM float))))))

(deftest list-filter-and-paginate
  (let [s (m/fresh-store)]
    (dotimes [i 25] (m/handle-create s "Object" {:designator (str "D" i) :type (if (even? i) "Aircraft" "Ship")}))
    (let [[body _] (m/handle-list s "Object" {})]
      (is (= 20 (:count body)))            ; default limit
      (is (true? (:has_more body)))
      (is (= 25 (:total body))))
    (let [[body _] (m/handle-list s "Object" {:type "Aircraft"})]
      (is (= 13 (:total body))))))         ; even i in 0..24 -> 13

(deftest expansion
  (let [s (m/fresh-store)
        [obj _] (m/handle-create s "Object" {:designator "O1" :type "Aircraft"})
        [pos _] (m/handle-create s "Position" {:lat 10.0 :lon 20.0 :objectId (:id obj)})
        [got _] (m/handle-get s "Position" (:id pos) {:expand "objectId"})]
    (is (= obj (:objectId_obj got)))))

(deftest update-and-delete
  (let [s (m/fresh-store)
        [rec _] (m/handle-create s "Object" {:designator "old" :type "Aircraft"})
        [upd _] (m/handle-update s "Object" (:id rec) {:designator "new"})]
    (is (= "new" (:designator upd)))
    (is (= (:id rec) (:id upd)))           ; id immutable
    (is (= 200 (second (m/handle-delete s "Object" (:id rec)))))
    (is (= 404 (second (m/handle-get s "Object" (:id rec) {}))))))

(deftest eavt-fact-emission
  (testing "datomic EAVT mapping preserved: ads_b_aviation.<Entity>/<field>"
    (let [facts (m/emit-facts "Object" {:id "adsbavia_obj_x" :designator "D" :type "Aircraft"})]
      (is (= "D" (get facts "ads_b_aviation.Object/designator")))
      (is (= "adsbavia_obj_x" (get facts "ads_b_aviation.Object/id"))))))

(deftest healthz
  (is (= [{:status "ok" :actor "ads_b_aviation-compat" :tier "L4" :entities entities} 200] (m/healthz))))

#?(:clj (defn -main [& _]
          (let [{:keys [fail error]} (run-tests 'ads_b_aviation.main-test)]
            (System/exit (if (pos? (+ fail error)) 1 0)))))
