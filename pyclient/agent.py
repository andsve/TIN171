import logging
from messages import *
from utils import cprint
from planner import *

dice_props = {}
dice_props[0]  = 0.0
dice_props[2]  = 0.0278
dice_props[3]  = 0.0556
dice_props[4]  = 0.0833
dice_props[5]  = 0.1111
dice_props[6]  = 0.1389
dice_props[7]  = 0.1667
dice_props[8]  = 0.1389
dice_props[9]  = 0.1111
dice_props[10] = 0.0833
dice_props[11] = 0.0556
dice_props[12] = 0.0278

resource_list = [0,0,0,0,0,0]#make a list of exist resource

class Agent:
    def __init__(self, nickname, gamename, game, client, resources,nodes,roads):
        self.gamestate = 0 # 0 = not started, 1 = setup (settle placements), 2 = game running
        self.game = game
        self.gamename = gamename
        self.client = client
        self.nickname = nickname
        self.playernum = None

        self.builtnodes = nodes
        self.builtroads = roads

        self.resources = resources

        self.resources["CLAY"] = 0
        self.resources["ORE"] = 0
        self.resources["SHEEP"] = 0
        self.resources["WHEAT"] = 0
        self.resources["WOOD"] = 0
        
        self.output_prefix = "[DEBUG] agent.py ->"
    
    def debug_print(self, msg):
        logging.info(msg)
        #cprint("{0} {1}".format(self.output_prefix, msg), 'red')
	
	#
    # Auxiliary gameboard functions
    #
    
    def calculate_new_settlement_weight(self, node, _round): # add the round number as parameter?
        weight = 0
        if node.t1:
            t1 = self.game.boardLayout.tiles[node.t1]
            weight = weight + self.resource_weight(t1.resource,_round) * dice_props[t1.number]
        if node.t2:
            t2 = self.game.boardLayout.tiles[node.t2]
            weight = weight + self.resource_weight(t2.resource,_round) * dice_props[t2.number]
        if node.t3:
            t3 = self.game.boardLayout.tiles[node.t3]
            weight = weight + self.resource_weight(t3.resource,_round) * dice_props[t3.number]   
        
        
        return weight

    def resource_weight(self, _type, _round):
        #1 = Clay
        #2 = Ore
        #3 = Sheep
        #4 = Wheat
        #5 = Wood
        resource_weight = [0,20,20,20,20,20]
        
        if (_round!=1):
            if (resource_list[_type]==0 and _type!=0):
                return 40 # enhance the importance of the scarce resource
        else:
            resource_list[_type] = 1
            return resource_weight[_type]
        
    
    
    def find_buildable_node(self):
        # Returns the best buildable new node!
        
        # First, get all buildable nodes!
        good_nodes = []
        for (k,n) in self.game.buildableNodes.nodes.items():
            if (n):
                self.debug_print("Trying see if build is possible on {0}".format(hex(k)))
                #self.debug_print("Sure build here man!")
                
                # look up node in gameboard
                node = self.game.boardLayout.nodes[k]
                
                good_nodes.append({'id': k, 'w': self.calculate_new_settlement_weight(node,1)})
                
                # print neighbour roads
                #self.debug_print("It has neighbours: {0}, {1}, {2}".format(node.n1, node.n2, node.n3))
                """
                # get node neighbours
                n1 = None
                if (node.n1 != None):
                    if (self.game.boardLayout.roads[node.n1].n1 == k):
                        n1 = self.game.boardLayout.roads[node.n1].n2
                    elif (self.game.boardLayout.roads[node.n1].n2 == k):
                        n1 = self.game.boardLayout.roads[node.n1].n1
                    
                n2 = None
                if (node.n2 != None):
                    if (self.game.boardLayout.roads[node.n2].n1 == k):
                        n2 = self.game.boardLayout.roads[node.n2].n2
                    elif (self.game.boardLayout.roads[node.n2].n2 == k):
                        n2 = self.game.boardLayout.roads[node.n2].n1
                
                n3 = None
                if (node.n3 != None):
                    if (self.game.boardLayout.roads[node.n3].n1 == k):
                        n1 = self.game.boardLayout.roads[node.n3].n2
                    elif (self.game.boardLayout.roads[node.n3].n2 == k):
                        n1 = self.game.boardLayout.roads[node.n3].n1
                
                # check neighbours of node
                if ((n1 == None or self.game.buildableNodes.nodes[n1]) and 
                    (n2 == None or self.game.buildableNodes.nodes[n2]) and
                    (n3 == None or self.game.buildableNodes.nodes[n3])):
                    self.debug_print("Sure build here man!")
                else:
                    self.debug_print("CANT BUILD HERE MANGE!")
                """
                
        best_id = -1
        best_w = -1
        # find best one good nodes
        for v in good_nodes:
            if (v['w'] > best_w):
                best_w = v['w']
                best_id = v['id']
        
        # return the best one
        return best_id
        
        #print(self.game.buildableNodes)
        
    # incomming messages from the message handler
    #  (i.e. alarms/signals/events from the game the agent needs to act on)
    def handle_message(self, name, message):
        
        if (name == "SitDownMessage" and message.nickname == self.nickname):
            # This is us sitting down, store the playernum!
            self.playernum = message.playernum
            #self.debug_print("I am player number: {0}".format(self.playernum))
        elif (name == "StartGameMessage"):
            self.debug_print("Game has started! Change agent state to 1 (initial placement)")
            self.gamestate = 1
            self.turnMsgs = 0

        #if self.gamestate == 0:
            #print "Game has not started yet, don't know what to do!"

        # count the number of TurnMessages to know if we're the last to play
        elif self.gamestate == 1 and name == "TurnMessage":
            self.turnMsgs += 1

        # add / remove to resource list
        elif name == "PlayerElementMessage" and int(message.playernum) == int(self.playernum):
            
            if message.action == "SET":
                self.resources[message.element] = int(message.value)

            elif message.action == "GAIN":
                self.resources[message.element] += int(message.value)

            elif message.action == "LOSE":
                self.resources[message.element] -= int(message.value)
        
        if name == "ResourceCountMessage":
            items = self.resources.items()
            self.debug_print("Have resources: {0} = {1}".format(items[0][0], items[0][1]))
            for res, val in items[1:]:
                if res != "UNKNOWN":
                    self.debug_print("                {0} = {1}".format(res, val))
        
        # Setup state 1    
        if self.gamestate == 1 and name == "TurnMessage" and message.playernum == self.playernum:
            new_settlement_place = self.find_buildable_node()
            # change the resource_list to see which kind of resources are taken
            node = self.game.boardLayout.nodes[new_settlement_place]
            if node.t1:
                t1 = self.game.boardLayout.tiles[node.t1]
                resource_list[t1.resource]=1
            if node.t2:
                t2 = self.game.boardLayout.tiles[node.t2]
                resource_list[t2.resource]=1
            if node.t3:
                t3 = self.game.boardLayout.tiles[node.t3]
                resource_list[t3.resource]=1  
                
            self.debug_print("We should place our settlements now!")
                
            response = PutPieceMessage(self.gamename, self.playernum, 1, new_settlement_place)
            self.client.send_msg(response)

        # Confirm PutPiece
        elif self.gamestate == 1 and name == "PutPieceMessage" and int(message.playernum) == int(self.playernum):
            self.gamestate = 2
            
            
        # Setup state 2    
        elif self.gamestate == 2 and name == "GameStateMessage" and int(message.state) == 6:
    
            #arbitarly build a first road
	    for r in self.game.buildableRoads.roads:
                if self.game.buildableRoads.roads[r]:
                    response = PutPieceMessage(self.gamename, self.playernum, 0, r)
                    self.client.send_msg(response)
                    break

        # Confirm PutPiece
        elif self.gamestate == 2 and name == "PutPieceMessage" and int(message.playernum) == int(self.playernum):
            self.gamestate = 3

            # If we were the last one to play, we won't get a TurnMessage, goto state 4
            if self.turnMsgs == 4:
                self.gamestate = 4

        #Setup state 3 or 4
        #(state 3 normally. state 4 if we were the last to play and it's our turn again)
        elif (self.gamestate == 3 and name == "TurnMessage" and int(message.playernum) == int(self.playernum)) or (self.gamestate == 4 and name == "GameStateMessage" and int(message.state) == 10):
	    new_settlement_place = self.find_buildable_node()
            # change the resource_list to see which kind of resources are taken
            node = self.game.boardLayout.nodes[new_settlement_place]
            if node.t1:
                t1 = self.game.boardLayout.tiles[node.t1]
                resource_list[t1.resource]=1
            if node.t2:
                t2 = self.game.boardLayout.tiles[node.t2]
                resource_list[t2.resource]=1
            if node.t3:
                t3 = self.game.boardLayout.tiles[node.t3]
                resource_list[t3.resource]=1          
                
            self.debug_print("We should place our settlements now!")
                
            response = PutPieceMessage(self.gamename, self.playernum, 1, new_settlement_place)
            self.client.send_msg(response)

            #we're done here, set state to 4
            self.gamestate = 4

        # Confirm PutPiece
        elif self.gamestate == 4 and name == "PutPieceMessage" and int(message.playernum) == int(self.playernum):
            self.gamestate = 5

        # Setup state 5    
        elif self.gamestate == 5 and name == "GameStateMessage" and int(message.state) == 11:          
        
            #arbitarly build a second road
            #must be connected to second settlement
	    for r in self.game.buildableRoads.roads:
                if self.game.buildableRoads.roads[r] and (self.game.boardLayout.roads[r].n1 == self.builtnodes[1] or self.game.boardLayout.roads[r].n2 == self.builtnodes[1]):
                    response = PutPieceMessage(self.gamename, self.playernum, 0, r)
                    self.client.send_msg(response)
                    break

        # Confirm PutPiece
        elif self.gamestate == 5 and name == "PutPieceMessage" and int(message.playernum) == int(self.playernum):
            self.gamestate = 6

            # We were not first to play, we must wait for a TurnMessage before requested to roll the dices
            if self.turnMsgs != 1:
                self.gamestate = 7
                    
        # State 6 or 7 (not rolled dices yet, might be forced to throw away cards or handle trades)
        elif (self.gamestate == 7 and name == "TurnMessage" and int(message.playernum) == int(self.playernum)) or (self.gamestate == 6 and name == "GameStateMessage" and int(message.state) == 15):

            # Roll Dices
            response = RollDiceMessage(self.gamename)
            self.client.send_msg(response)

            self.gamestate = 8
            
        elif self.gamestate == 7 and name == "DiscardRequestMessage":
            
            # Throw away cards here (message.numcards)
            numcards = int(message.numcards)
           
            ore = min(self.resources["ORE"], numcards)           
            clay = min(max(self.resources["CLAY"] - 1,0), numcards - ore)
            sheep = min(max(self.resources["SHEEP"] - 1,0), numcards - clay - ore)
            wheat = min(max(self.resources["WHEAT"] - 1,0), numcards - clay - ore - sheep)
            wood = min(max(self.resources["WOOD"] - 1,0), numcards - clay - ore - sheep - wheat)
            response = DiscardMessage(self.gamename, clay, ore, sheep, wheat, wood, 0)

            self.client.send_msg(response)
        
        elif self.gamestate == 7 and name == "MakeOfferMessage":

            # Handle Offers
            # Reject offer
            response = RejectOfferMessage(self.gamename, self.playernum)
            self.client.send_msg(response)

        # State 8 (dices have been rolled, might be forced to throw away cards, move the robber, choose player to steal from. otherwise play normally.
        elif self.gamestate == 8 and name == "DiscardRequestMessage":
            # Throw away cards here (message.numcards)

            numcards = int(message.numcards)

            ore = min(self.resources["ORE"], numcards)           
            clay = min(max(self.resources["CLAY"] - 1,0), numcards - ore)
            sheep = min(max(self.resources["SHEEP"] - 1,0), numcards - clay - ore)
            wheat = min(max(self.resources["WHEAT"] - 1,0), numcards - clay - ore - sheep)
            wood = min(max(self.resources["WOOD"] - 1,0), numcards - clay - ore - sheep - wheat)
            response = DiscardMessage(self.gamename, clay, ore, sheep, wheat, wood, 0)

            self.client.send_msg(response)
            
        # We need to move the robber, lets find a good spot!
        elif self.gamestate == 8 and name == "GameStateMessage" and int(message.state) == 33:
            
            # List to store possible tiles in
            possible_tiles = []
            
            # Iterate over all tiles
            for k,v in self.game.boardLayout.tiles.items():
                
                robber_scale = 0
                tile_number = v.number
                tile_resource = v.resource
                
                # We can't move it to the same tile again
                if (self.game.boardLayout.robberpos == int(k)):
                    continue
                
                # Store all nodes around this tile for future refernce
                n1 = self.game.boardLayout.nodes[v.n1]
                n2 = self.game.boardLayout.nodes[v.n2]
                n3 = self.game.boardLayout.nodes[v.n3]
                n4 = self.game.boardLayout.nodes[v.n4]
                n5 = self.game.boardLayout.nodes[v.n5]
                n6 = self.game.boardLayout.nodes[v.n6]
                
                # Check so we dont try to block ourselves!
                if (n1.owner != None and int(n1.owner) == int(self.playernum)):
                    continue
                if (n2.owner != None and int(n2.owner) == int(self.playernum)):
                    continue
                if (n3.owner != None and int(n3.owner) == int(self.playernum)):
                    continue
                if (n4.owner != None and int(n4.owner) == int(self.playernum)):
                    continue
                if (n5.owner != None and int(n5.owner) == int(self.playernum)):
                    continue
                if (n6.owner != None and int(n6.owner) == int(self.playernum)):
                    continue
                
                # We havn't built around this node, yay!
                # The more settlements around the tile, the better to place here
                num_settlements = 0.0
                if (n1.owner != None):
                    num_settlements += 1.0 * n1.type
                if (n2.owner != None):
                    num_settlements += 1.0 * n2.type
                if (n3.owner != None):
                    num_settlements += 1.0 * n3.type
                if (n4.owner != None):
                    num_settlements += 1.0 * n4.type
                if (n5.owner != None):
                    num_settlements += 1.0 * n5.type
                if (n6.owner != None):
                    num_settlements += 1.0 * n6.type
                
                robber_scale = num_settlements / 6.0 # (Maximum number of settlements around a tile is 3!)
                
                # Append to possible tiles
                possible_tiles.append({'id': k, 'scale': robber_scale})
            
            # Loop possible_tiles and find best one
            best_tile_id = -1
            best_tile_scale = -1
            
            self.debug_print("Possible tiles to move robber to:")
            for tile in possible_tiles:
                self.debug_print("       id: {0}, scale: {1}".format(hex(tile['id']), tile['scale']))
                if (tile['scale'] > best_tile_scale):
                    best_tile_scale = tile['scale']
                    best_tile_id = tile['id']
            self.debug_print("       ---")
            self.debug_print("       id: {0}, scale: {1} Seemed best!".format(hex(best_tile_id), best_tile_scale))
            
            # Now move robber to the best spot!
            response = MoveRobberMessage(self.gamename, self.playernum, best_tile_id)
            self.client.send_msg(response)

        elif self.gamestate == 8 and name == "ChoosePlayerRequestMessage":

            # Choose a player to steal from
            # TODO: Dont do this randomly
            i = 0
            self.debug_print("Steal list: {0}".format(message.choices))
            for c in message.choices:
                if c == 'true':
                    response = ChoosePlayerMessage(self.gamename, i)
                    self.client.send_msg(response)
                    break
                else:
                    i += 1

        elif self.gamestate == 8 and name == "GameStateMessage" and int(message.state) == 20:

            # Play normally
            # TODO: Do something!
            self.make_play()

    # the default playing method
    # TODO: Intelligent stuff
    def make_play(self):

        temp = Planner(self.game,self.gamename,self.resources,self.builtnodes,self.builtroads,self.client)
        plan = temp.make_plan()

        if plan:
            (build_spot, build_type) = plan

            #DEBUGGING                
            response = BuildRequestMessage(self.gamename,build_type)
            self.client.send_msg(response)

            response = PutPieceMessage(self.gamename,self.playernum,build_type,build_spot)
            self.client.send_msg(response)

        else:        
        
            response = EndTurnMessage(self.gamename)
            self.client.send_msg(response)
            self.gamestate = 7
		
    def can_build_at_node(self, node):
        # Returns 1 if it is possible to build a settlement at
        # this node, 0 otherwize.
        #print("HEY NOW: ")
        #print(self.game.boardLayout)
        return True
    
    
    def resources_at_node(self, node):
        # Returns a list of resources for the specific node.
        pass
    
    
    def harbour_at_node(self, node):
        # Returns the type of harbour at the specific node,
        # returns 0 if the node isn't a harbour node.
        pass
    
