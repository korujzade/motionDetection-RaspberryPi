#!/usr/bin/python
import os
import signal
import atexit
import subprocess
from datetime import datetime, date, timedelta
# Import smtplib for the actual sending function
import smtplib
# Import the email modules we'll need
from email.mime.text import MIMEText

class MotionDetection:
  process = None
  command = ["./Main", "-vid"]
  output  = []
  detectTime = None
  timeNow = None
  diff = 0
  FMT = '%H:%M:%S' 

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
      		self.detectTime = datetime.now().time()
      		self.detectTime = self.detectTime.strftime('%H:%M:%S')
      		self.sendMail()
      	timeNow = datetime.now().time()	
      	timeNow = timeNow.strftime('%H:%M:%S')
      	diff = datetime.strptime(timeNow, self.FMT) - datetime.strptime(self.detectTime, self.FMT)
      	diff = diff.seconds/3600
        print "Somebody is in the room."
      else:
        print "Only god know what's going on."

  
  def sendMail(self):
  	# Open a plain text file for reading.  For this example, assume that
	# the text file contains only ASCII characters.
	#fp = open(textfile, 'rb')
	# Create a text/plain message
	msg = MIMEText("There is somebody in your room. Please check your server for images!")

	me = "From Email"
	you = "To Email"
	msg['Subject'] = "Alert Alert!"
	msg['From'] = "oruczade.kamil@gmail.com"
	msg['To'] = "oruczade.kamil@gmail.com"

	# Send the message via our own SMTP server, but don't include the
	# envelope header.
	s = smtplib.SMTP('localhost')
	s.sendmail(me, [you], msg.as_string())
	s.quit()	


md = MotionDetection()
md.doMagic()

