;;; Example in clojure (and ergo lisp) of the simple resource example 
;;; that is set forth in the STM paper "Composable Memory Transactions"
;;; 
;;; Largely this is just translating the Haskell into clojure such that I
;;; can learn some Haskell and get a handle on what the paper discusses
;;; I _feel_ that clojure vs haskell wrt immutability and STM behaviour is 
;;; close enough to make the mapping fairly reasonable
;;;
;;; @author Greg Bowyer

;; The initial reference, defined in Haskel as 
;; type Resource = TVar Int
;; (That is a resource is a STM reference which is ultimately an int)
;; See how this is technically global, thread unsafe right !
(def resource (ref 1))

;; Implementation of the Haskell example putR defined as 
;; putR = R <- R+1
;; Note I am aware of clojures commute function, I want to 
;; do this as close to the Haskell version as possible

;; The theory holds that you should be able to bang this from 
;; a million threads and *never* see a lost update or incorrect invariant
(defn putR [] 
  (dosync
    (+ 1 @resource)))


