import socket
import game
import agent

import locale
locale.setlocale(locale.LC_ALL, 'en_US.ISO8859-1')

class Client:
    def __init__(self):
        self.game = game.Game()
        self.socket = None
        self.agent = None #= agent.Agent(self.game)
        
        
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
        print("Sending: {0}".format(msg.to_cmd()))
        self.client.send(self.make_message(msg.to_cmd()))
            
    def run(self):
        gamejoined = False
        satdown = False
        gamestarted = False
        
        nickname = "aiBot[{0}]".format(socket.gethostname())
        gamename = "game[{0}]".format(socket.gethostname())
        self.agent = agent.Agent(nickname, self.game)
        
        
        while True:
            """Receive high byte"""
            highByte = ord(self.client.recv(1))
            """Receive low byte"""
            lowByte = ord(self.client.recv(1))
            """Calculate length of the rest of the message and receive"""
            transLength = highByte * 256 + lowByte
            print "highByte: {0}, lowByte: {1}".format(highByte, lowByte)
            msg = self.client.recv(transLength)
            
            parsed = self.game.parse_message(msg)
            if parsed == None:
                print "Message not supported -- {0}".format(msg)
                continue
            else:
                (msg, message) = parsed
            
            if msg == "GamesMessage" and not gamejoined:
                # We receive a channel list and a game list
                gamejoined = True
                print("Making new game...")
                m = game.JoinGameMessage(nickname, "", socket.gethostname(), gamename)
                self.send_msg(m)

            elif msg == "JoinGameMessage" and not satdown:
                # We receive confirmation of a game created, available seats, etc
                satdown = True
                print("Sitting down...")
                m = game.SitDownMessage(gamename, nickname, 1, False)
                self.send_msg(m)
                
            elif msg == "ChangeFaceMessage" and not gamestarted:
                # We receive starting values, 0 of each resource, game state and game face
                gamestarted = True
                print("Starting game...")
                m = game.StartGameMessage(gamename)
                self.send_msg(m)
                
            elif msg == "BoardLayoutMessage":
                # We received gameboard information, pass it along to the Game-class.
                print "Got game board"
            
            elif msg == "GameTextMsgMessage":
                print "[GameTextMsgMessage] {0}".format(message.message)

            else:
                # Output only unhandeled messages to stdout
                if message == None:
                    print "{0} - NOT SUPPORTED".format(msg)
                    continue
                
                r = message.to_cmd()
                print "[{0}] {1}".format(msg, "to_cmd() NOT IMPLEMENTED"if r == None else r)

            # Dispatch message to agent
            self.agent.handle_message(msg, message)
            

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
