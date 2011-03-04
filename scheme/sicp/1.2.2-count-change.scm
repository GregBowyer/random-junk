(require (lib "trace.ss"))

(define (count-change amount)
    (cc amount 5))

(define (cc amount coinage)
    (cond ((= amount 0) 1)
          ((or (< amount 0) (= coinage 0)) 0)
          (else (+ (cc amount
                       (- coinage 1))
                   (cc (- amount
                          (first-denomination coinage))
                       coinage)))))
(define (first-denomination coinage)
    (cond
      ((= coinage 1) 1)
      ((= coinage 2) 5)
      ((= coinage 3) 10)
      ((= coinage 4) 25)
      ((= coinage 5) 50)))

(trace count-change)
(trace cc)
(trace first-denomination)
(count-change 10)
;292

