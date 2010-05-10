import os
import socket
i = 1
while 1:
    os.system("client.py -a doff.csbnet.se:8880 -g {1}-r{0} -n {1}-b{0}".format(i, socket.gethostname()))
    i += 1