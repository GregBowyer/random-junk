#include <stdio.h>
#include <pthread.h>
#include <assert.h>

#define NUM_RECTS 100000000
#define NUM_THREADS 8

double gArea = 0.0;
pthread_mutex_t gLock;

void *calcPI(void *arg) {
	int num = *((int *) arg);
	double partialHeight = 0.0;
	double lWidth = 1.0 / NUM_RECTS;
	double mid;

	// C99 bitches
	for (int i = num; i < NUM_RECTS; i += NUM_THREADS) {
		mid = (i + 0.5f) / NUM_RECTS;
		partialHeight += 4.0f / (1.0f + mid * mid);
	}

	pthread_mutex_lock(&gLock);
	gArea += partialHeight * lWidth;
	pthread_mutex_unlock(&gLock);
}

int main(int argc, char** argv) {
	pthread_t threads[NUM_THREADS];
	int tNum[NUM_THREADS];

	pthread_mutex_init(&gLock, NULL);

	for (int i=0; i<NUM_THREADS; i++) {
		tNum[i] = i;
		assert(0 == pthread_create(&threads[i], NULL, calcPI, (void *)&tNum[i]));
	}

	for (int tid=0; tid < NUM_THREADS; ++tid) {
		pthread_join(threads[tid], NULL);
	}

	pthread_mutex_destroy(&gLock);
	printf("Value of Π: %f\n", gArea);

	return 0;
}
