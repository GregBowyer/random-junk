# =============================================================================
#
#  File: pycublas.py v0.1
#  Copyright (c) 2009 by Derek Anderson <public@kered.org>
#  
#  Parts of this program were adopted from the BSD-licenced pystream project:
#  http://code.google.com/p/pystream/
#  which has been unfortunately abandoned by its creator, Tech-X.
#  
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
# 
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#  
#  A copy of the GNU Lesser General Public License is available at:
#  http://www.gnu.org/licenses/lgpl-3.0.txt
# 
# 
#  Description
#  -----------
#  This is designed to make using NVidia's CUBLAS API with Numpy's matrix
#  objects stupidly simple.
# 
#  For example:
#    import numpy
#    from pycublas import CUBLASMatrix
#    A = numpy.mat([[1,2,3],[4,5,6]],numpy.float32)
#    B = numpy.mat([[2,3],[4,5],[6,7]],numpy.float32)
#    C = (CUBLASMatrix(A)*CUBLASMatrix(B)).np_mat()
#    print C
# 
#  All CUBLAS alloc and free calls are mapped to the CUBLASMatrix object's life
#  in Python.
#
#  Performance numbers: (includes memory transfer times)
#    (4160x4160)*(4160x4160) = 43.0X faster than numpy
#    (4096x4096)*(4096x4096) = 34.0X
#    (3900x3900)*(3900x3900) = 47.3X
#    (2048x2048)*(2048x2048) = 28.2X 
#    (1024x1024)*(1024x1024) = 58.8X 
#    (512x512)*(512x512)     = 24.1X 
#    (256x256)*(256x256)     = 6.3X 
#    (128x128)*(128x128)     = 1.1X 
#  CPU: Intel(R) Core(TM)2 Duo CPU E8400 @ 3.00GHz stepping 06
#  GPU: nVidia Corporation GeForce 8800 GT (rev a2)
# 
#  Note: This version only supports float32.
#  Note: CUBLAS limits matrix dims to (65536x65536).
#
# =============================================================================

from __future__ import division, with_statement
import ctypes, math, numpy, platform, time


# arrived at via trial-and-error - might need tweaking for your GPU
MEM_ALIGN_SIZE = 32

class CUBLASMatrix(object):

  def __init__(self, X, dtype=numpy.float32, mem_align=True):

    if isinstance(X, numpy.matrix):
      assert len(X.shape)==2
      self.shape = X.shape
      self.dtype = X.dtype
    elif isinstance(X, tuple) and len(X)==2:
      self.shape = X
      self.dtype = dtype
    else:
      raise AttributeError('unsupported type: %s' % str(X))

    if self.dtype!=numpy.float32:
      raise Exception('only float32 supported (currently) - not '+ str(self.dtype))

    if self.dtype==numpy.float32: self.ctypes_dtype = ctypes.c_float

    # expanding the matrix to align with CUDA's memory banks can often double
    # performance at the cost of a few KB of memory.
    if mem_align:
      self._shape = ( int(math.ceil(self.shape[0]/MEM_ALIGN_SIZE))*MEM_ALIGN_SIZE,
                      int(math.ceil(self.shape[1]/MEM_ALIGN_SIZE))*MEM_ALIGN_SIZE )
      #print '[pycublas] memory alignment overhead: %.0fK' % ( ( (self._shape[0]-self.shape[0])*self._shape[1] + (self._shape[1]-self.shape[1])*self.shape[0] ) * ctypes.sizeof(self.ctypes_dtype)/1024 )
    else:
      self._shape = self.shape

    # it would seem CUBLAS uses 16 bit indices
    assert max(self._shape) <= 65536

    self.ld = self.shape[0]
    self._ld = self._shape[0]
    self.size = self.shape[0]*self.shape[1]
    self._size = self._shape[0]*self._shape[1]
    #print '[pycublas] reshaping:', self.shape, '->', self._shape, 'ld:', self.ld, '->', self._ld
    self._X = cublasAlloc(self._size, self.ctypes_dtype)
    self.zero()

    if isinstance(X, numpy.matrix):
      X = numpy.asfortranarray(X)
      cublasSetMatrix(self.shape[0], self.shape[1], self.ctypes_dtype, get_numpy_pointer(X,self.ctypes_dtype), self.ld, self._X, self._ld)

  
  def __del__(self):
    #print '[pycublas] freeing:', self
    cublasFree(self._X)
  
  def __mul__(self, other):
    assert isinstance(other, CUBLASMatrix)
    C = CUBLASMatrix((self.shape[0], other.shape[1]))
    cublasSgemm('N', 'N', self._shape[0], other._shape[1], self._shape[1], 1, self._X, self._ld, other._X, other._ld, 1, C._X, C._ld)
    return C
    
  def np_mat(self):
    X = numpy.zeros(self.shape, numpy.float32, order='F')
    cublasGetMatrix(self.shape[0], self.shape[1], self.ctypes_dtype, self._X, self._ld, get_numpy_pointer(X,self.ctypes_dtype), self.ld)
    return X
  def np_matrix(self):
    return self.np_mat()
    
  def scale(self, alpha):
    cublasSscal(self._size, alpha, self._X, 1)

  def zero(self):
    self.scale(0)


class CUBLASVector(object):

  def __init__(self, X, dtype=numpy.float32, mem_align=False):

    if isinstance(X, numpy.ndarray):
      assert len(X.shape)==1
      self.shape = X.shape
      self.dtype = X.dtype
    elif isinstance(X, tuple) and len(X)==1:
      self.shape = X
      self.dtype = dtype
    else:
      raise AttributeError('unsupported type: %s' % str(X))

    if self.dtype!=numpy.float32:
      raise Exception('only float32 supported (currently) - not '+ str(self.dtype))

    if self.dtype==numpy.float32: self.ctypes_dtype = ctypes.c_float

    if mem_align:
      self._shape = ( int(math.ceil(self.shape[0]/MEM_ALIGN_SIZE))*MEM_ALIGN_SIZE, )
    else:
      self._shape = self.shape

    self.size = self.shape[0]
    self._size = self._shape[0]
    self._X = cublasAlloc(self._size, self.ctypes_dtype)
    self.zero()

    if isinstance(X, numpy.ndarray):
      X = X.copy()
      cublasSetVector(self._size, self.ctypes_dtype, get_numpy_pointer(X,self.ctypes_dtype), 1, self._X, 1)

  
  def __del__(self):
    #print '[pycublas] freeing:', self
    cublasFree(self._X)
  
  def np_array(self):
    X = numpy.zeros(self.shape, numpy.float32, order='F')
    cublasGetVector(self.shape[0], self.ctypes_dtype, self._X, 1, get_numpy_pointer(X,self.ctypes_dtype), 1)
    return X
    
  def scale(self, alpha):
    cublasSscal(self._size, alpha, self._X, 1)

  def zero(self):
    self.scale(0)
  
  def dot(self, other):
    return cublasSdot(self._size, self._X, 1, other._X, 1)


# -----------------------------------------------------------------------------
#  CUBLAS 
# -----------------------------------------------------------------------------

if platform.system()=='Microsoft': libcublas = ctypes.windll.LoadLibrary('cublas.dll')
if platform.system()=='Darwin':    libcublas = ctypes.cdll.LoadLibrary('/usr/local/cuda/lib/libcublas.dylib')
if platform.system()=='Linux':     libcublas = ctypes.cdll.LoadLibrary('libcublas.so')
else:                              libcublas = ctypes.cdll.LoadLibrary('libcublas.so')

def get_numpy_pointer(x, ctypes_dtype):
  return x.ctypes.data_as(ctypes.POINTER(ctypes_dtype))

CUBLAS_STATUS_SUCCESS          = 0x00000000
CUBLAS_STATUS_NOT_INITIALIZED  = 0x00000001
CUBLAS_STATUS_ALLOC_FAILED     = 0x00000003
CUBLAS_STATUS_INVALID_VALUE    = 0x00000007
CUBLAS_STATUS_MAPPING_ERROR    = 0x0000000B
CUBLAS_STATUS_EXECUTION_FAILED = 0x0000000D
CUBLAS_STATUS_INTERNAL_ERROR   = 0x0000000E
CUBLAS_STATUS = {
  CUBLAS_STATUS_SUCCESS:          'CUBLAS_STATUS_SUCCESS',
  CUBLAS_STATUS_NOT_INITIALIZED:  'CUBLAS_STATUS_NOT_INITIALIZED',
  CUBLAS_STATUS_ALLOC_FAILED:     'CUBLAS_STATUS_ALLOC_FAILED',
  CUBLAS_STATUS_INVALID_VALUE:    'CUBLAS_STATUS_INVALID_VALUE', 
  CUBLAS_STATUS_MAPPING_ERROR:    'CUBLAS_STATUS_MAPPING_ERROR', 
  CUBLAS_STATUS_EXECUTION_FAILED: 'CUBLAS_STATUS_EXECUTION_FAILED', 
  CUBLAS_STATUS_INTERNAL_ERROR:   'CUBLAS_STATUS_INTERNAL_ERROR',
}
CUBLAS_STATUS_TYPE = ctypes.c_uint

def check_cublas_status(status):
  if status != CUBLAS_STATUS_SUCCESS:
    raise Exception(CUBLAS_STATUS[status])

# cublasInit
_cublasInit = libcublas.cublasInit
_cublasInit.restype = CUBLAS_STATUS_TYPE
_cublasInit.argtypes = []
def cublasInit():
  status = _cublasInit()
  check_cublas_status(status)

# cublasShutdown
_cublasShutdown = libcublas.cublasShutdown
_cublasShutdown.restype = CUBLAS_STATUS_TYPE
_cublasShutdown.argtypes = []
def cublasShutdown():
  status = _cublasShutdown()
  check_cublas_status(status)    

# -----------------------------------------------------------------------------
#  Memory Management 
# -----------------------------------------------------------------------------

# cublasAlloc
_cublasAlloc = libcublas.cublasAlloc
_cublasAlloc.restype = CUBLAS_STATUS_TYPE
_cublasAlloc.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_void_p)]
def cublasAlloc(n, ctype):
  #print '[pycublas] cublasAlloc %.1fM' % (n*ctypes.sizeof(ctype)/2**20)
  assert isinstance(n, int)
  devPtr = ctypes.pointer(ctype())
  castDevPtr = ctypes.cast(ctypes.pointer(devPtr), ctypes.POINTER(ctypes.c_void_p))
  status = _cublasAlloc(n, ctypes.sizeof(ctype), castDevPtr)
  check_cublas_status(status)
  return devPtr

# cublasFree
_cublasFree = libcublas.cublasFree
_cublasFree.restype = CUBLAS_STATUS_TYPE
_cublasFree.argtypes = [ctypes.c_void_p]
def cublasFree(devPtr):
  status = _cublasFree(devPtr)
  check_cublas_status(status)

# cublasSetVector
_cublasSetVector = libcublas.cublasSetVector
_cublasSetVector.restype = CUBLAS_STATUS_TYPE
_cublasSetVector.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p, ctypes.c_int]
def cublasSetVector(n, ctype, hostVector, incx, deviceVector, incy):
    assert isinstance(n, int)
    assert isinstance(incx, int)
    assert isinstance(incy, int)
    elemSize = ctypes.sizeof(ctype)
    status = _cublasSetVector(n, elemSize, hostVector, incx, deviceVector, incy)
    check_cublas_status(status)    

# cublasGetVector
_cublasGetVector = libcublas.cublasGetVector
_cublasGetVector.restype = CUBLAS_STATUS_TYPE
_cublasGetVector.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p, ctypes.c_int]
def cublasGetVector(n, ctype, deviceVector, incx, hostVector, incy):
    assert isinstance(n, int)
    assert isinstance(incx, int)
    assert isinstance(incy, int)
    elemSize = ctypes.sizeof(ctype)
    status = _cublasGetVector(n, elemSize, deviceVector, incx, hostVector, incy)
    check_cublas_status(status)   

# cublasSetMatrix
_cublasSetMatrix = libcublas.cublasSetMatrix
_cublasSetMatrix.restype = CUBLAS_STATUS_TYPE
_cublasSetMatrix.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p, ctypes.c_int]
def cublasSetMatrix(rows, cols, ctype, hostMatrixA, lda, deviceMatrixB, ldb):
  assert isinstance(rows, int)
  assert isinstance(cols, int)
  assert isinstance(lda, int)
  assert isinstance(ldb, int)
  elemSize = ctypes.sizeof(ctype)
  status = _cublasSetMatrix(rows, cols, elemSize, hostMatrixA, lda, deviceMatrixB, ldb)
  check_cublas_status(status) 

# cublasGetMatrix
_cublasGetMatrix = libcublas.cublasGetMatrix
_cublasGetMatrix.restype = CUBLAS_STATUS_TYPE
_cublasGetMatrix.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p, ctypes.c_int]
def cublasGetMatrix(rows, cols, ctype, deviceMatrixA, lda, hostMatrixB, ldb):
  assert isinstance(rows, int)
  assert isinstance(cols, int)
  assert isinstance(lda, int)
  assert isinstance(ldb, int)
  elemSize = ctypes.sizeof(ctype)
  status = _cublasGetMatrix(rows, cols, elemSize, deviceMatrixA, lda, hostMatrixB, ldb)
  check_cublas_status(status)

# cublasGetError
_cublasGetError = libcublas.cublasGetError
_cublasGetError.restype = CUBLAS_STATUS_TYPE
_cublasGetError.argtypes = []
def cublasGetError():
  status = _cublasGetError()
  check_cublas_status(status)

# -----------------------------------------------------------------------------
#  BLAS1 
# -----------------------------------------------------------------------------

_cublasSdot = libcublas.cublasSdot
_cublasSdot.restype = ctypes.c_float
_cublasSdot.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_float), ctypes.c_int, ctypes.POINTER(ctypes.c_float), ctypes.c_int]
def cublasSdot(n, x, incx, y, incy):
  r = _cublasSdot(n, x, incx, y, incy)
  cublasGetError()
  return float(r)

_cublasSscal = libcublas.cublasSscal
_cublasSscal.restype = CUBLAS_STATUS_TYPE
_cublasSscal.argtypes = [ctypes.c_int, ctypes.c_float, ctypes.POINTER(ctypes.c_float), ctypes.c_int]
def cublasSscal(n, alpha, x, incx):
  _cublasSscal(n, alpha, x, incx)
  cublasGetError()

# -----------------------------------------------------------------------------
#  BLAS2 
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
#  BLAS3 
# -----------------------------------------------------------------------------

# cublasSgemm
_cublasSgemm = libcublas.cublasSgemm
_cublasSgemm.restype = None
_cublasSgemm.argtypes = [ctypes.c_char, ctypes.c_char, ctypes.c_int, ctypes.c_int, ctypes.c_int,
                         ctypes.c_float, ctypes.POINTER(ctypes.c_float), ctypes.c_int,
                         ctypes.POINTER(ctypes.c_float), ctypes.c_int, ctypes.c_float, 
                         ctypes.POINTER(ctypes.c_float), ctypes.c_int]
def cublasSgemm(transa, transb, m, n, k, alpha, A, lda, B, ldb, beta, C, ldc):
  _cublasSgemm(transa, transb, m, n, k, alpha, A, lda, B, ldb, beta, C, ldc)
  cublasGetError()

# -----------------------------------------------------------------------------
#  Init
# -----------------------------------------------------------------------------

cublasInit()

# -----------------------------------------------------------------------------
#  Test
# -----------------------------------------------------------------------------

def _test_matrix():
#  A = numpy.mat([[1,2,3],[4,5,6]],numpy.float32)
#  B = numpy.mat([[2,3],[4,5],[6,7]],numpy.float32)
#  A = numpy.mat( numpy.array( numpy.random.random_sample((256,8192)), numpy.float32) )
#  B = numpy.mat( numpy.array( numpy.random.random_sample((8192,256)), numpy.float32) )
#  A = numpy.mat( numpy.array( numpy.random.random_sample((257,8191)), numpy.float32) )
#  B = numpy.mat( numpy.array( numpy.random.random_sample((8191,257)), numpy.float32) )
  A = numpy.mat( numpy.array( numpy.random.random_sample((256,65536)), numpy.float32) )
  B = numpy.mat( numpy.array( numpy.random.random_sample((65536,256)), numpy.float32) )
#  A = numpy.mat( numpy.array( numpy.random.random_sample((200,3000)), numpy.float32) )
#  B = numpy.mat( numpy.array( numpy.random.random_sample((3000,3000,)), numpy.float32) )
#  A = numpy.mat( numpy.array( numpy.random.random_sample((2048,2048)), numpy.float32) )
#  B = numpy.mat( numpy.array( numpy.random.random_sample((2048,2048)), numpy.float32) )
#  i = 3000
#  A = numpy.mat( numpy.array( numpy.random.random_sample((i,i)), numpy.float32) )
#  B = numpy.mat( numpy.array( numpy.random.random_sample((i,i)), numpy.float32) )
#  A = numpy.mat([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]],numpy.float32)
#  B = numpy.mat([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]],numpy.float32)
#  print A
#  print A*B
  print '[pycublas] shapes: ', A.shape, '*', B.shape, '=', (A.shape[0],B.shape[1])
  start = time.time()
  C1 = (CUBLASMatrix(A)*CUBLASMatrix(B)).np_matrix()
  t1 = time.time()-start
  print '[pycublas] time (CUBLAS): %fs' % t1
  start = time.time()
  C2 = A*B
  t2 = time.time()-start
  print '[pycublas] time (numpy): %fs' % t2
  print '[pycublas] speedup: %.1fX' % (t2/t1)
  print '[pycublas] error (average per cell):', numpy.abs(C1-C2).sum()/C2.size

def _test_array():
#  A = numpy.array( [1,2,3], numpy.float32)
  A = numpy.array( numpy.random.random_sample((5000000,)), numpy.float32)
  print 'A.shape', A.shape
#  print _A.np_array()
  start = time.time()
  _A = CUBLASVector(A)
  for i in range(200):
    r1 = _A.dot(_A)
  t1 = time.time()-start
  print '[pycublas] time (CUBLAS): %fs' % t1
  start = time.time()
  for i in range(200):
    r2 = numpy.dot(A,A)
  t2 = time.time()-start
  print '[pycublas] time (numpy): %fs' % t2

  print 'numpy.dot(A,A)', 
  print '[pycublas] speedup: %.1fX' % (t2/t1)
  print r1
  print r2
  print '[pycublas] error (average per cell):', abs(r1-r2)/A.size

if __name__=='__main__':
  _test_matrix()
#  _test_array()

