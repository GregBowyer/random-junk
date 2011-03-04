(define (pascals row col)
  (cond ((= col 1) 1)
        ((= row col) 1)
        (else 
         (+ (pascals (- row 1) (- col 1))
            (pascals (- row 1) col)))))

