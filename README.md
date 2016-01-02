# Motion Detection in RaspberryPi

The application, run in Raspberry Pi, detects motions, alert a user and record motion.

## Why did I create this app?
Well, I am living with my uni mates far away from university area. And we all are leaving our place for Christmas holiday. As you suppose, we need security :) 

## How it works?

When any motion is detected, the app sends an alert mail to the user and upload video frames to your sftp server (could be cloud server in future). As soon as the frames are uploaded, they will be deleted from a storage of Raspberry PI.   
I am using Mixtures of Gaussian model for detecting differences between video frames.

## How to install and use it?

- Prerequisites
  - OpenCV 3.0 (http://docs.opencv.org/2.4/doc/tutorials/introduction/linux_install/linux_install.html)
  - paramiko python package `apt-get install python-paramiko`
  - sendmail `apt-get install sendmail`
- Use the tool
  - Fill the config.txt file with requested credentials without leaving any symbol (no spaces, no quotes)
    - localpath in Raspberry Pi (motion frames will be uploaded)
    - your email address (emails are sent from localhost, different email services like gmail, yahoo will be provided in future)
    - sftp server address
    - sftp server username
    - sftp server password
    - sftp server directory path (motion frames will be uploaded from localpath)
  - run the python file `python run.py`
  - Yaay, you have security!


