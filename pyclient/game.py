import logging
from messages import *
from utils import cprint

class Game:
    def __init__(self, nickname, stats, resources,nodes,roads,harbor_list):
        self.messagetbl = {}
        self.init_parser()
        self.nickname = nickname
        self.stats = stats
        self.playernum = -1

        self.output_prefix = "[DEBUG] game.py ->"

        self.resources = resources
        self.builtnodes = nodes
        self.builtroads = roads
        
        # keep track of victory points for all players
        self.vp = {0: 0, 1: 0, 2: 0, 3: 0}
        self.longest_road = -1
        self.largest_army = -1
        
        self.boardLayout = None

        self.harbor_list = harbor_list
        

    def debug_print(self, msg):
        logging.info(msg)
       #cprint("{0} {1}".format(self.output_prefix, msg), 'blue')        
    
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
            logging.critical("Can not parse '{0}'".format(msg))
            return
        
        message_class, name = self.messagetbl[id]
        inst = message_class.parse(txt)
        if inst:
            self.update_game(name, inst)
        return (name, inst)
        
    """
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
    """
    def update_game(self, id, message):
        import sys
        import jsettlers_utils as soc
        """ Update game state """
        
        # Look up how the data is exposed by matching the id with the
        # message-classes listed below. Some of them will need some tweaking
        # (i.e.BankTradeMessage - must map Jsettlers resource id -> resource name)

        if id == "SitDownMessage" and message.nickname == self.nickname:
            self.playernum = message.playernum
        
        # Count longest round points
        elif id == "LongestRoadMessage" and message.playernum >= 0:
            self.longest_road = int(message.playernum)

        
        # Keep track of largest army message
        elif id == "LargestArmyMessage" and message.playernum >= 0:
            self.largest_army = int(message.playernum)
        
        elif id == "BoardLayoutMessage":
            # Set game board
            self.boardLayout = BoardLayout()
            self.buildableNodes = BuildableNodes()
            self.buildableRoads = BuildableRoads()

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
                harbor_type = 0
                if board_tile in soc.harbour_to_resource:
                    harbor_type = soc.harbour_to_resource[board_tile]
        
                self.boardLayout.nodes[cs[0]].harbor = int(harbor_type)
                self.boardLayout.nodes[cs[1]].harbor = int(harbor_type)

                self.debug_print("{0} has harbor {1}".format(hex(cs[0]),harbor_type))
                self.debug_print("{0} has harbor {1}".format(hex(cs[1]),harbor_type))
                
                # store harbour -> tile information
                self.boardLayout.harbour_tiles[soc.hex_grid[num]] = int(harbor_type)
            #print(self.boardLayout.harbour_tiles)

            #set the robber location
            self.boardLayout.robberpos = message.robberpos
                       
        elif id == "PutPieceMessage":
            logging.info("PutPiece (#{0}): Type = {1}, Coords = {2}".format(message.playernum, message.piecetype, hex(message.coords)))
            if message.piecetype == "SETTLEMENT":
                self.vp[message.playernum] += 1
                
                self.boardLayout.nodes[message.coords].owner = message.playernum 
                self.boardLayout.nodes[message.coords].type = 1

                # decrease the number of settlements we have left to build
                if int(message.playernum) == int(self.playernum):
                    self.resources["SETTLEMENTS"] -= 1
                    self.builtnodes.append(message.coords)
                    if 0 < self.boardLayout.nodes[message.coords].harbor < 6:
                        self.harbor_list[self.boardLayout.nodes[message.coords].harbor] = True

                #May not build on built spots
                self.buildableNodes.nodes[message.coords] = False

                #May not build on neighbouring nodes
                if self.boardLayout.nodes[message.coords].n1:
                    road = self.boardLayout.nodes[message.coords].n1
                    id1 = self.boardLayout.roads[road].n1
                    id2 = self.boardLayout.roads[road].n2
                    self.debug_print("Built s at {0}. May not build s on {1} or {2}".format(hex(message.coords),hex(id1),hex(id2)))
                    self.buildableNodes.nodes[id1] = False
                    self.buildableNodes.nodes[id2] = False

                if self.boardLayout.nodes[message.coords].n2:
                    road = self.boardLayout.nodes[message.coords].n2
                    id1 = self.boardLayout.roads[road].n1
                    id2 = self.boardLayout.roads[road].n2
                    self.debug_print("Built s at {0}. May not build s on {1} or {2}".format(hex(message.coords),hex(id1),hex(id2)))
                    self.buildableNodes.nodes[id1] = False
                    self.buildableNodes.nodes[id2] = False

                if self.boardLayout.nodes[message.coords].n3:
                    road = self.boardLayout.nodes[message.coords].n3
                    id1 = self.boardLayout.roads[road].n1
                    id2 = self.boardLayout.roads[road].n2
                    self.debug_print("Built s at {0}. May not build s on {1} or {2}".format(hex(message.coords),hex(id1),hex(id2)))
                    self.buildableNodes.nodes[id1] = False
                    self.buildableNodes.nodes[id2] = False

                #May build on unoccupied adjacent roads
                if int(message.playernum) == int(self.playernum):
                    r1 = self.boardLayout.nodes[message.coords].n1
                    r2 = self.boardLayout.nodes[message.coords].n2
                    r3 = self.boardLayout.nodes[message.coords].n3

                    if r1 and self.boardLayout.roads[r1].owner == None:
                        self.debug_print("Built s at {0}. May build road on {1}".format(hex(message.coords),hex(r1)))
                        self.buildableRoads.roads[r1] = True

                    if r2 and self.boardLayout.roads[r2].owner == None:
                        self.debug_print("Built s at {0}. May build road on {1}".format(hex(message.coords),hex(r2)))
                        self.buildableRoads.roads[r2] = True

                    if r3 and self.boardLayout.roads[r3].owner == None:
                        self.debug_print("Built s at {0}. May build road on {1}".format(hex(message.coords),hex(r3)))
                        self.buildableRoads.roads[r3] = True
       
            elif message.piecetype == "ROAD":
                self.boardLayout.roads[message.coords].owner = message.playernum

                # decrease the number of settlements we have left to build
                if int(message.playernum) == int(self.playernum):
                    self.resources["ROADS"] -= 1

                #May not build on built roads
                self.buildableRoads.roads[message.coords] = False
                #May build on unoccupied roads adjacent to built roads
                
                if int(message.playernum) == int(self.playernum):
                    n1 = self.boardLayout.roads[message.coords].n1
                    n2 = self.boardLayout.roads[message.coords].n2
                    self.builtroads.append(message.coords)

                    r1 = self.boardLayout.nodes[n1].n1
                    r2 = self.boardLayout.nodes[n1].n2
                    r3 = self.boardLayout.nodes[n1].n3

                    if r1 and self.boardLayout.roads[r1].owner == None:
                        self.buildableRoads.roads[r1] = True
                        self.debug_print("Built road at {0}. May build on road {1}".format(hex(message.coords),hex(r1)))

                    if r2 and self.boardLayout.roads[r2].owner == None:
                        self.buildableRoads.roads[r2] = True
                        self.debug_print("Built road at {0}. May build on {1}".format(hex(message.coords),hex(r2)))

                    if r3 and self.boardLayout.roads[r3].owner == None:
                        self.buildableRoads.roads[r3] = True
                        self.debug_print("Built road at {0}. May build on {1}".format(hex(message.coords),hex(r3)))
                        
                    r1 = self.boardLayout.nodes[n2].n1
                    r2 = self.boardLayout.nodes[n2].n2
                    r3 = self.boardLayout.nodes[n2].n3

                    if r1 and self.boardLayout.roads[r1].owner == None:
                        self.buildableRoads.roads[r1] = True
                        self.debug_print("Built road at {0}. May build road on {1}".format(hex(message.coords),hex(r1)))

                    if r2 and self.boardLayout.roads[r2].owner == None:
                        self.buildableRoads.roads[r2] = True
                        self.debug_print("Built road at {0}. May build road on {1}".format(hex(message.coords),hex(r2)))

                    if r3 and self.boardLayout.roads[r3].owner == None:
                        self.buildableRoads.roads[r3] = True
                        self.debug_print("Built road at {0}. May build road on {1}".format(hex(message.coords),hex(r3)))

            elif message.piecetype == "CITY":
                self.vp[message.playernum] += 1
                
                self.boardLayout.nodes[message.coords].type = 2
                
                # increase the number of settlements we have left to build
                # decrease the number of cities we have left to build
                if int(message.playernum) == int(self.playernum):
                    self.resources["SETTLEMENTS"] += 1
                    self.resources["CITIES"] -= 1

        elif id == "PlayerElementMessage" and message.playernum == self.playernum:
            symb = {"SET":"=", "GAIN":"+=", "LOSE":"-="}[message.action]
            logging.info("Resources recieved: {0} {1} {2}".format(message.element, symb, message.value))
            
        
        elif id == "MoveRobberMessage":
            logging.info("Robber moved: player={0}, coords={1}".format(message.playernum, hex(message.coords)))
            self.boardLayout.robberpos = message.coords
            
        elif id == "LastSettlementMessage":
            logging.info("Last settlement: player={0}, coords={1}".format(message.playernum, hex(message.coords)))
            

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
        self.type = None

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
        
        self.harbour_tiles = {0x17: 6, #0x17
                              0x5b: 6, #0x5b
                              0x9d: 6, #0x9d
                              0xdd: 6, #0xdd
                              0xd9: 6, #0xd9
                              0xb5: 6, #0xb5
                              0x71: 6, #0x71
                              0x31: 6, #0x31
                              0x13: 6} #0x13
            
class BuildableNodes:

    def __init__(self):

        import jsettlers_utils as soc
        self.nodes = {}
        for k in soc.nodeLUT:
            self.nodes[k] = True

class BuildableRoads:

    def __init__(self):

        import jsettlers_utils as soc
        self.roads = {}
        for k in soc.roadLUT:
            self.roads[k] = False
