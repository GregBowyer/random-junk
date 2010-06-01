from theano import function, config, shared, sandbox, Out
import theano.tensor as T
import numpy
import time

vlen = 1000 * 32 * 512  # 10 x #cores x # threads per core
iters = 1

rng = numpy.random.RandomState(22)
x = shared(numpy.asarray(rng.rand(vlen), numpy.float32)) #config.floatX))
#f = function([], T.exp(x))
#f = function([], sandbox.cuda.basic_ops.gpu_from_host(T.exp(x)))
f = function([], 
        Out(sandbox.cuda.basic_ops.gpu_from_host(T.exp(x)), borrow=True))
t0 = time.time()
for i in xrange(iters):
    r = f()
print 'Looping ', iters, 'times took', time.time() - t0, 'seconds'
print 'Result is', numpy.asarray(r)
print 'Shape is', r.shape
