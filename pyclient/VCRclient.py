import client
import pickle
from copy import deepcopy

class VCRClient(client.Client):
    def __init__(self, playbackFile = "vcrclient.rec", record = False):
        client.Client.__init__(self)
        
        self.playbackFile = playbackFile
        self.record = record
        self.playback = not record
        
        self.record_data = {}
        self.i = 0
        
        self.current_turn = -1
    
    def connect(self, server):
        if self.record:
            print("VCRClient - Recording mode")
            return client.Client.connect(self, server)
        
        # Load recorded data
        print("VCRClient - Playback mode")
        print("Reading playback data...")
        pkl_file = open(self.playbackFile, 'rb')
        self.record_data = pickle.load(pkl_file)
        pkl_file.close()
        return True
        
    def setup(self, gamename, autostart, seat_num, nickname = None):
        if self.record:
            client.Client.setup(self, gamename, autostart, seat_num, nickname)
            self.record_data = {'nickname': self.nickname, 'gamename': self.gamename, 'frames': []}
        else:
            # Playback
            self.gamejoined = True
            self.satdown = True
            self.gamestarted = True
            
            self.autostart = autostart
            self.seat_num = seat_num
            
            self.nickname = self.record_data['nickname']
            self.gamename = self.record_data['gamename']
            
            
    def run_update(self, i = -1):
        if self.record:
            res = client.Client.run_update(self)
            
            # Record data!
            if self.stats['TURN_ACTIVE'] != self.current_turn:
                self.current_turn = self.stats['TURN_ACTIVE']
                print("Recording data... (Turn {0})".format(self.current_turn))
                self.record_data['frames'].append({'game': deepcopy(self.game), 'resources': deepcopy(self.resources)})
            
            if res:
                print("Recording over, saving to file: {0}".format(self.playbackFile))
                output = open(self.playbackFile, 'wb')
                pickle.dump(self.record_data, output)
                output.close()
                
            return res
        else:
            frame = i
            if i == -1:
                if self.i >= len(self.record_data['frames']):
                    self.i = len(self.record_data['frames'])
                frame = self.i
                self.i += 1
            
            if frame >= len(self.record_data['frames']):
                frame = len(self.record_data['frames'])
            
            print("Playback frame #{0}...".format(frame))
            
            # Setup frame data
            if frame < len(self.record_data['frames']):
                self.game = self.record_data['frames'][frame]['game']
                self.resources = self.record_data['frames'][frame]['resources']
            #else:
            #    return 9001 # LOL WUT
    def reset_playback(self):
        self.i = 0



def main(args):
    from sys import exit
    from optparse import OptionParser
    import logging
    
    
    parser = OptionParser()
    parser.add_option("-a", "--addr", default = "localhost:8880")
    parser.add_option("-s", "--seat", type="int", default = 1)
    parser.add_option("-g", "--game", default = None)
    parser.add_option("-n", "--nick", default = None)
    parser.add_option("-w", "--wait", action="store_true", default = False)
    parser.add_option("-r", "--recordfile", default = "vcrclient.rec")
    parser.add_option("-p", "--play", action="store_true", default = False)
    
    (options, args) = parser.parse_args()
    
    print options
    
    if ":" not in options.addr:
        print "try using host:port"
        sys.exit(-1)
    host, port = options.addr.split(":")
    
    client = VCRClient(options.recordfile, not options.play)
    if not client.connect((host, int(port))):
        print("Could not connect to: {0}".format(options.addr))
        exit(-1)
    
    client.setup(options.game, not options.wait, options.seat, options.nick)
    client.run()

if __name__ == '__main__':
    import sys
    import os

    if os.name == 'nt':
        os.system("mode 80,60")
        os.system("mode con: cols=80 lines=900")
    
    try:
        main(sys.argv[1:])
    except:
        import pdb
        import traceback
        traceback.print_exc(file=sys.stdout)
        pdb.set_trace()