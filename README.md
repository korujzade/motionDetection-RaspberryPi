# Motion Detection in RaspberryPi

The application, run in Raspberry Pi, detects motions and record them.

## Why did I create this app?
Well, I am living with my uni mates far way from university area. And we all are leaving our place for Christmas holiday. As you suppose, we need security :) 

## How it works?

When any motion is detected, the app sends an alert mail to the user and upload video frames to your server/cloud server. As soon as the frames are uploaded, they will be deleted from a storage of Raspberry PI.   
I am using Mixture of Gaussian algorithm for detecting differences between video frames.

## How to install and use it?

- Pre-requests
  - OpenCV (http://docs.opencv.org/2.4/doc/tutorials/introduction/linux_install/linux_install.html)
  - paramiko python package (apt-get install python-paramiko)



