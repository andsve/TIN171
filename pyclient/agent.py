from messages import *
from utils import cprint

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
    def __init__(self, nickname, gamename, game, client):
        self.gamestate = 0 # 0 = not started, 1 = setup (settle placements), 2 = game running
        self.game = game
        self.gamename = gamename
        self.client = client
        self.nickname = nickname
        
        self.output_prefix = "[DEBUG] agent.py ->"
    
    def debug_print(self, msg):
        cprint("{0} {1}".format(self.output_prefix, msg), 'red')
	
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
        #4 = Grain
        #5 = Lumber
        resource_weight = [0,20,15,10,15,20]
        
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
        
        #if self.gamestate == 0:
            #print "Game has not started yet, don't know what to do!"
        if self.gamestate == 1:
            # Setup state
            if (name == "TurnMessage" and message.playernum == self.playernum):
                new_settlement_place = self.find_buildable_node()
                # change the resource_list to see which kind of resources are taken
                node = self.game.boardLayout.nodes[new_settlement_place]
                t1 = self.game.boardLayout.tiles[node.t1]
                t2 = self.game.boardLayout.tiles[node.t2]
                t3 = self.game.boardLayout.tiles[node.t3]
                resource_list[t1.resource]=1
                resource_list[t2.resource]=1
                resource_list[t3.resource]=1
                
                self.debug_print("We should place our settlements now!")
                
                response = PutPieceMessage(self.gamename, self.playernum, 1, new_settlement_place)
                self.client.send_msg(response)
		
					# Always place a road after settlement
					# 
        #else:
            # Game is running!
            #print "LETS PLAY!"
        
        # DEBUG: 
        #if message:
        #    print "Agent: {0} - {1}".format(name, message.values())
		
		
		
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
    
