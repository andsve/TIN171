import socket
import game

from messages import ToMessage
from messages import MakeMessage

import game

class Client:
    def __init__(self):
        self.socket = None
        
    def connect(self, server):
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect(server)
        except:
            return False
        return True
          
    def sendMsg(self, msg):
		print("Sending: {0}".format(msg.toCmd()))
		self.client.send(MakeMessage(msg.toCmd()))
            
    def run(self):
        gamejoined = False
        satdown = False
        gamestarted = False
        
        while True:
            print("waiting to receive")
            """Receive high byte"""
            highByte = ord(self.client.recv(1))
            """Receive low byte"""
            lowByte = ord(self.client.recv(1))
            """Calculate length of the rest of the message and receive"""
            transLength = highByte * 256 + lowByte
            msg = self.client.recv(transLength)
            print(msg)

            """We receive a channel list and a game list"""
            """JOINGAME sep nickname sep2 password sep2 host sep2 game"""
            if msg[0:4] == "1019" and not gamejoined:
                gamejoined = True
                print("Making new game...")
                m = game.JoinGameMessage("aiBot", "", socket.gethostname(), "game")
                self.sendMsg(m)

            """We receive confirmation of a game created, available seats, etc"""
            """SITDOWN sep game sep2 nickname sep2 playerNumber sep2 robotFlag"""    
            if msg[0:4] == "1013" and not satdown:
                satdown = True
                print("Sitting down...")
                m = game.SitDownMessage("game", "aiBot", 1, False)
                self.sendMsg(m)
                

            """We receive starting values, 0 of each resource, game state and game face"""
            """STARTGAME sep game"""
            if msg[0:4] == "1058" and not gamestarted:
                gamestarted = True
                print("Starting game...")
                m = game.StartGameMessage("game")
                self.sendMsg(m)
                
            
            """ We received gameboard information, pass it along to the Game-class. """
            if msg[0:4] == "1014":
                honker = game.Game(msg[10:].split(","))
                #m = game.ParseMsg(msg)

            """Game has STARTED! We get information about board layout, resources, starting player, etc"""
                        

def main(args):
    from sys import exit
    
    if len(args) == 2:
        addr = args[0]
        port = int(args[1])
    else:
        addr = "komugi.se"
        port = 8880
    
    server = (addr, port)
    client = Client()
    if not client.connect(server):
        print("Could not connect to: {0}".format(server))
        exit(-1)

    print("connected")
    client.run()

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
