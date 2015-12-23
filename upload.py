import paramiko
import glob
from os import path
import sftp

remote_dir ="/home/frames"

with sftp.Server("root", "password", "server") as server:
    for image in glob.glob("/local/path/*.jpg"):
        base = path.basename(image)
        server.upload(image, path.join(remote_dir, base))