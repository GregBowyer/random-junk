from theano import function, shared, sandbox, config
from theano import tensor as T
import numpy
x = T.fmatrix('x')
y = T.fmatrix('y')
arry1 = shared(numpy.random.rand(5000, 5000), config.floatX)
arry2 = shared(numpy.random.rand(5000, 5000), config.floatX)
f = function([x, y], [x * y])
r = f(arry1, arry2)
print r
