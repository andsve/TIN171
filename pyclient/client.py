import socket
import game
import agent
import random

try:
    import graphdump
    HAS_GRAPHWIZ = True
except:
    HAS_GRAPHWIZ = False
    print "warning: python library 'yapgvb' and graphwiz is needed to dump images of the graph"
    

# Set up logging
import time
import logging
import logging.handlers

class ConsolePrettyPrinter(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)
    def emit(self, record):
        import utils
        import os
        prefix = '{0}:{1}:'.format(record.module, record.levelname)
        padding = " " * (13 - len(prefix))
        
        color = {"client":'white'
                , "game":'red'
                , "agent":'green'
                , "planner":'yellow'}.setdefault(record.module, 'grey')
        
        if os.name == 'nt':
            utils.nt_set_color(color)
        print padding + prefix,
        if os.name == 'nt':
            utils.nt_set_color('grey')
            
        if os.name == 'nt' and record.levelname == "CRITICAL":
            utils.nt_set_color('red')
        print record.message
        if os.name == 'nt' and record.levelname == "CRITICAL":
            utils.nt_set_color('grey')            
            
        

logconsole = ConsolePrettyPrinter()
logconsole.setLevel(logging.INFO)

js_logger = logging.getLogger("")
logging.basicConfig(filename="robot-output.{0}.log".format(time.strftime("%H%M%S")),filemode="w",level=logging.DEBUG,format="%(module)s:%(levelname)s: %(message)s")
js_logger.addHandler(logconsole)


class Client:
    def __init__(self):
        self.socket = None
        self.agent = None #= agent.Agent(self.game)
        self.game = None

        self.resources = {"SHEEP": 0
                        ,"VICTORY_CARDS": 0
                        ,"WHEAT": 0
                        ,"SETTLEMENTS": 5
                        ,"MONOPOLY_CARDS": 0
                        ,"KNIGHT_CARDS": 0
                        ,"DEV_CARDS": 25
                        ,"ROAD_CARDS": 0
                        ,"MAY_PLAY_DEVCARD": False
                        ,"WOOD": 0
                        ,"CITIES": 4
                        ,"CLAY": 0
                        ,"ROADS": 15
                        ,"NUMKNIGHTS": 0
                        ,"ORE": 0
                        ,"RESOURCE_CARDS": 0}
                        
        self.builtnodes = []
        self.builtroads = []

    def connect(self, server):
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect(server)
        except:
            return False
        return True
    
    def make_message(self, raw_msg):
        highByte = chr(len(raw_msg) / 256)
        lowByte = chr(len(raw_msg) % 256)
        return highByte + lowByte + raw_msg
          
    def send_msg(self, msg):
        logging.debug("Sending: {0}".format(msg.to_cmd()))
        self.client.send(self.make_message(msg.to_cmd()))
            
    def run(self, gamename, autostart, seat_num):
        gamejoined = False
        satdown = False
        gamestarted = False
        
        nickname = "aiBot-{1}[{0}]".format(socket.gethostname(), random.randint(0, 99))
        #gamename = "sventest" #use static name for testing against others
        
        if gamename == None:
            gamename = "game-{1}[{0}]".format(socket.gethostname(), random.randint(0, 99))
        
        self.game = game.Game(nickname,self.resources,self.builtnodes,self.builtroads)
        self.agent = agent.Agent(nickname, gamename, self.game, self, self.resources,self.builtnodes,self.builtroads)
        
        while True:
            highByte = ord(self.client.recv(1))
            lowByte = ord(self.client.recv(1))
            transLength = highByte * 256 + lowByte
            msg = self.client.recv(transLength)
            
            try:
                parsed = self.game.parse_message(msg)
            except:
                logging.critical("Failed to parse this message: {0}".format(msg))
                # TODO: Attempt to skip message
                continue
                
            if parsed == None:
                logging.debug("Message not supported -- {0}".format(msg))
                continue
            else:
                (msg, message) = parsed
            
            # Graph dump on these messages
#            if msg in ["PutPieceMessage", "BoardLayoutMessage"]:
#                if HAS_GRAPHWIZ:
#                    graphdump.generate_graph(self.game)
            
            if msg == "GamesMessage" and not gamejoined:
                # We receive a channel list and a game list
                gamejoined = True
                logging.info("Starting a new game...")
                m = game.JoinGameMessage(nickname, "", socket.gethostname(), gamename)
                self.send_msg(m)

            elif msg == "JoinGameMessage" and not satdown:
                # We receive confirmation of a game created, available seats, etc
                satdown = True
                logging.info("Sitting down...")
                m = game.SitDownMessage(gamename, nickname, seat_num, False)
                self.send_msg(m)
                
            elif msg == "ChangeFaceMessage" and not gamestarted:
                # We receive starting values, 0 of each resource, game state and game face
                gamestarted = True
                logging.info("Starting game...")
                if autostart:
                    m = game.StartGameMessage(gamename)
                    self.send_msg(m)
            
            elif msg == "GameTextMsgMessage":
                import pdb
                import messages
                logging.info("(Chat) {0}".format(message.message))
                g = self.game
                a = self.agent
                if message.message.upper().startswith("PDB"):
                    pdb.set_trace()
                elif message.message.upper().startswith("QUIT"):
                    logging.info("Server told me to quit!")
                    return
                    
                elif "can't build" in message.message:
                    logging.critical("BUG: Can not build, canceling all build requests!")
                    logging.critical(a.resources)
                    # Blah blah
                    #self.send_msg(messages.CancelBuildRequestMessage(gamename, 0))
                    #self.send_msg(messages.CancelBuildRequestMessage(gamename, 1))
                    #self.send_msg(messages.EndTurnMessage(gamename))
             
            elif msg == "GameStateMessage":
                logging.info("Switching gamestate to: {0}".format(message.state_name))
                
                if message.state_name == "OVER":
                    logging.info("The game is over.")
                    logging.info("Victory points: {0}".format(self.game.vp))
                    logging.info("Victory cards: {0}".format(self.agent.resources["VICTORY_CARDS"]))

             
            elif msg == "RobotDismissMessage":
                import messages
                logging.info("I AM OUT OF HERE, NO ROBOTS ALLOWED")
                self.send_msg(messages.LeaveGameMessage(nickname, socket.gethostname(), gamename))
               
            else:
                # Output only unhandeled messages to stdout
                if message == None:
                    logging.debug("{0} - NOT SUPPORTED".format(msg))
                    continue
                
                r = message.to_cmd()
                logging.debug("[{0}] {1}".format(msg, "to_cmd() NOT IMPLEMENTED"if r == None else r))

            # Dispatch message to agent
            self.agent.handle_message(msg, message)
            
            """Game has STARTED! We get information about board layout, resources, starting player, etc"""
                        

def main(args):
    from sys import exit
    from optparse import OptionParser
    
    parser = OptionParser()
    parser.add_option("-a", "--addr", default = "home.md5.se:8880")
    parser.add_option("-s", "--seat", type="int", default = 1)
    parser.add_option("-g", "--game", default = None)
    parser.add_option("-w", "--wait", action="store_true", default = False)
    
    (options, args) = parser.parse_args()
    
    print options
    
    if ":" not in options.addr:
        print "try using host:port"
        sys.exit(-1)
    host, port = options.addr.split(":")
    
    client = Client()
    if not client.connect((host, int(port))):
        print("Could not connect to: {0}".format(options.addr))
        exit(-1)
        
    client.run(options.game, not options.wait, options.seat)

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