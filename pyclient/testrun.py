import logging
from threading import *
from client import *

# Number of total threads at any time
total_threads = 10
num_simul = Semaphore(total_threads)

# Total number of games to run
num_games = 10

# Score results are saved in this list
res = []

# somewhat of a threadsafe print function
print_sem = Semaphore()
def tprint(txt):
    print_sem.acquire()
    print(txt)
    print_sem.release()

# Save score (threadsafe lols)
save_sem = Semaphore()
def save_score(i, v):
    save_sem.acquire()
    res[i] = v
    save_sem.release()

# A threaded client starter
class ThreadClient(Thread):
    def __init__(self, game_id, host, port):
        Thread.__init__(self)
        self.host = host
        self.port = port
        self.game_id = game_id
        
    def run(self):
        # Acquire a new thread semaphore
        num_simul.acquire()
        
        score = None
        while (score == None):
            self.client = Client()
        
            if not self.client.connect((self.host, int(self.port))):
                print("Could not connect to: {0}".format(self.host))
                exit(-1)
            
            tprint("Starting simulation client {0}...".format(self.game_id))
            score = self.client.run(None, True, 1)
            self.client = None
            if (score == None):
                tprint("Simulation client {0} has failed! Reported score: {1}".format(self.game_id, score))
            else:
                tprint("Simulation client {0} has finished. Reported score: {1}".format(self.game_id, score))
        
        # Save score in global list
        save_score(self.game_id, score)
        
        # Done with this thread!
        num_simul.release()

if __name__ == '__main__':
    import sys
    import os

    if os.name == 'nt':
        os.system("mode 80,60")
        os.system("mode con: cols=80 lines=900")
    
    logging.disable(logging.INFO)
    
    try:
        h = "doff.csbnet.se"
        p = 8880
        
        for i in range(num_games):
            res.append(0)
            
            t = ThreadClient(i, h, p)
            t.start()
        
        # Make sure all threads are done
        for i in range(total_threads):
            num_simul.acquire()
        
        # Display results
        tprint("------------------------------------")
        tprint("Results from {0} games...\n".format(num_games))
        for i in range(num_games):
            tprint("{0}: {1}".format(i+1, res[i]))
            
    except:
        import pdb
        import traceback
        traceback.print_exc(file=sys.stdout)
        pdb.set_trace()