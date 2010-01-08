(ns ctr 
 (:require (clojure stacktrace inspector) (clojure.contrib repl-utils))
 (:require (clojure stacktrace inspector) (clojure.contrib repl-utils pprint))
 (:import com.oracle.coherence.common.identifiers.Identifier)
 (:import com.shopzilla.site.service.clickrate.domain.ClickThroughRate))

(defn setup-env[name] 
  (doseq [tuple
    [ '("com.sun.management.jmxremote" "true")
      '("tangosol.coherence.management" "all")
      '("tangosol.coherence.log.level" "2")
      '("tangosol.pof.config" "ctr-pof-config.xml")
      '("tangosol.pof.enabled" "true")
      '("tangosol.coherence.distributed.localstorage" "false")

      `("tangosol.coherence.override" ~(format "tangosol-coherence-override-local-%s.xml" name))
      `("tangosol.coherence.cacheconfig" ~(format "ctr-%s-cache-config.xml" name))
      `("visualvm.display.name" ~(format "'%s Coherence Clojure Console'" name))]]

    (let [[name value] tuple]
      (prn (format "Set %s --> %s" name value))
      (. System (setProperty name value))
      (assert (= value (. System (getProperty name)))))))
 
;(def *grid* (. com.tangosol.net.CacheFactory (getCache "Impressions")))

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

 (. *grid* (invoke 10 (create-basic-processor)))

