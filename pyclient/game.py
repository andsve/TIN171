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
        
        if not id in self.messagetbl:
            print "ERROR: can not parse '{0}'".format(msg)
            return
        
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
        import sys
        """ Update game state """
        
        # Look up how the data is exposed by matching the id with the
        # message-classes listed below. Some of them will need some tweaking
        # (i.e.BankTradeMessage - must map Jsettlers resource id -> resource name)
        
        if id == "BoardLayoutMessage":
            # Set game board
            self.boardLayout = BoardLayout()

            import jsettlers_utils as soc

            # Add resources and numbers to all tiles
            self.boardLayout.tiles[0x37].resource = message.hexes[5]
            self.boardLayout.tiles[0x37].number = soc.number_dict[message.numbers[5]]
            self.boardLayout.tiles[0x59].resource = message.hexes[6]
            self.boardLayout.tiles[0x59].number = soc.number_dict[message.numbers[6]]
            self.boardLayout.tiles[0x7b].resource = message.hexes[7]
            self.boardLayout.tiles[0x7b].number = soc.number_dict[message.numbers[7]]
            self.boardLayout.tiles[0x35].resource = message.hexes[10]
            self.boardLayout.tiles[0x35].number = soc.number_dict[message.numbers[10]]
            self.boardLayout.tiles[0x57].resource = message.hexes[11]
            self.boardLayout.tiles[0x57].number = soc.number_dict[message.numbers[11]]
            self.boardLayout.tiles[0x79].resource = message.hexes[12]
            self.boardLayout.tiles[0x79].number = soc.number_dict[message.numbers[12]]
            self.boardLayout.tiles[0x9b].resource = message.hexes[13]
            self.boardLayout.tiles[0x9b].number = soc.number_dict[message.numbers[13]]
            self.boardLayout.tiles[0x33].resource = message.hexes[16]
            self.boardLayout.tiles[0x33].number = soc.number_dict[message.numbers[16]]
            self.boardLayout.tiles[0x55].resource = message.hexes[17]
            self.boardLayout.tiles[0x55].number = soc.number_dict[message.numbers[17]]
            self.boardLayout.tiles[0x77].resource = message.hexes[18]
            self.boardLayout.tiles[0x77].number = soc.number_dict[message.numbers[18]]
            self.boardLayout.tiles[0x99].resource = message.hexes[19]
            self.boardLayout.tiles[0x99].number = soc.number_dict[message.numbers[19]]
            self.boardLayout.tiles[0xbb].resource = message.hexes[20]
            self.boardLayout.tiles[0xbb].number = soc.number_dict[message.numbers[20]]
            self.boardLayout.tiles[0x53].resource = message.hexes[23]
            self.boardLayout.tiles[0x53].number = soc.number_dict[message.numbers[23]]
            self.boardLayout.tiles[0x75].resource = message.hexes[24]
            self.boardLayout.tiles[0x75].number = soc.number_dict[message.numbers[24]]
            self.boardLayout.tiles[0x97].resource = message.hexes[25]
            self.boardLayout.tiles[0x97].number = soc.number_dict[message.numbers[25]]
            self.boardLayout.tiles[0xb9].resource = message.hexes[26]
            self.boardLayout.tiles[0xb9].number = soc.number_dict[message.numbers[26]]
            self.boardLayout.tiles[0x73].resource = message.hexes[29]
            self.boardLayout.tiles[0x73].number = soc.number_dict[message.numbers[29]] 
            self.boardLayout.tiles[0x95].resource = message.hexes[30]
            self.boardLayout.tiles[0x95].number = soc.number_dict[message.numbers[30]]
            self.boardLayout.tiles[0xb7].resource = message.hexes[31]
            self.boardLayout.tiles[0xb7].number = soc.number_dict[message.numbers[31]]

            #fix harbors

            #first harbor (0x17)
            if message.hexes[0] in soc.harbors['clay']:
                harbor_type = 1
            elif message.hexes[0] in soc.harbors['ore']:
                harbor_type = 2
            elif message.hexes[0] in soc.harbors['sheep']:
                harbor_type = 3
            elif message.hexes[0] in soc.harbors['grain']:
                harbor_type = 4
            elif message.hexes[0] in soc.harbors['lumber']:
                harbor_type = 5
            elif message.hexes[0] in soc.harbors['3for1']:
                harbor_type = 6
            else:
                harbor_type = 0
                
            #set Node(0x27) and Node(0x38) to harbor = #resource
            self.boardLayout.nodes[0x27].harbor = harbor_type
            self.boardLayout.nodes[0x38].harbor = harbor_type

            #second harbor (0x5b)
            if message.hexes[2] in soc.harbors['clay']:
                harbor_type = 1
            elif message.hexes[2] in soc.harbors['ore']:
                harbor_type = 2
            elif message.hexes[2] in soc.harbors['sheep']:
                harbor_type = 3
            elif message.hexes[2] in soc.harbors['grain']:
                harbor_type = 4
            elif message.hexes[2] in soc.harbors['lumber']:
                harbor_type = 5
            elif message.hexes[2] in soc.harbors['3for1']:
                harbor_type = 6
            else:
                harbor_type = 0
                
            #set Node(0x5a) and Node(0x6b) to harbor = #resource
            self.boardLayout.nodes[0x5a].harbor = harbor_type
            self.boardLayout.nodes[0x6b].harbor = harbor_type

            #third harbor (0x9d)
            if message.hexes[8] in soc.harbors['clay']:
                harbor_type = 1
            elif message.hexes[8] in soc.harbors['ore']:
                harbor_type = 2
            elif message.hexes[8] in soc.harbors['sheep']:
                harbor_type = 3
            elif message.hexes[8] in soc.harbors['grain']:
                harbor_type = 4
            elif message.hexes[8] in soc.harbors['lumber']:
                harbor_type = 5
            elif message.hexes[8] in soc.harbors['3for1']:
                harbor_type = 6
            else:
                harbor_type = 0
                
            #set Node(0x9c) and Node(0xad) to harbor = #resource
            self.boardLayout.nodes[0x9c].harbor = harbor_type
            self.boardLayout.nodes[0xad].harbor = harbor_type

            #forth harbor (0x13)
            if message.hexes[9] in soc.harbors['clay']:
                harbor_type = 1
            elif message.hexes[9] in soc.harbors['ore']:
                harbor_type = 2
            elif message.hexes[9] in soc.harbors['sheep']:
                harbor_type = 3
            elif message.hexes[9] in soc.harbors['grain']:
                harbor_type = 4
            elif message.hexes[9] in soc.harbors['lumber']:
                harbor_type = 5
            elif message.hexes[9] in soc.harbors['3for1']:
                harbor_type = 6
            else:
                harbor_type = 0
                
            #set Node(0x25) and Node(0x34) to harbor = #resource
            self.boardLayout.nodes[0x25].harbor = harbor_type
            self.boardLayout.nodes[0x34].harbor = harbor_type

            #fifth harbor (0xdd)
            if message.hexes[21] in soc.harbors['clay']:
                harbor_type = 1
            elif message.hexes[21] in soc.harbors['ore']:
                harbor_type = 2
            elif message.hexes[21] in soc.harbors['sheep']:
                harbor_type = 3
            elif message.hexes[21] in soc.harbors['grain']:
                harbor_type = 4
            elif message.hexes[21] in soc.harbors['lumber']:
                harbor_type = 5
            elif message.hexes[21] in soc.harbors['3for1']:
                harbor_type = 6
            else:
                harbor_type = 0
                
            #set Node(0xcd) and Node(0xdc) to harbor = #resource
            self.boardLayout.nodes[0xcd].harbor = harbor_type
            self.boardLayout.nodes[0xdc].harbor = harbor_type

            #sixth harbor (0x31)
            if message.hexes[22] in soc.harbors['clay']:
                harbor_type = 1
            elif message.hexes[22] in soc.harbors['ore']:
                harbor_type = 2
            elif message.hexes[22] in soc.harbors['sheep']:
                harbor_type = 3
            elif message.hexes[22] in soc.harbors['grain']:
                harbor_type = 4
            elif message.hexes[22] in soc.harbors['lumber']:
                harbor_type = 5
            elif message.hexes[22] in soc.harbors['3for1']:
                harbor_type = 6
            else:
                harbor_type = 0
                
            #set Node(0x43) and Node(0x52) to harbor = #resource
            self.boardLayout.nodes[0x43].harbor = harbor_type
            self.boardLayout.nodes[0x52].harbor = harbor_type

            #seventh harbor (0xd9)
            if message.hexes[32] in soc.harbors['clay']:
                harbor_type = 1
            elif message.hexes[32] in soc.harbors['ore']:
                harbor_type = 2
            elif message.hexes[32] in soc.harbors['sheep']:
                harbor_type = 3
            elif message.hexes[32] in soc.harbors['grain']:
                harbor_type = 4
            elif message.hexes[32] in soc.harbors['lumber']:
                harbor_type = 5
            elif message.hexes[32] in soc.harbors['3for1']:
                harbor_type = 6
            else:
                harbor_type = 0
                
            #set Node(0xc9) and Node(0xda) to harbor = #resource
            self.boardLayout.nodes[0xc9].harbor = harbor_type
            self.boardLayout.nodes[0xda].harbor = harbor_type

            #eigth harbor (0x71)
            if message.hexes[33] in soc.harbors['clay']:
                harbor_type = 1
            elif message.hexes[33] in soc.harbors['ore']:
                harbor_type = 2
            elif message.hexes[33] in soc.harbors['sheep']:
                harbor_type = 3
            elif message.hexes[33] in soc.harbors['grain']:
                harbor_type = 4
            elif message.hexes[33] in soc.harbors['lumber']:
                harbor_type = 5
            elif message.hexes[33] in soc.harbors['3for1']:
                harbor_type = 6
            else:
                harbor_type = 0    
                
            #set Node(0x72) and Node(0x83) to harbor = #resource
            self.boardLayout.nodes[0x72].harbor = harbor_type
            self.boardLayout.nodes[0x83].harbor = harbor_type

            #ninth harbor (0xb5)
            if message.hexes[35] in soc.harbors['clay']:
                harbor_type = 1
            elif message.hexes[35] in soc.harbors['ore']:
                harbor_type = 2
            elif message.hexes[35] in soc.harbors['sheep']:
                harbor_type = 3
            elif message.hexes[35] in soc.harbors['grain']:
                harbor_type = 4
            elif message.hexes[35] in soc.harbors['lumber']:
                harbor_type = 5
            elif message.hexes[35] in soc.harbors['3for1']:
                harbor_type = 6
            else:
                harbor_type = 0
                
            #set Node(0xa5) and Node(0xb6) to harbor = #resource
            self.boardLayout.nodes[0xa5].harbor = harbor_type
            self.boardLayout.nodes[0xb6].harbor = harbor_type

            #set the robber location
            self.boardLayout.robberLoc = message.robberpos
            
        elif id == "PlayerElementMessage":
            # Update resources
            pass
            
        elif id == "PutPieceMessage":
            print "PutPieceMessage: {0}".format(message.values())
            if message.piecetype == 1:
                self.boardLayout.nodes[message.coords].owner = message.playernum
            elif message.piecetype == 0:
                self.boardLayout.roads[message.coords].owner = message.playernum
            
        elif id == "MoveRobberMessage":
            print "MoveRobberMessage: {0}".format(message.values())
            self.boardLayout.robberLoc = message.coords
            
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
        self.harbor = 0
        self.owner = None    

class TileNode:
    def __init__(self, name, neighbour1, neighbour2
                  , neighbour3, neighbour4, neighbour5, neighbour6):
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

    self.robberLoc = None

    def __init__(self):
        import jsettlers_utils as soc
        self.roads = {}
        for k,v in soc.roadLUT.items():
            self.roads[k] = RoadNode(*v)
        
        self.nodes = {}
        for k, v in soc.nodeLUT.items():
            self.nodes[k] = BoardNode(*v)
            
        self.tiles = {}
        for tile in soc.hex_grid:
            if tile in [0x11, 0x13, 0x15, 0x17
                            ,0x39, 0x5b, 0x7d, 0x9d
                            ,0xbd, 0xdd, 0xdb, 0xd9
                            ,0xd7, 0xb5, 0x93, 0x71
                            ,0x51, 0x31]:
                continue
            nodes = soc.nodes_around_hex(tile)
            self.tiles[tile] = TileNode(tile, *[self.nodes[n] for n in nodes])
       
