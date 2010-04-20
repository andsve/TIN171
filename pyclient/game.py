from messages import *

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
            if g.endswith("Message") and hasattr(cg, "id"):
                self.messagetbl[str(cg.id)] = (cg, g)
    
    def parse_message(self, msg):
        """ Create a message from recieved data """
        id, txt = msg[:4], msg[5:]
        message_class, name = self.messagetbl[id]
        inst = message_class.parse(txt)
        if inst:
            self.update_game(name, inst)
        return (name, inst)
        
    def create_graph(self):
        import jsettlers_utils as soc
        
        all_hexes = {}
        all_roads = {}
        all_nodes = {}
        
        for hex in soc.hex_grid:
            # All nodes surrounding hex
            nodes = soc.nodes_around_hex(hex)
            all_hexes[hex] = nodes
            
            for node in nodes:
                # All roads going out from node
                r = soc.node_to_roads(node_to_roads)
            
            # All roads around hex
            roads = soc.roads_around_hex(hex)
            
    def update_game(self, id, message):
        """ Update game state """
        
        # Look up how the data is exposed by matching the id with the
        # message-classes listed below. Some of them will need some tweaking
        # (i.e.BankTradeMessage - must map Jsettlers resource id -> resource name)
        
        if id == "BoardLayoutMessage":
            # Set game board
            self.boardLayout = BoardLayout()

            # Add resource to all tiles
                        
            
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
        #static layout-info
        self.id = name
        self.n1 = neighbour1
        self.n2 = neighbour2
        #dynamic info
        self.owner = None

class BoardNode:
    def __init__(self, name, neighbour1, neighbour2, neighbour3, tile1, tile2, tile3):
        #static layout-info
        self.id = name
        self.n1 = neighbour1
        self.n2 = neighbour2
        self.n3 = neighbour3        
        self.t1 = tile1
        self.t2 = tile2
        self.t3 = tile3
        #dynamic info
        self.harbor = None
        self.owner = None

class TileNode:
    def __init__(self, name, neighbour1, neighbour2, neighbour3)
        #static layout-info
        self.id = name
        self.n1 = neighbour1
        self.n2 = neighbour2
        self.n3 = neighbour3
        self.n4 = neighbour4
        self.n5 = neighbour5
        self.n6 = neighbour6
        #dynamic info
        self.resource = None
        self.number = None

class BoardLayout:
    # Static look-up tables

    def __init__(self):
        pass
