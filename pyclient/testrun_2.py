import logging
import threading
from client import *
import socket

import multiprocessing

# Timeout before assuming game is dead
G_TIMEOUT = 60 * 3

# Number of total threads at any time
total_threads = 1
num_simul = multiprocessing.Semaphore(total_threads)

# Total number of games to run
num_games = 100

# Score results are saved in this list
res = []

# somewhat of a threadsafe print function
print_sem = multiprocessing.Semaphore()
def tprint(txt):
    print_sem.acquire()
    print(txt)
    print_sem.release()

# Save score (threadsafe lols)
save_sem = multiprocessing.Semaphore()
def save_score(i, v):
    save_sem.acquire()
    res[i] = v
    save_sem.release()

def run_client(i):
    import time
    start_time = time.time()
    tprint("Starting game {0}".format(i))
    logging.disable(logging.INFO)
    h = "doff.csbnet.se"
    p = 8880
    try_num = 1
    score = None
    while not score:
        n = "{0}-{1}".format(socket.gethostname(), i, try_num)
        client = Client()
        client.connect((h, p)) 
        client.setup(n, True, 1, n)
        score = client.run()

        if score in (None, -1, 0):
            tprint("Failed game {0}".format(i))
            return 0
            
        try_num += 1
    tprint("Finished game {0}: {1}, {2} seconds".format(i, score, time.time() - start_time))
    return score
    
if __name__ == '__main__':
    import sys
    import os
    import socket
    socket.setdefaulttimeout(G_TIMEOUT)
    
    if os.name == 'nt':
        os.system("mode 80,60")
        os.system("mode con: cols=80 lines=900")
    
    logging.disable(logging.INFO)
    
    try:
        pool = multiprocessing.Pool(processes = total_threads)
        it = pool.imap(run_client, range(num_games), 1)
        i = -1
        while i != None:
            try:
                i = it.next(timeout = G_TIMEOUT)
                res.append(i)
            except TypeError:
                tprint("Well WUT, that is really annoying isn't it? Fix plx.")
            except multiprocessing.TimeoutError:
                tprint("Hmz, timeout error!")
            except StopIteration:
                break
        
        # Display results
        tprint("------------------------------------")
        tprint("Results from {0} games...\n".format(len(res)))
        for x in range(0, 12):
            tprint("{0}p - {1}".format(x, res.count(x)))
            
        winratio = (res.count(10) + res.count(11)) / float(len(res))
        average = float(sum(res))/len(res)
        median = sorted(res)[len(res)/2]
        tprint("Win ratio: {0}, Average: {1}, Median: {2}".format(winratio, average, median))

            
        try:
            import pylab
            tprint("{0}/{1} tests failed.".format(res.count(0), len(res)))
            pylab.hist(res, bins=12, range=(0, 11), histtype="bar", align="mid")

            xmin, xmax, ymin, ymax = pylab.axis()
            pylab.axis([2, 12, ymin, ymax])
            pylab.show()
        except ImportError:
            tprint("Install numpy and matplotlib for sweet graphs!")

    except:
        import pdb
        import traceback
        traceback.print_exc(file=sys.stdout)
        pdb.set_trace()
