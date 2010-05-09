import os
i = 1
while 1:
    os.system("client.py -g run{0} -n bot{0}".format(i))
    i += 1