import subprocess
from subprocess import PIPE
import os
import sys
from pathlib import Path

fifo_path = Path("./mcfifo")
server_path = Path("../server/server.jar")
mc_server_command = f"java -Xms1G -Xmx1G -jar {server_path} nogui"

os.remove(fifo_path)
os.mkfifo(fifo_path)

#with open(fifo_path, "r") as fifo:
#fifo = open(fifo_path, "r")

#proc = subprocess.Popen(['ping', 'google.com'], stdout=PIPE, stdin=PIPE)

#proc.terminate()
