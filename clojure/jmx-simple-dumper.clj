(ns jmx-dumper
  (:require [clojure.contrib.jmx :as jmx])
  (:require [clojure.contrib.command-line :as cmd-line]))

(cmd-line/with-command-line *command-line-args*
  "JMX Dumper, dumps JMX Mbeans"
  [[server s "Hostname of server to connect to"]
   [port p "JMX port of server to connect to"]
   [mbean m "MBean path to query"]
   [attr a "Attribute to query"]
   [element e "Element of an attribute to extract"]]
  
  (jmx/with-connection {:host server, :port port}
    (println
      (if attr
          (let [jmx-mbean (jmx/read mbean attr)]
            (if element 
              (get jmx-mbean (keyword element))
              jmx-mbean))
        (jmx/mbean mbean)))))
