#include <stdio.h>

static long num_rects = 100000000;

/**
 * OpenMP version of computing approx Π
 * comple with:
 * 		gcc -std=c99 -fopenmp
 * run with:
 * 		OMP_NUM_THREADS=4 ./a.out
 */
int main(int argc, char** argv) {
	double mid, height, width, sum = 0.0;
	double area;

	width = 1.0 / (double) num_rects;
	// C99 bitches
#pragma omp parallel for private(mid, height) reduction(+:sum)
	for (int i =0; i < num_rects; i++) {
		mid = (i + 0.5) * width;
		height = 4.0 / (1.0 + mid * mid);
		sum += height;
	}

	area = width * sum;
	printf("Computed approx Π = %f\n", area);

	return 0;
}
