; Recursive process [correct]
(require (lib "trace.ss"))
(define (f n)
  (cond ((< n 3) n)
        (else (+
               (f (- n 1))
               (* 2 (f (- n 2)))
               (* 3 (f (- n 3)))))))

; Iterative process
(define (f-it n)
  (define (f-iter a b c n)
    (if (< n 3) a
        (f-iter (+ a (* 2 b) (* 3 c)) a b (- n 1))))
  (f-iter 2 1 0 n))

;why ? [n -> 5]

; for starts we are required to work out the three multiplications of n
; we encode the fact that we need to remove -1 -2 -3 from n in the starting numbers by
; making a (the (* 1 n)) - 1 behind n at the start; as we accumilate through the iteration
; that variable remains in spirit 1 behind n, the same applies for the -2 and -3

; with that taken into account we reduce the problem to (+ a (* 2 b) (* 3 c))

;(f-iter (+ 2 (* 2 1) (* 3 0)) 2 1 (- n 1))
;-> (f-iter (+ 2 2 0) 2 1 4)
;-> (f-iter 4 2 1 4)

;(f-iter (+ 4 (* 2 2) (* 3 1)) 4 2 (- n 1))
;-> (f-iter (+ 4 4 3) 4 2 3)
;-> (f-iter 11 4 2 3)

;(f-iter (+ 11 (* 2 4) (* 3 2)) 11 4 (- n 1))
;-> (f-iter (+ 11 8 6) 11 4 2)
;-> (f-iter 25 11 4 2)

;!cond (< n 3) thus -> 25