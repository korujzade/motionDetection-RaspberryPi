#include "opencv2/imgcodecs.hpp"
#include "opencv2/imgproc.hpp"
#include "opencv2/videoio.hpp"
#include <opencv2/highgui.hpp>
#include <opencv2/video.hpp>
#include <stdio.h>
#include <iostream>
#include <sstream>
#include <ctime>
using namespace cv;
using namespace std;

// Struct keeps boundary pixel values of motion area and the number of pixels
// changed
struct Pixel_Values {
	int minX;
	int maxX;
	int minY;
	int maxY;
	int changes;
};

time_t rawtime;
struct tm * timeinfo;
char buffer[80];

Mat frame, gray, fgMaskMOG2;
string message = "No motion is in the room!";
Ptr<BackgroundSubtractor> pMOG2;
int keyboard;
int c=0;
string path = string("/home/korujzade/Desktop/motionDetection-RaspberryPi/frames/");

void processVideo();
Pixel_Values motion_values(Mat fgMaskMOG2);

int main(int argc, char* argv[]) {

	//create GUI windows
	namedWindow("Raw Frame");
	namedWindow("Gray Frame");
	namedWindow("FG Mask MOG 2");

	//create Background Subtractor objects with MOG2 approach
	pMOG2 = createBackgroundSubtractorMOG2();

	// imput data coming from web camera
	if (strcmp(argv[1], "-vid") == 0) {
		processVideo();
	} else {
		//error in reading input parameters
		cerr << "Please, check the input parameters." << endl;
		cerr << "Exiting..." << endl;
		return EXIT_FAILURE;
	}
	//destroy GUI windows
	destroyAllWindows();
	return EXIT_SUCCESS;
}

// function analyse each frame and finds differences between them
void processVideo() {
	//create the capture object
	VideoCapture capture(0);
	if (!capture.isOpened()) {
		exit(EXIT_FAILURE);
	}
	//read input data. ESC or 'q' for quitting
	while ((char) keyboard != 'q' && (char) keyboard != 27) {
		//read the current frame
		if (!capture.read(frame)) {
			cerr << "Unable to read next frame." << endl;
			cerr << "Exiting..." << endl;

			exit(EXIT_FAILURE);
		}

		resize(frame, frame, Size(500, 500));
		cvtColor(frame, gray, CV_RGB2GRAY);
		GaussianBlur(gray, gray, Size(21, 21), 0);

		//update the background model
		pMOG2->apply(gray, fgMaskMOG2);

		// notification on right up corner of the frame
		rectangle(frame, cv::Point(10, 2), cv::Point(300, 20),
				cv::Scalar(255, 255, 255), -1);

		// border values of motion area
		Pixel_Values values = motion_values(fgMaskMOG2);

		// if the number of pixels changed is more than 5, alert
		// and show boundary of motion
		if (values.changes >= 5) {

			time(&rawtime);
			timeinfo = localtime(&rawtime);
			strftime(buffer, 80, "%d-%m-%Y %I:%M:%S", timeinfo);
			string str(buffer);

			stringstream sstm;
			sstm << path << str << string("-") << c << string(".jpg");
			str = sstm.str();

			message = "Alert Alert Alert!!!";
			rectangle(frame, cv::Point(values.minX, values.minY),
					cv::Point(values.maxX - values.minX,
							values.maxY - values.minY), cv::Scalar(32, 32, 212),
					1);

			imwrite(str, frame);

		}
		putText(frame, message.c_str(), cv::Point(15, 15), FONT_HERSHEY_SIMPLEX,
				0.5, cv::Scalar(0, 0, 0));
		message = "No motion in the room!";

		//show the current frame and the fg masks
		imshow("Raw Frame", frame);
		imshow("Gray Frame", gray);
		imshow("FG Mask MOG 2", fgMaskMOG2);

		c++;
		//get the input from the keyboard
		keyboard = waitKey(30);
	}
	//delete capture object
	capture.release();
}

Pixel_Values motion_values(Mat fgMaskMOG2) {

	Pixel_Values newValues;
	newValues.minX = fgMaskMOG2.cols;
	newValues.minY = fgMaskMOG2.rows;
	newValues.maxX = 0;
	newValues.maxY = 0;
	newValues.changes = 0;

	for (int i = 0; i < fgMaskMOG2.cols; i++) {
		for (int j = 0; j < fgMaskMOG2.rows; j++) {
			if (fgMaskMOG2.at<uchar>(Point(i, j)) == 255) {
				newValues.changes++;
				if (newValues.maxX < i)
					newValues.maxX = i;
				if (newValues.maxY < j)
					newValues.maxY = j;
				if (newValues.minX > i)
					newValues.minX = i;
				if (newValues.minY > j)
					newValues.minY = j;
			}
		}
	}

	return newValues;
}

