#include <stdio.h>

#include "tbb/parallel_reduce.h"
#include "tbb/task_scheduler_init.h"
#include "tbb/blocked_range.h"
#include "tbb/partitioner.h"

using namespace std;
using namespace tbb;

static long num_rects = 100000000;

/**
 * ThreadBuildingBlocks (TBB) version of calculating Π
 * complete with icky C++
 * comple with:
 * 		g++ -ltbb
 */
class Pi {
	double *const my_rects;

  public:
	double partialHeight;
	Pi(double *const width) : my_rects(width), partialHeight(0) { }
	// Copy Ctor
	Pi(Pi& pi, split): my_rects(pi.my_rects), partialHeight(0) { }

  	void operator()(const blocked_range<size_t>& r) {
		double rectangleWidth = *my_rects;
		double x;
		for (size_t i = r.begin(); i != r.end(); ++i) {
			x = (i + 0.5) * rectangleWidth;
			partialHeight += 4.0 / (1.0 + (x*x));
		}
	}

	void join(const Pi& y) {
		partialHeight += y.partialHeight; 
	}
};

int main(int argc, char** argv) {
	double area;
	double width = 1.0 / (double) num_rects;
	Pi my_block((double *const) &width);
	task_scheduler_init init;

	parallel_reduce(blocked_range<size_t>(0, num_rects), my_block, auto_partitioner());
	area = my_block.partialHeight * width;

	printf("The value of Π is %f\n", area);
	return 0;
}
