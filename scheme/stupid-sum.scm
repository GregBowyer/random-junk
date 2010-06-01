; Stupid sum, I did this all on my own :P
; its basically a foldr

(define (sum li)
    (if (null? li) 0
      ; CAR / CDR by any other name
      (+ (first li) (sum (rest li)))))
