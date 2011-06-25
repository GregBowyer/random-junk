#include <stdio.h>

static long num_rects = 100000;

int main(int argc, char** argv) {
	double mid, height, width, sum = 0.0;
	double area;

	width = 1.0 / (double) num_rects;
	// C99 bitches
	for (int i =0; i < num_rects; i++) {
		mid = (i + 0.5) * width;
		height = 4.0 / (1.0 + mid * mid);
		sum += height;
	}

	area = width * sum;
	printf("Computed approx Π = %f\n", area);

	return 0;
}
