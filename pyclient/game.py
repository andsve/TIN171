from messages import *

class Game:
    def __init__(self, nickname):
        # Initiate gameboard when the message is recieved?
        #self.gameboard = gameboard # save raw gameboad
        #self.parse_board()         # parse gameboard and create internal representation
        self.messagetbl = {}
        self.init_parser()
        self.nickname = nickname
        
    
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

        if id == "SitDownMessage" and message.nickname == self.nickname:

            self.playernum = message.playernum
        
        elif id == "BoardLayoutMessage":
            # Set game board
            self.boardLayout = BoardLayout()
            self.buildableNodes = BuildableNodes()
            self.buildableRoads = BuildableRoads()

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

            # Harbours
            harbour_coords = [(0x27, 0x38), (0x5a, 0x6b), (0x9c, 0xad)
                             ,(0x25, 0x34), (0xcd, 0xdc), (0x43, 0x52)
                             ,(0xc9, 0xda), (0x72, 0x83), (0xa5, 0xb6)]
                             
            hex_indicies = [0, 2, 8, 9, 21, 22, 32, 33, 35]
                            
            for num, cs in zip(hex_indicies, harbour_coords):
                board_tile = soc.board_indicators[message.hexes[num]]
                if board_tile in soc.harbour_to_resource:
                    harbor_type = soc.harbour_to_resource[board_tile]
                else:
                    harbor_type = 0
                self.boardLayout.nodes[cs[0]].harbor = harbor_type
                self.boardLayout.nodes[cs[1]].harbor = harbor_type

            #set the robber location
            self.boardLayout.robberpos = message.robberpos
                       
        elif id == "PutPieceMessage":
            print "PutPieceMessage: {0}".format(message.values())
            if message.piecetype == 1:
                self.boardLayout.nodes[message.coords].owner = message.playernum

                #May not build on neighbouring nodes
                if self.boardLayout.nodes[message.coords].n1:
                    road = self.boardLayout.nodes[message.coords].n1
                    id1 = self.boardLayout.roads[road].n1
                    id2 = self.boardLayout.roads[road].n2
                    self.buildableNodes.nodes[id1] = False
                    self.buildableNodes.nodes[id2] = False

                if self.boardLayout.nodes[message.coords].n2:
                    road = self.boardLayout.nodes[message.coords].n2
                    id1 = self.boardLayout.roads[road].n1
                    id2 = self.boardLayout.roads[road].n2
                    self.buildableNodes.nodes[id1] = False
                    self.buildableNodes.nodes[id2] = False

                if self.boardLayout.nodes[message.coords].n3:
                    road = self.boardLayout.nodes[message.coords].n3
                    id1 = self.boardLayout.roads[road].n1
                    id2 = self.boardLayout.roads[road].n2
                    self.buildableNodes.nodes[id1] = False
                    self.buildableNodes.nodes[id2] = False
       
            elif message.piecetype == 0:
                self.boardLayout.roads[message.coords].owner = message.playernum

                #May not build on built roads
                self.buildableRoads.roads[message.coords] = False
                #May build on roads adjacent to built roads
                
                if message.player == self.playernum:
                    n1 = self.boardLayout.roads[message.coords].n1
                    n2 = self.boardLayout.roads[message.coords].n2

                    r1 = self.boardLayout.nodes[n1].n1
                    r2 = self.boardLayout.nodes[n1].n2
                    r3 = self.boardLayout.nodes[n1].n3

                    if r1 and self.boardLayout.roads[r1].owner == None:
                        self.buildableRoads.roads[message.coords] = True

                    if r2 and self.boardLayout.roads[r2].owner == None:
                        self.buildableRoads.roads[r2] = True

                    if r3 and self.boardLayout.roads[r3].owner == None:
                        self.buildableRoads.roads[r3] = True
                        
                    r1 = self.boardLayout.nodes[n2].n1
                    r2 = self.boardLayout.nodes[n2].n2
                    r3 = self.boardLayout.nodes[n2].n3

                    if r1 and self.boardLayout.roads[r1].owner == None:
                        self.buildableRoads.roads[message.coords] = True

                    if r2 and self.boardLayout.roads[r2].owner == None:
                        self.buildableRoads.roads[r2] = True

                    if r3 and self.boardLayout.roads[r3].owner == None:
                        self.buildableRoads.roads[r3] = True

                
        elif id == "MoveRobberMessage":
            print "MoveRobberMessage: {0}".format(message.values())
            self.boardLayout.robberpos = message.coords
            
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

    def __init__(self):

        self.robberpos = None
        
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
            self.tiles[tile] = TileNode(tile, *nodes)
            
class BuildableNodes:

    def __init__(self):

        import jsettlers_utils as soc
        self.nodes = {}
        for k in soc.nodeLUT:
            self.nodes[k] = True

class BuildableRoads:

    def __init__(self)

        import jsettlers_utils as soc
        self.roads = {}
        for k in soc.roadLUT:
            self.roads[k] = False
