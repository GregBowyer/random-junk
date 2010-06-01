import numpy
from theano import tensor as T
from theano import sandbox, shared, Out, config, function
import time

print 'CPU version: '

t0 = time.time()
arry1 = numpy.random.randn(7000, 7000).astype(numpy.float32)
arry2 = numpy.random.randn(7000, 7000).astype(numpy.float32)

arry1 * arry2
print 'time was ', time.time() - t0
del arry1
del arry2

#------------------------------------------------------------------------------------------ 
print 'GPU version: '
t0 = time.time()
x = T.fmatrix('x')
y = T.fmatrix('y')
z = x * y
arry1 = numpy.random.randn(7000, 7000).astype(numpy.float32)
arry2 = numpy.random.randn(7000, 7000).astype(numpy.float32)
#z = arry1 * arry2
f = function([x, y], Out(z, borrow=True))
f(arry1, arry2)
print 'time was ', time.time() - t0
