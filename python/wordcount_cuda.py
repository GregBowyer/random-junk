#!/usr/bin/python
import pycuda.autoinit
import numpy
from pycuda import gpuarray, reduction
import time
import sys
 
def createCudaWordCountKernel():
    initvalue = "0"
    mapper = "(a[i] == 32)*(b[i] != 32)" # 32 is ascii code for whitespace
    reducer = "a+b"
    cudafunctionarguments = "char* a, char* b"
    wordcountkernel = reduction.ReductionKernel(numpy.float32, neutral = initvalue,
                                            reduce_expr=reducer, map_expr = mapper,
                                            arguments = cudafunctionarguments)
    return wordcountkernel
 
def createBigDataset(filename):
    print "reading data"
    dataset = file(filename).read()
    print "creating a big dataset"
    words = " ".join(dataset.split()) # in order to get rid of \t and \n
    chars = [ord(x) for x in words]
    bigdataset = []
    for k in range(100):
        bigdataset += chars
    print "dataset size = ", len(bigdataset)
    print "creating numpy array of dataset"
    bignumpyarray = numpy.array( bigdataset, dtype=numpy.uint8)
    return bignumpyarray
 
def wordCount(wordcountkernel, bignumpyarray):
    print "uploading array to gpu"
    gpudataset = gpuarray.to_gpu(bignumpyarray)
    datasetsize = len(bignumpyarray)
    start = time.time()
    wordcount = wordcountkernel(gpudataset[:-1],gpudataset[1:]).get()
    stop = time.time()
    seconds = (stop-start)
    estimatepersecond = (datasetsize/seconds)/(1024*1024*1024)
    print "word count took ", seconds*1000, " milliseconds"
    print "estimated throughput ", estimatepersecond, " Gigabytes/s"
    return wordcount
 
if __name__ == "__main__":
    bignumpyarray = createBigDataset(sys.argv[1])
    wordcountkernel = createCudaWordCountKernel()
    wordcount = wordCount(wordcountkernel, bignumpyarray)
