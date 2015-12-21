# Motion Detection in RaspberryPi

The application detects motion from Webcam, runs in Raspberry PI.

## Why did I created this app?
Well, I and all my housemates are leaving our place for Christmas holiday, but we don't have security cameras.

## How it works?

 When any motion is detected, app sends alert mail to user and start to save video frames to your cloud server.
 I am using Mixture of Gaussian algorithm for detecting differences between video frames.

## How to configure the app to your Raspberry Pi ?

- Install OpenCV to Raspberry Pi
- Enter the directory name in commad line argument and run application ( temporarily save video frames when motion is detected)
- Run Php file, enter email address and your cloud server credentials (saving frames to your cloud)
- Done



