#R rosetta stone

# Lisp (scheme) + Python translations

# Operators + simple functions

2 + 2 # → python 2 + 2, lisp (+ 2 2)
1.8 + 0.1 # → python 1.8 + 0.1, lisp (+ 1.8 0.1) NOTE appears inexact
2 / 2 # → python 2 / 2, lisp (/ 2 2)
2 * 2 # → python 2 * 2, lisp (* 2 2)
2 ^ 2 # → python 2 ** 2, lisp (expt 2 3)

sqrt(2) # → python math.sqrt(2), lisp(sqrt 2)
exp(1) # → python math.exp(2), lisp(exp 2) NOTE eulers constant

# Assignment [mutable, dynamic types]
x <- 10 / 2 # → python x = 10 / 2, lisp (declare x (/ 10 2))
x = 10 / 2 # Same, but less common syntax

-1 + 0i # → python -1 + 0j, lisp (imag-part -1+0i)

# Datastructures

# Lists (vectors)
c(1, 2, 3, 4, 5, 6) # → python [1, 2, 3, 4, 5, 6], lisp '(1 2 3 4 5 6)
1:6 # Same as above, but in a compact form

seq(1, 6) # → python range(1, 6)
seq(1, 6, by=2) # → python range(1, 6, 2)

x <- 1:6; x[2] # → python range(1, 6)[2], lisp (second '(1 2 3 4 5 6))
x[c(1, 3, 4)] #
