(ns ctr 
 (:require (clojure stacktrace inspector) (clojure.contrib repl-utils))
 (:require clojure.contrib.pprint)
 (:require clojure.contrib.duck-streams))

(defn setup-env [name port]
  (doseq [tuple
    [ '("com.sun.management.jmxremote" "true")
      '("tangosol.coherence.management" "all")
      '("tangosol.coherence.log.level" "2")
      '("tangosol.coherence.distributed.localstorage" "false")
      '("tangosol.pof.enabled" "true")
      '("tangosol.pof.config" "ctr-pof-config.xml")
      `("tangosol.coherence.clusterport" ~(str port))
      `("tangosol.coherence.override" ~(format "tangosol-coherence-override-%s-dev.xml" name))
      `("tangosol.coherence.cacheconfig" ~(format "clickrate-%s-cache-config.xml" name))
      `("visualvm.display.name" ~(format "'%s-Clojure-Console'" name))]]

    (let [[name value] tuple]
      (prn (format "Set %s --> %s" name value))
      (. System (setProperty name value))
      (assert (= value (. System (getProperty name)))))))

(defn bind-env [env-name port]
  "Shortcut function to bind to the given cluster"
  (do
    (ns ctr)
    (setup-env env-name port)
    (. com.tangosol.net.CacheFactory ensureCluster)))
 
(defn get-grid [gridname]
  (. com.tangosol.net.CacheFactory (getCache gridname)))

(defn dump-grid [grid file]
  (clojure.contrib.duck-streams/write-lines file
    (map #(let [[k v] %] (format "%s=%s" k (bean v))) grid)))

(defn print-grid [gridname]
  "Prints out an entire grid to stdout"
  (map #(let [[k v] %]
          (print "\n")
          (clojure.contrib.pprint/pprint k)
          (clojure.contrib.pprint/pprint (bean v))
          (print "--------------------------------------------------\n"))
       (get-grid gridname)))

(comment
(defn create-basic-processor [] 
  "Create a basic processor to be attached to a grid for processing"
  (proxy [com.tangosol.util.processor.AbstractProcessor com.tangosol.io.pof.PortableObject] []
    (process [entry] 
             (let [key (. entry getKey) value (. entry getValue)]
               (prn (format "Key: %s Value: %s" key value))
               (if (. entry (isPresent)) value 
                 (new ClickThroughRate key))))
    (readExternal [reader] )
    (writeExternal [writer] )))

 (. *grid* (invoke 10 (create-basic-processor))))
