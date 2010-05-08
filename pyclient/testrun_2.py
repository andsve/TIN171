import logging
import threading
from client import *
import socket

import multiprocessing

# Number of total threads at any time
total_threads = 8
num_simul = threading.Semaphore(total_threads)

# Total number of games to run
num_games = 100

# Score results are saved in this list
res = []

# somewhat of a threadsafe print function
print_sem = threading.Semaphore()
def tprint(txt):
    print_sem.acquire()
    print(txt)
    print_sem.release()

# Save score (threadsafe lols)
save_sem = threading.Semaphore()
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
        score = client.run(n, True, 1, n)
        
        if not score:
            tprint("Failed game {0}".format(i))
        
        try_num += 1
    tprint("Finished game {0}: {1}, {2} seconds".format(i, score, time.time() - start_time))
    return score
    
if __name__ == '__main__':
    import sys
    import os

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
                i = it.next(timeout = 60*3)
                res.append(i)
            except TypeError:
                tprint("Well WUT, that is really annoying isn't it? Fix plx.")
            except multiprocessing.TimeoutError:
                tprint("Hmz, timeout error!")
                res.append(None)
            except StopIteration:
                break
        
        # Display results
        tprint("------------------------------------")
        tprint("Results from {0} games...\n".format(num_games))
        print res
        for i, v in enumerate(res):
            tprint("{0}: {1}".format(i+1, v))
            
        try:
            import pylab
            data = map(lambda x: 1 if x == None else x, res)
            pylab.hist(data, range=(1, 11), histtype="barstacked")
            pylab.show()
        except ImportError:
            tprint("Install numpy and matplotlib for sweet graphs!")

    except:
        import pdb
        import traceback
        traceback.print_exc(file=sys.stdout)
        pdb.set_trace()