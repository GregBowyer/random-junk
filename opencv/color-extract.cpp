#include <opencv2/opencv.hpp>
#include <opencv2/ml/ml.hpp>
#include <opencv2/legacy/legacy.hpp>

#include <cstdio>

int main(int argc, char** argv) {

    cv::Mat source = cv::imread(argv[1]);

    //ouput images
    cv::Mat meanImg(source.rows, source.cols, CV_32FC3);
    cv::Mat fgImg(source.rows, source.cols, CV_8UC3);
    cv::Mat bgImg(source.rows, source.cols, CV_8UC3);

    //convert the input image to float
    cv::Mat floatSource;
    source.convertTo(floatSource, CV_32F);

    //now convert the float image to column vector
    cv::Mat samples(source.rows * source.cols, 3, CV_32FC1);
    int idx = 0;
    for (int y = 0; y < source.rows; y++) {
        cv::Vec3f* row = floatSource.ptr<cv::Vec3f > (y);
        for (int x = 0; x < source.cols; x++) {
            samples.at<cv::Vec3f > (idx++, 0) = row[x];
        }
    }

    //we need just 2 clusters
    cv::EMParams params(2);
    cv::ExpectationMaximization em(samples, cv::Mat(), params);

    //the two dominating colors
    cv::Mat means = em.getMeans();
    //the weights of the two dominant colors
    cv::Mat weights = em.getWeights();

    //we define the foreground as the dominant color with the largest weight
    const int fgId = weights.at<float>(0) > weights.at<float>(1) ? 0 : 1;

    //now classify each of the source pixels
    idx = 0;
    double* ps;
    for (int y = 0; y < source.rows; y++) {
        for (int x = 0; x < source.cols; x++) {

            //classify
            const int result = cvRound(em.predict(samples.row(idx++), NULL));
            //get the according mean (dominant color)
            ps = means.ptr<double>(result, 0);

            //set the according mean value to the mean image
            float* pd = meanImg.ptr<float>(y, x);
            //float images need to be in [0..1] range
            pd[0] = ps[0] / 255.0;
            pd[1] = ps[1] / 255.0;
            pd[2] = ps[2] / 255.0;

            //set either foreground or background
            if (result == fgId) {
                fgImg.at<cv::Point3_<uchar> >(y, x, 0) = source.at<cv::Point3_<uchar> >(y, x, 0);
            } else {
                bgImg.at<cv::Point3_<uchar> >(y, x, 0) = source.at<cv::Point3_<uchar> >(y, x, 0);
            }
        }
    }

    printf("%f %f %f\n", ps[0] / 255.0, ps[1] / 255.0, ps[2] / 255.0);

    cv::imshow("Means", meanImg);
    cv::imshow("Foreground", fgImg);
    cv::imshow("Background", bgImg);
    cv::waitKey(0);

    return 0;
}
