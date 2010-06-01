from theano import function, config, shared, sandbox, Out, dot
import theano.tensor as T
import numpy
import time

vlen = 10 * 32 * 512  # 10 x #cores x # threads per core
iters = 1

rng = numpy.random.RandomState(22)
x = T.fmatrix('x')
y = T.fmatrix('y')
a1 = shared(numpy.array(rng.rand(12000, 12000), numpy.float32))
a2 = shared(numpy.array(rng.rand(12000, 12000), numpy.float32))
#z = y * x
z = dot(a1, a2)

f = function([], sandbox.cuda.basic_ops.gpu_from_host(z))

t0 = time.time()
for i in xrange(iters):
    r = f()
    #r = a1 * a2
print 'Looping ', iters, 'times took', time.time() - t0, 'seconds'
print 'Result is', numpy.asarray(r)
print 'Shape is', r.shape
