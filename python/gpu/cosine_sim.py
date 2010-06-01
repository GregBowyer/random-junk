#!env python

# Attempt to use and abuse cuda to do cosine sim on a GPU

import numpy as np
import time

import pycuda.autoinit
import pycuda.driver as drv
import pycuda.gpuarray as gpuarr
import pycuda.cumath as cumath
from pycuda.compiler import SourceModule

import math

VEC_SIZE = 10000000

vec1 = np.asarray(np.random.randn(VEC_SIZE), np.float32)
vec2 = np.asarray(np.random.randn(VEC_SIZE), np.float32)

t0 = time.time()
sqr1 = np.sqrt(np.dot(vec1, vec1))
sqr2 = np.sqrt(np.dot(vec2, vec2))
print np.dot(vec1, vec2) / sqr1 + sqr2
print 'CPU time: ', time.time() - t0

mod = SourceModule('''
__global__ void magnitude(float *vec) {

    //__shared__ float reduction[];

    unsigned int t = threadIdx.x;

    vec[t] *= vec[t];

    __syncthreads();

    for(unsigned int stride = blockDim.x >> 1; stride > 0; stride >>= 1) {
        __syncthreads();
        if(t < stride) {
            vec[t] += vec[t+stride];
        }
    }
}
''')

def magnitude(vec, vec2):
    #, fn = mod.get_function('magnitude')):
    #gpu_vec = drv.mem_alloc(vec.nbytes)
    #drv.memcpy_htod(gpu_vec, vec)

    #fn(gpu_vec, block=(512, 1, 1))

    #dest = drv.from_device_like(gpu_vec, vec)

    #print 'Dot product: ', dest[0]
    
    gpu_arry = gpuarr.to_gpu_async(vec)
    gpu_arry2 = gpuarr.to_gpu_async(vec2)
    mag = cumath.sqrt(gpuarr.dot(gpu_arry, gpu_arry, dtype=np.float32))
    mag2 = cumath.sqrt(gpuarr.dot(gpu_arry2, gpu_arry2, dtype=np.float32))

    product = gpuarr.dot(gpu_arry, gpu_arry2, dtype=np.float32) / mag + mag2
    print product
    return product.get()

# GPU version
t0 = time.time()
print magnitude(vec1, vec2)
print "GPU TIME: ", time.time() - t0
