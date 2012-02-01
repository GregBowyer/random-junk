#include <stdio.h>
#include <pthread.h>
#include <assert.h>
#include <unistd.h>
#include <stdlib.h>
#include <time.h>
#include <sys/time.h>

void *wasteTime(void *arg) {
    sleep(0.100);
}

void print_timer(char *operation, struct timeval timer[]) {
    int secs = (timer[1].tv_sec - timer[0].tv_sec);
    int usecs = (timer[1].tv_usec - timer[0].tv_usec);
    if (secs > 0 || usecs > 0) {
        printf("Time taken to %s - secs %d, msecs %d\n", operation, secs, usecs);
    }
}

int main(int argc, char** argv) {

    int num_threads = atoi(argv[1]);
    int wait_secs = atoi(argv[2]);

    // Avoid parsing the threads something that might be stack allocated
    printf("Num threads %d emulated wait secs %d\n", num_threads, wait_secs);

    pthread_t threads[num_threads];

    struct timeval create_timer[2];
    struct timeval join_timer[2];

    int num_active = 0;

    while(1) {

        gettimeofday(&create_timer[0], NULL);
        if (num_active == 0) {
            for (; num_active < num_threads; ) {
                assert (0 == pthread_create(&threads[num_active], NULL, wasteTime, NULL));
	    	num_active++;
            }
        }
        gettimeofday(&create_timer[1], NULL);
        print_timer("create threads", create_timer);

        // Crappy sleep to avoid spinning the main loop like a mentalist
	//sleep(0.050);

        // Drain ...
        gettimeofday(&join_timer[0], NULL);
	for (int i=0; i<num_active; ++i) {
            // We ignore the error, its EBUSY which should be a common case
            assert(0 == pthread_join(threads[i], NULL));
        }
	num_active = 0;

        gettimeofday(&join_timer[1], NULL);
        print_timer("join threads", join_timer);

	// The apach thread pool deallocates after 15 seconds
	printf("Sleeping for %d secs\n", wait_secs);
        sleep(wait_secs);
    }

    // We can never reach here ..... :S
    return 0;
}
