from subprocess import call
import os

os.chdir("motion/")
call(["cmake", "."])
call(["make"])

with open('../config.txt') as f:
	creds = [x.strip().split(':' , 1)[1] for x in f.readlines()]
try:
	call(["python", "md.py", creds[0], creds[1], creds[2], creds[3], creds[4], creds[5]])
except (KeyboardInterrupt, SystemExit):
	print "\nsee yaa!"	