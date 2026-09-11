(ns github.workflow-test
  (:require [clojure.test :refer [deftest is]]
            [github.workflow :as workflow]))

(def repo-scope {:owner "kotoba-lang" :repo "demo"})

(def fixture
  {[:get "/orgs/kotoba-lang"] {:login "kotoba-lang"}
   [:get "/repos/kotoba-lang/demo"] {:id 1 :name "demo"}
   [:get "/repos/kotoba-lang/demo/issues?state=all&per_page=100"]
   [{:id 10 :number 1 :title "Work" :state "open"}
    {:id 11 :number 2 :title "PR shadow" :state "open" :pull_request {}}]
   [:get "/repos/kotoba-lang/demo/pulls?state=all&per_page=100"]
   [{:id 11 :number 2 :title "Ship" :state "open"}]
   [:get "/repos/kotoba-lang/demo/actions/workflows?per_page=100"] {:workflows [{:id 20 :name "ci"}]}
   [:get "/repos/kotoba-lang/demo/actions/runs?per_page=100"]
   {:workflow_runs [{:id 21 :name "ci" :status "completed" :conclusion "success"}]}
   [:get "/repos/kotoba-lang/demo/commits/HEAD/check-runs?per_page=100"]
   {:check_runs [{:id 22 :name "test" :status "completed" :conclusion "success"}]}
   [:post "/graphql"]
   {:data {:organization {:projectsV2 {:nodes [{:id "P1" :number 1 :title "Roadmap" :closed false}]}}
           :repository {:projectsV2 {:nodes []}}}}})

(deftest full-harness-roundtrip
  (let [snapshot (workflow/execute-plan (workflow/fixture-transport fixture) repo-scope)
        health (workflow/health snapshot)]
    (is (= "kotoba.github.workflow.v0" (:schema snapshot)))
    (is (= "kotoba-lang/demo" (get-in snapshot [:scope :graph])))
    (is (= 1 (count (:projects snapshot))))
    (is (= 1 (count (:issues snapshot))))
    (is (= 1 (count (:pull-requests snapshot))))
    (is (= {:projects 1 :open-issues 1 :open-pulls 1 :failed-checks 0}
           (:counts health)))
    (is (:ready? health))))

(deftest fail-closed-on-partial-api
  (is (thrown? #?(:clj clojure.lang.ExceptionInfo :cljs js/Error)
               (workflow/execute-plan (workflow/fixture-transport {}) repo-scope))))

(deftest public-organization-identity
  (let [profile {:id "gftdcojp" :name "Gftd Japan 株式会社"
                 :domain "gftd.co.jp" :operator-email "jun@gftd.group"}
        snapshot (workflow/with-organization-profile {} profile)]
    (is (= profile (:business-organization snapshot)))
    (is (thrown? #?(:clj clojure.lang.ExceptionInfo :cljs js/Error)
                 (workflow/organization-profile (assoc profile :operator-email "invalid"))))))
