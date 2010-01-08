; Of course this is bad clojure style, you would never do something
; that is so mutable on a global context

(ns greg.dht-test)

(add-classpath "file:///home/greg/projects/coherence/core/coherence/lib/coherence.jar")

(try 
  (def *dht* (. com.tangosol.net.CacheFactory (getCache "testCache")))
  (catch Exception e 
    ; Just for this I need the better error tracking
    ; Clojure by default will simply print the exception 
    ; rather than its associated stack
    (. e (printStackTrace))))

(print *dht*)

;; Some ultily functions to make life simpler
(defmacro get-grid [key] 
  "Gets an entity out of the global grid (sym *dht*)"
  `(. *dht* (get ~key)))

(defmacro put-grid [key value]
  "Puts random crap into the grid *note* only externables are distributed"
  `(. *dht* (put ~key ~value)))
