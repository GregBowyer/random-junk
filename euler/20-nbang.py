# project euler, solve the sum of the digits of 100!
# (that is 100 * 99 * 98 * 97 .... * 1)

from operator import mul

sum((int(c) for c in str(reduce(mul, range(1,100)))))
