import sys
import paramiko
import glob
from os import path
import sftp
import os
import signal
import atexit
import subprocess
import thread
from datetime import datetime, date, timedelta
# Import smtplib for the actual sending function
import smtplib
# Import the email modules we'll need
from email.mime.text import MIMEText

localpath = sys.argv[1]
imagespath = "*.jpg"
imagespath = localpath + imagespath

def uploadFrames():
	remote_dir = sys.argv[6]
	with sftp.Server(sys.argv[4], sys.argv[5], sys.argv[3]) as server:
	    while True:	
		    for image in glob.glob(imagespath):
		        base = path.basename(image)
		        server.upload(image, path.join(remote_dir, base))
		        os.remove(image)

thread.start_new_thread(uploadFrames, ());

class MotionDetection:
  process = None
  command = ["./Main", "-vid", localpath]
  output  = []
  detectTime = None
  timeNow = None
  diff = 0
  FMT = '%H:%M:%S'
  email = sys.argv[2] 

  # initialize stuff
  def __init__(self):
    atexit.register(self.kill_child)
    self.output = self.run()

  # stuff that cleans up (kills remained processes on exit)
  def kill_child(self):
    if self.process.pid is None:
      pass
    else:
      os.kill(self.process.pid, signal.SIGTERM)
      print "Killed process PID: " + str(self.process.pid)
      print "Cleaned up everything. Good to go!"

  # run child process. 
  def run(self): 
    try:
      self.process = subprocess.Popen(self.command, stdout=subprocess.PIPE)
      print "Motion detection running on background with PID: " + str(self.process.pid)
      for line in iter(self.process.stdout.readline, ""):
        yield line
    except (KeyboardInterrupt, SystemExit):
      print "\nExiting..."

  # do your magic in here!
  def doMagic(self):
    for line in self.output:
      if line == "no motion\n":
        print "No motion detected!"
      elif line == "alert\n":
      	if (self.detectTime is None) or (diff>=1):
      		self.detectTime = datetime.now().time().strftime('%H:%M:%S')
      		self.sendMail()
      	timeNow = datetime.now().time().strftime('%H:%M:%S')	
      	diff = datetime.strptime(timeNow, self.FMT) - datetime.strptime(self.detectTime, self.FMT)
      	diff = diff.seconds/3600
        print "Somebody is in the room."
      else:
        print "Only god knows what's going on."
  
  def sendMail(self):
	# Create a text/plain message
	msg = MIMEText("There is motion in your room. Please, check your server for images!")
	me = self.email
	you = self.email
	msg['Subject'] = "Alert Alert!"
	msg['From'] = self.email
	msg['To'] = self.email

	# Send the message via our own SMTP server, but don't include the
	# envelope header.
	s = smtplib.SMTP('localhost')
	s.sendmail(me, [you], msg.as_string())
	s.quit()

md = MotionDetection()
md.doMagic()

