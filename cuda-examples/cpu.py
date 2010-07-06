import numpy
import time

vlen = 1000 * 32 * 512  # 10 x #cores x # threads per core
iters = 1

rng = numpy.random.RandomState(22)
array = numpy.asarray(rng.rand(vlen), numpy.float32)
t0 = time.time()
for i in xrange(iters):
    r = numpy.exp(array)
print 'Looping ', iters, 'times took', time.time() - t0, 'seconds'
print 'Result is', r
print 'Shape is', r.shape
