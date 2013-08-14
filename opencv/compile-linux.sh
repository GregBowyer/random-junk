g++ -I/opt/sun-jdk-1.6.0.33/include -I/opt/sun-jdk-1.6.0.33/include/linux -shared -fPIC -DMAX_THREADS=1000 -DJVMTI_TYPE=1 -o libcalltracer.so -Wl,-soname,calltracer.so -lc -Wall ../src/ctrace.c
g++ -I/opt/sun-jdk-1.6.0.33/include -I/opt/sun-jdk-1.6.0.33/include/linux -shared -fPIC -DMAX_THREADS=1000 -DJVMTI_TYPE=1 -o libcalltracer.so -Wl,-soname,calltracer.so -lc -Wall ../src/ctrace.c
