#include <stdio.h>
#include <pthread.h>
#include <assert.h>

#define TRUE 1

/**
 * Implementation of dekkers algorithm for multual exclusion
 */

volatile int favoured = 0;
volatile int thread0Intent, thread1Intent;

int protectMe = 0;

int criticalRegion() {
	return protectMe++;
}

void *thread0(void *arg) {

	int tid = *((int *) arg);

	while (TRUE) {
		thread0Intent = 1;
		while (thread1Intent) {
			if (favoured == 1) {
				thread0Intent = 0;
				while (favoured == 1) { }
				thread0Intent = 1;
			}
		}
		int counter = criticalRegion();
		printf("Thread %d Counter is %d\n", tid, counter);
		favoured = 1;
		thread0Intent = 0;
	}

	return NULL;
}

void *thread1(void *arg) {

	int tid = *((int *) arg);

	while (TRUE) {
		thread1Intent = 1;
		while (thread0Intent) {
			if (favoured == 0) {
				thread1Intent = 0;
				while (favoured == 0) { } 
				thread1Intent = 1;
			}
		}
		int counter = criticalRegion();
		printf("Thread %d Counter is %d\n", tid, counter);
		favoured = 0;
		thread1Intent = 0;
	}

	return NULL;
}

int main(int argc, char **argv) {
	pthread_t fred0;
	pthread_t fred1;
	int tid0 = 0;
	int tid1 = 1;
	assert(0 == pthread_create(&fred0, NULL, &thread0, &tid0));
	assert(0 == pthread_create(&fred1, NULL, &thread1, &tid1));

	// This will never complete, but we do this to stop main() running off
	// in our contrieved example
	assert(0 == pthread_join(fred0, NULL));
	assert(0 == pthread_join(fred1, NULL));
	return 0;
}

