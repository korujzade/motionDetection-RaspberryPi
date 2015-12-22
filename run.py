#!/usr/bin/python
import os
import signal
import atexit
import subprocess

class MotionDetection:
  process = None
  command = ["./Main", "-vid"]
  output  = []

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
        print "Somebody is in the room."
      else:
        print "Only god know what's going on."

md = MotionDetection()
md.doMagic()

