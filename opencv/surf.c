#include <stdio.h>
#include <opencv2/features2d/features2d.hpp>
#include <opencv2/nonfree/features2d.hpp>
#include <opencv2/nonfree/nonfree.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc_c.h>
#include <opencv2/legacy/compat.hpp>

int main(int argc, char** argv) {

    CvMemStorage* storage = cvCreateMemStorage(0);
    cvNamedWindow("Image", 1);

    int key = 0;

    static CvScalar blue_color[] = { 0, 255, 0 };

    //CvCapture* capture = cvCreateCameraCapture(0);
    CvCapture* capture = cvCaptureFromCAM(CV_CAP_ANY);
    CvMat* prevgray = 0, *image = 0, *gray = 0;

    while(key != 'q') {
        int firstFrame = gray == 0;
        IplImage* frame = cvQueryFrame(capture);
        if (!frame) {
            break;
        }

        if (!gray) {
            image = cvCreateMat(frame->height, frame->width, CV_8UC1);
        }

        cvCvtColor(frame, image, CV_BGR2GRAY);
        CvSeq *imageKeyPoints = 0, *imageDescriptors = 0;

        //CvSURFParams params = cvSURFParams(400, 1);
        CvSURFParams params = {
           .extended = 1,
           .hessianThreshold = 500,
           .nOctaves = 2,
           .nOctaveLayers = 8
        };

        cvExtractSURF(image, 0, &imageKeyPoints, &imageDescriptors, storage, params);

        printf("Image descriptors: %d\n", imageDescriptors->total);

        for (int i=0; i < imageKeyPoints->total; i++) {
            CvSURFPoint* r = (CvSURFPoint*) cvGetSeqElem(imageKeyPoints, i);
            CvPoint center;
            int radius;
            center.x = cvRound(r->pt.x);
            center.y = cvRound(r->pt.y);
            radius = cvRound(r->size * 1.2 / 20.0 * 2);
            cvCircle(frame, center, radius, blue_color[0], 1, 8, 0);
        }

        cvShowImage("Image", frame);
        cvWaitKey(10);
    }

    cvDestroyWindow("Image");
    return 0;
}
