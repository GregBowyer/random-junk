;; Clojure program that solves problem 1 in the project euler 
;; problems

;; Gratuitous python version
;; sum((x for x in xrange(1, 1000) if (x % 5 == 0) or (x % 3 == 0)))

(defn sum-of-multiples [limit]
  "Find the sum of the given multiples that are > limit" 
  (reduce + (filter 
              #(or (zero? (rem % 3)) (zero? (rem % 5)))
              (range 1 limit))))

(sum-of-multiples 1000)
