g++ -DAZNIX_API_VERSION=200 \
    -DAZUL \
    -DAZ_X86 \
    -m64 \
    -D_REENTRANT \
    -D_XOPEN_SOURCE=600 \
    -D_GNU_SOURCE \
    -D_FILE_OFFSET_BITS=64 \
    -D_LARGEFILE_SOURCE \
    -fno-strict-aliasing \
    -fPIC \
    -I/usr/local/include \
    -laznix \
    -lpthread \
    -o azp_test \
    ./test.c

./azp_test
