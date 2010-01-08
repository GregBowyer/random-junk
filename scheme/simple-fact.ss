(define (fac x)
  (if (= x 0) 1
    (* x
      (fac (- x 1)))))

(display (fac 12345))
