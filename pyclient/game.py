from messages import *
import pdb

class Game:
    def __init__(self):
        # Initiate gameboard when the message is recieved?
        #self.gameboard = gameboard # save raw gameboad
        #self.parse_board()         # parse gameboard and create internal representation
        self.messagetbl = {}
        self.init_parser()
    
    def init_parser(self):
        """ Create a LUT for message id => message instance """
        self.messagetbl = {}
        for g in globals():
            cg = globals()[g]
            if str(g).endswith("Message") and hasattr(cg, "id"):
                self.messagetbl[str(cg.id)] = (cg, g)
    
    def parse_message(self, msg):
        """ Create a message from recieved data """
        id, txt = msg[:4], msg[5:]
        message_class, name = self.messagetbl[id]
        inst = message_class.parse(txt)
        if inst:
            self.update_game(name, inst)
        return (name, inst)
        
    def update_game(self, id, message):
        """ Update game state """
        
        # Look up how the data is exposed by matching the id with the
        # message-classes listed below. Some of them will need some tweaking
        # (i.e.BankTradeMessage - must map Jsettlers resource id -> resource name)
        
        if id == "BoardLayoutMessage":
            # Set game board
            self.boardLayout = BoardLayout()

            # Add resource to all neighbours
            if message.board[5] != 0:
             """self.boardLayout[ord('\x27')].addResource(message.board[5])
                self.boardLayout[ord('\x36')].addResource(message.board[5])
                self.boardLayout[ord('\x38')].addResource(message.board[5])
                self.boardLayout[ord('\x47')].addResource(message.board[5])
                self.boardLayout[ord('\x49')].addResource(message.board[5])
                self.boardLayout[ord('\x58')].addResource(message.board[5])"""
            
            pass               
            
        elif id == "PlayerElementMessage":
            # Update resources
            pass
            
        elif id == "PutPieceMessage":
            print "PutPieceMessage: {0}".format(message.values())
            
        elif id == "MoveRobberMessage":
            print "MoveRobberMessage: {0}".format(message.values())
            
        elif id == "LastSettlementMessage":
            print "LastSettlementMessage: {0}".format(message.values())
            
    def parse_board(self):
        for elt in self.gameboard:
            print(elt)
            #pass # TODO: parse the gameboard information sent by the server

class RoadNode:
    def __init__(self, name, neighbour1, neighbour2):
        self.id = name
        self.n1 = neighbour1
        self.n2 = neighbour2
        self.owner = None

class BoardNode:
    def __init__(self, name, neighbour1, neighbour2, neighbour3):
        self.id = name
        self.n1 = neighbour1
        self.n2 = neighbour2
        self.n3 = neighbour3
        self.harbor = None
        self.resource1 = None
        self.resource2 = None
        self.resource3 = None

class BoardLayout:
    # Static look-up tables

    def __init__(self):
        pass
