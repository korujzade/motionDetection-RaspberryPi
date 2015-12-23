import paramiko
import glob
from os import path
import sftp
import os

remote_dir ="/home/frames"
with sftp.Server("root", "password", "server") as server:
    while True:	
	    for image in glob.glob("/path/to/local/dir*.jpg"):
	        base = path.basename(image)
	        server.upload(image, path.join(remote_dir, base))
	        os.remove(image)