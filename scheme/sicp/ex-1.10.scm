(define (ACK x y)
  "Defines the ackerman function, suitable for feeding in grahams number :P"
  (cond ((= y 0) 0)
		((= x 0) (* 2 y))
		((= y 1) 2)
		(else (ACK (- x 1)
				   (ACK x (- y 1))))))

#|
Q: What are the values of the following expressions
|#	    

(ACK 1 10)
(ACK 0 (ACK 1 9))
(ACK 0 (ACK 0 (ACK 1 8)))
(ACK 0 (ACK 0 (ACK 0 (ACK 1 7))))
(ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 1 6)))))
(ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 1 5))))))
(ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 1 4)))))))
(ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 1 3))))))))
(ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 1 2)))))))))
(ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 1 1))))))))))
(ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 1 (cond ((= 1 1) 2))))))))))
(ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 2)))))))))
(ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 4))))))))
(ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 8)))))))
(ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 16))))))
(ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 32)))))
(ACK 0 (ACK 0 (ACK 0 (ACK 0 64))))
(ACK 0 (ACK 0 (ACK 0 128)))
(ACK 0 (ACK 0 256))
(ACK 0 512)
1024

;The value is: 1024

(ACK 2 4)
(ACK 1 (ACK 2 3))
(ACK 1 (ACK 1 (ACK 2 2)))
(ACK 1 (ACK 1 (ACK 1 (ACK 2 1))))
(ACK 1 (ACK 1 (ACK 1 (ACK 1 (cond ((= 1 1) 2))))))
(ACK 1 (ACK 1 (ACK 1 2))))
(ACK 1 (ACK 1 (ACK 0 (ACK 1 1))))
(ACK 1 (ACK 1 (ACK 0 (cond ((= 1 1) 2)))))
(ACK 1 (ACK 1 (ACK 0 2)))
(ACK 1 (ACK 1 4))
(ACK 1 (ACK 0 (ACK 1 3)))
(ACK 1 (ACK 0 (ACK 0 (ACK 1 2))))
(ACK 1 (ACK 0 (ACK 0 (ACK 0 (ACK 1 1)))))
(ACK 1 (ACK 0 (ACK 0 (ACK 0 (cond ((= 1 1) 2))))))
(ACK 1 (ACK 0 (ACK 0 (ACK 0 2))))
(ACK 1 (ACK 0 (ACK 0 4)))
(ACK 1 (ACK 0 8))
(ACK 1 16)
(ACK 0 (ACK 1 15))
(ACK 0 (ACK 0 (ACK 1 14)))
(ACK 0 (ACK 0 (ACK 0 (ACK 1 13))))
(ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 1 12)))))
(ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 1 11))))))
(ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 1 10)))))))
(ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 1 9))))))))
(ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 1 8)))))))))
(ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 1 7))))))))))
(ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 1 6)))))))))))
(ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 1 5))))))))))))
(ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 1 4)))))))))))))
(ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 1 3))))))))))))))
(ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 1 2)))))))))))))))
(ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 1 1))))))))))))))))
(ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (cond ((= 1 1) 2))))))))))))))))
(ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 2)))))))))))))))
(ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 4))))))))))))))
(ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 8)))))))))))))
(ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 16))))))))))))
(ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 32)))))))))))
(ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 64))))))))))
(ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 128)))))))))
(ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 256))))))))
(ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 512)))))))
(ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 1024))))))
(ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 2048)))))
(ACK 0 (ACK 0 (ACK 0 (ACK 0 4096))))
(ACK 0 (ACK 0 (ACK 0 8192)))
(ACK 0 (ACK 0 16384))
(ACK 0 32768)
65536

; The value is 65536

(ACK 3 3)
(ACK 2 (ACK 3 2))
(ACK 2 (ACK 1 (ACK 3 1)))
(ACK 2 (ACK 1 (cond ((= 1 1) 2))))
(ACK 2 (ACK 1 2))
(ACK 2 (ACK 0 (ACK 1 1)))
(ACK 2 (ACK 0 (cond ((= 1 1) 2))))
(ACK 2 (ACK 0 2))
(ACK 2 4)

; see answer for (ACK 2 4)
(ACK 2 4)
(ACK 1 (ACK 2 3))
(ACK 1 (ACK 1 (ACK 2 2)))
(ACK 1 (ACK 1 (ACK 1 (ACK 2 1))))
(ACK 1 (ACK 1 (ACK 1 (ACK 1 (cond ((= 1 1) 2))))))
(ACK 1 (ACK 1 (ACK 1 2))))
(ACK 1 (ACK 1 (ACK 0 (ACK 1 1))))
(ACK 1 (ACK 1 (ACK 0 (cond ((= 1 1) 2)))))
(ACK 1 (ACK 1 (ACK 0 2)))
(ACK 1 (ACK 1 4))
(ACK 1 (ACK 0 (ACK 1 3)))
(ACK 1 (ACK 0 (ACK 0 (ACK 1 2))))
(ACK 1 (ACK 0 (ACK 0 (ACK 0 (ACK 1 1)))))
(ACK 1 (ACK 0 (ACK 0 (ACK 0 (cond ((= 1 1) 2))))))
(ACK 1 (ACK 0 (ACK 0 (ACK 0 2))))
(ACK 1 (ACK 0 (ACK 0 4)))
(ACK 1 (ACK 0 8))
(ACK 1 16)
(ACK 0 (ACK 1 15))
(ACK 0 (ACK 0 (ACK 1 14)))
(ACK 0 (ACK 0 (ACK 0 (ACK 1 13))))
(ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 1 12)))))
(ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 1 11))))))
(ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 1 10)))))))
(ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 1 9))))))))
(ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 1 8)))))))))
(ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 1 7))))))))))
(ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 1 6)))))))))))
(ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 1 5))))))))))))
(ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 1 4)))))))))))))
(ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 1 3))))))))))))))
(ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 1 2)))))))))))))))
(ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 1 1))))))))))))))))
(ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (cond ((= 1 1) 2))))))))))))))))
(ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 2)))))))))))))))
(ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 4))))))))))))))
(ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 8)))))))))))))
(ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 16))))))))))))
(ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 32)))))))))))
(ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 64))))))))))
(ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 128)))))))))
(ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 256))))))))
(ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 512)))))))
(ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 1024))))))
(ACK 0 (ACK 0 (ACK 0 (ACK 0 (ACK 0 2048)))))
(ACK 0 (ACK 0 (ACK 0 (ACK 0 4096))))
(ACK 0 (ACK 0 (ACK 0 8192)))
(ACK 0 (ACK 0 16384))
(ACK 0 32768)
65536

; The value is 65536

#|
Consider the following procedures where ACK is the procedure defined above.

(define (f n) (ACK 0 n))
(define (g n) (ACK 1 n))
(define (h n) (ACK 2 n))
(define (k n) (* 5 n n))

Give concise mathematical definitions for the functions computed by the procedures for postive integers
for instance:

	;#<procedure:k> -> 5n²
|#

;#<procedure:f> -> 2n

;#<procedure:g> -> 2^n

;#<procedure:h> -> 2^{h(n-1)} with h(0)=0 h(1)=2
