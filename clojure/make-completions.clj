(def completions 
  (reduce concat (map (fn [p] (keys (ns-publics (find-ns p))))
    '(clojure.core clojure.inspector clojure.main clojure.set clojure.stacktrace clojure.template clojure.test clojure.walk clojure.xml clojure.test ))))

(comment
duck-streams classpath combinatorics agent-utils 
                   accumulators cond condition java-utils jar macro-utils macros map-utils math javadoc.browse 
                   dataflow datalog fnmap json.read json.write monads monadic-io-streams profile repl-ln repl-utils 
                   seq-utils shell-out set str-utils stream-utils pprint trace swing-utils)

(with-open [f (java.io.BufferedWriter. (java.io.FileWriter. (str (System/getenv "HOME") "/.clj_completions")))]
  (.write f (apply str (interleave completions (repeat "\n")))))
