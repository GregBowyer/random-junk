#include <opencv2/opencv.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/gpu/gpu.hpp>
#include <string>
#include <iostream>
#include <cstdio>

using namespace cv;

int main(int argc, char** argv) {
    int spatialRad = 4;
    int colorRad = 4;
    int min = 25;

    int i = 1;
    Mat img = imread(argv[i]);
    Mat rgba;
    cvtColor(img, rgba, CV_BGRA2RGBA, 4);

    // Host array and cudaMemCpyToDevice in CUDA speak
    gpu::GpuMat srcImage = gpu::GpuMat(rgba); 
    // Device array and cudaMemcpyToHost in CUDA speak
    Mat deviceRes;
    gpu::meanShiftSegmentation(srcImage, deviceRes, spatialRad, colorRad, min);

    Mat dst;
    cvtColor(deviceRes, dst, CV_RGBA2BGRA, 4);

    namedWindow("test", CV_WINDOW_AUTOSIZE);
    imshow("test", dst);

    waitKey(0);
    //imwrite(argv[2], dst);

    return 0;
} 
