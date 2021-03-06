import logging
import random
from messages import *
from utils import cprint
from planner import *
from jsettlers_utils import pieceToType
from jsettlers_utils import elementIdToType

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

resource_weight = [0,55,25,35,35,45]
total_highest = 0

best_resource = [""]

class Agent:
    def __init__(self, nickname, stats, gamename, game, client, resources,nodes,roads,harbor_list):
        self.gamestate = 0 # 0 = not started, 1 = setup (settle placements), 2 = game running
        self.game = game
        self.stats = stats
        self.gamename = gamename
        self.client = client
        self.nickname = nickname
        self.playernum = -1

        self.builtnodes = nodes
        self.builtroads = roads

        self.resources = resources

        self.resources["CLAY"] = 0
        self.resources["ORE"] = 0
        self.resources["SHEEP"] = 0
        self.resources["WHEAT"] = 0
        self.resources["WOOD"] = 0
        self.resources["DEV_CARDS"] = 25
        self.resources["NUMKNIGHTS"] = 0
        self.resources["KNIGHT_CARDS"] = 0
        self.resources["VICTORY_CARDS"] = 0
        self.resources["MONOPOLY_CARDS"] = 0
        self.resources["ROAD_CARDS"] = 0
        self.resources["RESOURCE_CARDS"] = 0
        self.resources["MAY_PLAY_DEVCARD"] = False

        self.bought = {}
        self.bought["roadcard"] = False
        self.bought["resourcecard"] = False
        self.bought["monopolycard"] = False

        self.harbor_list = harbor_list

        self.strategy = None
        #self.strategy = "BEST_PROBS"
        #self.strategy = "RANDOM"

        self.stats["START_HARBORS"] = [False,False,False,False,False,False,False]

        self.played_knight = False
        self.debug_print("self.played_knight = True (1)")
        self.rob_several = False
        self.debug_print("self.rob_several = False (1)")
        
        self.planner = Planner(self.game, self.stats, self.gamename,self.resources,self.builtnodes,self.builtroads,self.client,self.bought,self.harbor_list)
        
        self.output_prefix = "[DEBUG] agent.py ->"
    
    def debug_print(self, msg):
        logging.info(msg)
        #cprint("{0} {1}".format(self.output_prefix, msg), 'red')
    
    #
    # Auxiliary gameboard functions
    #
    def get_settlement_stats(self, pos):
        tiles = (self.game.boardLayout.nodes[pos].t1
                ,self.game.boardLayout.nodes[pos].t2
                ,self.game.boardLayout.nodes[pos].t3)
        info = []
        for tile in tiles:
            if tile != None:
                resource_num = str(self.game.boardLayout.tiles[tile].resource)
                if resource_num in elementIdToType:
                    resource = elementIdToType[resource_num]
                    num = self.game.boardLayout.tiles[tile].number
                    if num in dice_props:
                        #probability = dice_props[num]
                        info.append((resource, num))
                    else:
                        #probability = "?????????????????"
                        info.append((resource, "???"))
                    #info.append((resource, probability))
        return info

    def total_resources(self):
        return self.resources["CLAY"] + self.resources["ORE"] + self.resources["SHEEP"] + self.resources["WHEAT"] + self.resources["WOOD"]
        
    def calculate_new_settlement_weight(self, node): # add the round number as parameter?
        weight = 0
        w1=0
        w2=0
        w3=0
        r1=0
        r2=0
        r3=0
        if node.t1:
            t1 = self.game.boardLayout.tiles[node.t1]
            r1 = t1.resource
            w1 = self.resource_weight(r1) * dice_props[t1.number]
            self.debug_print("The original weight on tile1 is {0}, tile number is {1}, type is {2}".format(w1,t1.number,t1.resource))

        if node.t2:
            t2 = self.game.boardLayout.tiles[node.t2]
            r2 = t2.resource
            w2 = self.resource_weight(r2) * dice_props[t2.number]
            self.debug_print("The original weight on tile2 is {0}, tile number is {1}, type is {2}".format(w2,t2.number,t2.resource))
            if (r2 == r1):
                if(w2>w1):
                    w1 = w1*0.7
                else:
                    w2 = w2*0.7
                
        if node.t3:
            t3 = self.game.boardLayout.tiles[node.t3]
            r3 = t3.resource
            w3 = self.resource_weight(r3) * dice_props[t3.number]
            self.debug_print("The original weight on tile3 is {0}, tile number is {1}, type is {2}".format(w3,t3.number,t3.resource))
            if (r3 == r1):
                if(w3>w1):
                    w1 = w1*0.7
                else:
                    w3 = w3*0.7
            elif (r3 == r2):
                if(w3>w2):
                    w2 = w2*0.7
                else:
                    w3 = w3*0.7

        weight = w1+w2+w3
        # if it is the first settlement than force the robot to take three kinds of resource
        rl=0
        for i in resource_list:
            rl= rl+i
        if (rl==0):
            if(r1!=0 and r2!=0 and r3!=0):
                if(r1!=r2 and r2!=r3):
                    if(t1.resource!=t3.resource):
                        weight = weight + 5
        if (rl!=0):
            if(r1!=0 and r2!=0 and r3!=0):
                if(resource_list[r1]+resource_list[r2]+resource_list[r3] <= 1):
                    weight = weight + 2
                    if(r1!=r2 or r1!=r3 or r2!=r3):
                        weight = weight +2

        return weight

    def resource_weight(self, _type):
        #1 = Clay
        #2 = Ore
        #3 = Sheep
        #4 = Wheat
        #5 = Wood
        resource_weight = [0,30,15,25,25,30]
        return resource_weight[_type]

    def find_best_resource_spot(self, b_resource):
        # Traverse map, if the node belongs to the best resource, then calculate the weight.
        # The harbor has really high priority.
        best_spot = None
        best_weight = 0
        for b_r in b_resource:
            node_score = {}
            for n in self.game.buildableNodes.nodes:
                if self.game.buildableNodes.nodes[n]:
                    tempScore = 0
                    t1 = self.game.boardLayout.nodes[n].t1
                    t2 = self.game.boardLayout.nodes[n].t2
                    t3 = self.game.boardLayout.nodes[n].t3
                    for t in [t1,t2,t3]:
                        if t and self.game.boardLayout.tiles[t].resource != 0:
                            if elementIdToType[str(self.game.boardLayout.tiles[t].resource)] == b_r:
                                tempScore += dice_props[self.game.boardLayout.tiles[t].number] * 50 # really high weight for this kinda resource
                            else:
                                tempScore += 0.5 * dice_props[self.game.boardLayout.tiles[t].number] * resource_weight[self.game.boardLayout.tiles[t].resource]
                    node_score[n] = tempScore
            #Find the best node
            bestNode = None
            highest = 0
            for n in node_score:
                self.debug_print("Node {0} has {1} score.".format(hex(n),node_score[n]))
                if node_score[n] > highest:
                    highest = node_score[n]
                    bestNode = n
            if highest > best_weight:
                best_weight = highest
                best_spot = bestNode
                best_resource[0] = b_r
        return best_spot
    
    def find_best_resource_harbor(self, b_r):
    #depends on the best resource, find the specific harbor, otherwise, chase for a 3:1 harbor
        node_score = {}
        foundHarbor = False
        for n in self.game.buildableNodes.nodes:
            if self.game.buildableNodes.nodes[n]:
                tempScore = 0
                self.debug_print("The type of the harbor is {0}".format(self.game.boardLayout.nodes[n].harbor))
                if 0 < self.game.boardLayout.nodes[n].harbor < 6:
                    self.debug_print("Find resource harbor: {0}".format(elementIdToType[str(self.game.boardLayout.nodes[n].harbor)]))
                    if elementIdToType[str(self.game.boardLayout.nodes[n].harbor)]== b_r:
                        tempScore += 10
                        foundHarbor = True
               # elif self.game.boardLayout.nodes[n].harbor == 6:
               #     tempScore += 5 #take the 3:1 harbor
                t1 = self.game.boardLayout.nodes[n].t1
                t2 = self.game.boardLayout.nodes[n].t2
                t3 = self.game.boardLayout.nodes[n].t3
                for t in [t1,t2,t3]:
                    if t and self.game.boardLayout.tiles[t].resource != 0:
                        tempScore += 0.2 * dice_props[self.game.boardLayout.tiles[t].number] * resource_weight[self.game.boardLayout.tiles[t].resource]
                node_score[n] = tempScore
        #Find the best node
        #if foundHarbor:
        bestNode = None
        highest = 0
        for n in node_score:
            self.debug_print("Node {0} has {1} score.".format(hex(n),node_score[n]))
            if node_score[n] > highest:
                highest = node_score[n]
                bestNode = n
        return bestNode

        #return self.find_second_settlement()

    def find_first_settlement(self):

        node_score = {}

        rares = {}
        rares["CLAY"] = []
        rares["ORE"] = []
        rares["SHEEP"] = []
        rares["WHEAT"] = []
        rares["WOOD"] = []

        resource_matrix = []
        resource_matrix.append([[],[],[],[],[],[]])
        resource_matrix.append([[],[],[],[],[],[]])
        resource_matrix.append([[],[],[],[],[],[]])
        resource_matrix.append([[],[],[],[],[],[]])
        resource_matrix.append([[],[],[],[],[],[]])
        resource_matrix.append([[],[],[],[],[],[]])

        for n in self.game.buildableNodes.nodes:

            if self.game.buildableNodes.nodes[n]:

                tempScore = 0
                tempList = [0,0,0,0,0,0]

                t1 = self.game.boardLayout.nodes[n].t1
                t2 = self.game.boardLayout.nodes[n].t2
                t3 = self.game.boardLayout.nodes[n].t3

                if t1:
                    if t2 and self.game.boardLayout.tiles[t2].resource != 0:
                        if self.game.boardLayout.tiles[t1].resource != 0 and self.game.boardLayout.tiles[t1].resource != self.game.boardLayout.tiles[t2].resource:
                            resource_matrix[self.game.boardLayout.tiles[t1].resource][self.game.boardLayout.tiles[t2].resource].append(n)
                            resource_matrix[self.game.boardLayout.tiles[t2].resource][self.game.boardLayout.tiles[t1].resource].append(n)
                        if t3 and self.game.boardLayout.tiles[t3].resource != 0 and self.game.boardLayout.tiles[t2].resource != self.game.boardLayout.tiles[t3].resource:
                            resource_matrix[self.game.boardLayout.tiles[t3].resource][self.game.boardLayout.tiles[t2].resource].append(n)
                            resource_matrix[self.game.boardLayout.tiles[t2].resource][self.game.boardLayout.tiles[t3].resource].append(n)
                    if t3 and self.game.boardLayout.tiles[t3].resource != 0 and self.game.boardLayout.tiles[t1].resource != 0 and self.game.boardLayout.tiles[t1].resource != self.game.boardLayout.tiles[t3].resource:
                        resource_matrix[self.game.boardLayout.tiles[t3].resource][self.game.boardLayout.tiles[t1].resource].append(n)
                        resource_matrix[self.game.boardLayout.tiles[t1].resource][self.game.boardLayout.tiles[t3].resource].append(n)
                    
                if t1 and t2 and t3 and self.game.boardLayout.tiles[t1].resource != 0 and self.game.boardLayout.tiles[t2].resource != 0 and self.game.boardLayout.tiles[t3].resource != 0:
                    for t in [t1,t2,t3]:
                        if n not in rares[elementIdToType[str(self.game.boardLayout.tiles[t].resource)]] and dice_props[self.game.boardLayout.tiles[t].number] > 0.06:
                            rares[elementIdToType[str(self.game.boardLayout.tiles[t].resource)]].append(n)

                for t in [t1,t2,t3]:

                    if t and self.game.boardLayout.tiles[t].resource != 0 and dice_props[self.game.boardLayout.tiles[t].number] > 0.03:
                        tempScore += dice_props[self.game.boardLayout.tiles[t].number] * resource_weight[self.game.boardLayout.tiles[t].resource]
                        tempList[self.game.boardLayout.tiles[t].resource] = 1

                node_score[n] = tempScore * (tempList[1] + tempList[2] + tempList[3] + tempList[4] + tempList[5])

        for i in resource_matrix:
            self.debug_print(i)
            
        for (r,l) in rares.items():
            self.debug_print("Rares: {0} = {1}".format(r,l))
            length = len(l) / 1.0
            for n in l:
                node_score[n] += 5.0 / length

        for i in resource_matrix:
            for j in i:
                if len(j) > 0:
                    length = len(j) / 1.0
                    for n in j:
                        node_score[n] += 10.0 / length
                

        bestNode = None
        highest = 0

        for n in node_score:
            self.debug_print("Node {0} has {1} score.".format(hex(n),node_score[n]))
            if node_score[n] > highest:
                highest = node_score[n]
                bestNode = n

        return bestNode

    def find_second_settlement(self):

        node_score = {}

        for n in self.game.buildableNodes.nodes:

            if self.game.buildableNodes.nodes[n]:

                tempScore = 0
                tempList = [0,0,0,0,0,0]

                t1 = self.game.boardLayout.nodes[n].t1
                t2 = self.game.boardLayout.nodes[n].t2
                t3 = self.game.boardLayout.nodes[n].t3

                for t in [t1,t2,t3]:

                    if t and self.game.boardLayout.tiles[t].resource != 0 and dice_props[self.game.boardLayout.tiles[t].number] > 0.03:
                        tempScore += dice_props[self.game.boardLayout.tiles[t].number] * resource_weight[self.game.boardLayout.tiles[t].resource] + ((1 - max(tempList[self.game.boardLayout.tiles[t].resource],resource_list[self.game.boardLayout.tiles[t].resource])) * 20)
                        tempList[self.game.boardLayout.tiles[t].resource] = 1

                # this second spot allows us to get resources for settlement
                if resource_list[1] + tempList[1] >= 1 and resource_list[3] + tempList[3] >= 1 and resource_list[4] + tempList[4] >= 1 and resource_list[5] + tempList[5] >= 1:
                    tempScore *= 4
                
                # this second spot allows us to get resources for city
                if resource_list[2] + resource_list[4] < 2 and resource_list[2] + tempList[2] >= 1 and resource_list[4] + tempList[4] >= 1:
                    tempScore *= 5

                node_score[n] = tempScore * (tempList[1] + tempList[2] + tempList[3] + tempList[4] + tempList[5])
                #node_score[n] = tempScore

        bestNode = None
        highest = 0

        for n in node_score:
            self.debug_print("Node {0} has {1} score.".format(hex(n),node_score[n]))
            if node_score[n] > highest:
                highest = node_score[n]
                bestNode = n
                
        return bestNode

    def random_settlement(self):

        good_nodes = []

        for n in self.game.buildableNodes.nodes:

            if self.game.buildableNodes.nodes[n]:

                t1 = 0
                t2 = 0
                t3 = 0

                if self.game.boardLayout.nodes[n].t1 and self.game.boardLayout.tiles[self.game.boardLayout.nodes[n].t1].resource != 0:
                    t1 = 1
                if self.game.boardLayout.nodes[n].t2 and self.game.boardLayout.tiles[self.game.boardLayout.nodes[n].t2].resource != 0:
                    t2 = 1
                if self.game.boardLayout.nodes[n].t3 and self.game.boardLayout.tiles[self.game.boardLayout.nodes[n].t3].resource != 0:
                    t3 = 1

                # only consider nodes with 2 or 3 adjacent tiles
                if t1 + t2 + t3 >= 2:
                    good_nodes.append(n)

        return random.choice(good_nodes)

    def best_probabilites_settlement(self):

        node_score = {}

        for n in self.game.buildableNodes.nodes:

            if self.game.buildableNodes.nodes[n]:

                t1 = self.game.boardLayout.nodes[n].t1
                t2 = self.game.boardLayout.nodes[n].t2
                t3 = self.game.boardLayout.nodes[n].t3

                tempScore = 0

                for t in [t1,t2,t3]:

                    if t and self.game.boardLayout.tiles[t].resource != 0:
                        tempScore += dice_props[self.game.boardLayout.tiles[t].number]

                node_score[n] = tempScore


        bestNode = None
        highest = 0

        for n in node_score:
            if node_score[n] > highest:
                highest = node_score[n]
                bestNode = n
                
        return bestNode

    def find_buildable_node(self):
        # Returns the best buildable new node!
        
        # First, get all buildable nodes!
        good_nodes = []
        for (k,n) in self.game.buildableNodes.nodes.items():
            if (n):
                #self.debug_print("Trying see if build is possible on {0}".format(hex(k)))
                #self.debug_print("Sure build here man!")
                
                # look up node in gameboard
                node = self.game.boardLayout.nodes[k]
                sw = self.calculate_new_settlement_weight(node)
                good_nodes.append({'id': k, 'w': sw})
                self.debug_print("The total weight on this point is {0}".format(sw))
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
        
                    
            # Update resource information
            if message.action in ("GAIN", "LOSE"):
                key = "TOTAL_" + message.element
                if not key in self.stats:
                    self.stats[key] = int(message.value)
                else:
                    self.stats[key] += int(message.value)
                
        if name == "ResourceCountMessage":
            pass
            #items = self.resources.items()
            #self.debug_print("Have resources: {0} = {1}".format(items[0][0], items[0][1]))
            #for res, val in items[1:]:
            #    if res != "UNKNOWN":
            #        self.debug_print("                {0} = {1}".format(res, val))

        # updates the number of devcards left
        if name == "DevCardCountMessage":
            self.resources["DEV_CARDS"] = message.count

        if name == "DevCardMessage":
            # we gain a devcard
            if int(message.playernum) == int(self.playernum) and int(message.action) == 0:

                if int(message.cardtype) == 0:
                    self.resources["KNIGHT_CARDS"] += 1

                elif int(message.cardtype) == 1:
                    self.resources["ROAD_CARDS"] += 1
                    self.bought["roadcard"] = True

                elif int(message.cardtype) == 2:
                    self.resources["RESOURCE_CARDS"] += 1
                    self.bought["resourcecard"] = True

                elif int(message.cardtype) == 3:
                    self.resources["MONOPOLY_CARDS"] += 1
                    self.bought["monopolycard"] = True

                elif int(message.cardtype) >= 4 and int(message.cardtype) <= 8:
                    self.resources["VICTORY_CARDS"] += 1

            # we used a devcard
            elif int(message.playernum) == int(self.playernum) and int(message.action) == 1:

                if int(message.cardtype) == 0:
                    self.resources["KNIGHT_CARDS"] -= 1

                elif int(message.cardtype) == 1:
                    self.resources["ROAD_CARDS"] -= 1

                elif int(message.cardtype) == 2:
                    self.resources["RESOURCE_CARDS"] -= 1

                elif int(message.cardtype) == 3:
                    self.resources["MONOPOLY_CARDS"] -= 1

        if name == "SetPlayedDevCardMessage" and int(message.playernum) == int(self.playernum):
            self.resources["MAY_PLAY_DEVCARD"] = not message.cardflag
                    
        # Setup state 1    
        if self.gamestate == 1 and name == "TurnMessage" and message.playernum == self.playernum:

            # analysis of game board
            probs = {}
            probs["CLAY"] = 0
            probs["ORE"] = 0
            probs["SHEEP"] = 0
            probs["WHEAT"] = 0
            probs["WOOD"]= 0

            tile_list = []

            for n in self.game.buildableNodes.nodes:
                for t in [self.game.boardLayout.nodes[n].t1,self.game.boardLayout.nodes[n].t2,self.game.boardLayout.nodes[n].t3]:
                    if t and t not in tile_list:
                        tile_list.append(t)
                
            for t in tile_list:
                if self.game.boardLayout.tiles[t].resource != 0:    
                    probs[elementIdToType[str(self.game.boardLayout.tiles[t].resource)]] += dice_props[self.game.boardLayout.tiles[t].number]

            self.debug_print("Resources have probabilities:")
            psum = 0
            for (r,v) in probs.items():
                #if r == "CLAY" or r == "ORE":
                    #probs[r] = v/3 * 4
                    #v = v/3 * 4
                psum += v
                self.debug_print("                             {0} = {1}".format(r,v))
                
            self.debug_print("The sum of probability of all tiles is {0}".format(psum))

            rgood = []
            rbad = []
            # Find the worst resource
            # If the worst one exists, then drop it, try to get it through trading            
            for (r,v) in probs.items():
                if(v < 0.2):
                    self.debug_print("The worst resource is {0}, the probability is {1}".format(r,v))
                    rbad.append(r)
            
            # Find the best resource
            # If the best one exists, then chase for it, and also the harbor.
            for (r,v) in probs.items():
                if(v > 0.3):
                    self.debug_print("The best resource is {0}, the probability is {1}".format(r,v))
                    rgood.append(r)

            if self.strategy == "RANDOM":
                new_settlement_place = self.random_settlement()

            elif self.strategy == "BEST_PROBS":
                new_settlement_place = self.best_probabilites_settlement()
                #self.strategy == "STRAT2"
            
            elif len(rbad) > 0 and len(rgood) > 0:
                    self.debug_print("Use the function of Best resource spot!")
                    new_settlement_place = self.find_best_resource_spot(rgood)
                    self.strategy = "STRAT1"
            else:            
                new_settlement_place = self.find_first_settlement() #new function
                self.strategy = "STRAT2"
            
            self.stats["FIRST_SETTLEMENT"] = hex(new_settlement_place)
            self.stats["FIRST_SETTLEMENT_RES"] = self.get_settlement_stats(new_settlement_place)
            if self.game.boardLayout.nodes[new_settlement_place].harbor > 0:
                self.stats["START_HARBORS"][int(self.game.boardLayout.nodes[new_settlement_place].harbor)] = True
            
            
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
                    n1 = self.game.boardLayout.roads[r].n1
                    n2 = self.game.boardLayout.roads[r].n2
                    if self.game.boardLayout.nodes[n1].owner == None:
                        n = n1
                    else:
                        n = n2

                    t1 = 0
                    t2 = 0
                    t3 = 0
                    if self.game.boardLayout.nodes[n].t1:
                        t1 = 1
                    if self.game.boardLayout.nodes[n].t2:
                        t2 = 1
                    if self.game.boardLayout.nodes[n].t3:
                        t3 = 1
                    #avoid build road stupidly
                    if t1 + t2 + t3 >= 2:
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
            """new_settlement_place = self.find_buildable_node()"""
            # If we use the best_resource function, than for the second settlement
            self.debug_print("Best resource is {0}".format(best_resource[0]))
            if self.strategy == "RANDOM":
                new_settlement_place = self.random_settlement()
            elif self.strategy == "BEST_PROBS":
                new_settlement_place = self.best_probabilites_settlement()
            elif self.strategy == "STRAT1":
                self.debug_print("Find the harbor")
                new_settlement_place = self.find_best_resource_harbor(best_resource[0])
            else:
                new_settlement_place = self.find_second_settlement() #new function
                
            self.stats["SECOND_SETTLEMENT"] = hex(new_settlement_place)
            self.stats["SECOND_SETTLEMENT_RES"] = self.get_settlement_stats(new_settlement_place)
                                                  
                
            # change the resource_list to see which kind of resources are taken
            """node = self.game.boardLayout.nodes[new_settlement_place]
            if node.t1:
                t1 = self.game.boardLayout.tiles[node.t1]
                resource_list[t1.resource]=1
            if node.t2:
                t2 = self.game.boardLayout.tiles[node.t2]
                resource_list[t2.resource]=1
            if node.t3:
                t3 = self.game.boardLayout.tiles[node.t3]
                resource_list[t3.resource]=1"""
                
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
                    n1 = self.game.boardLayout.roads[r].n1
                    n2 = self.game.boardLayout.roads[r].n2
                    if self.game.boardLayout.nodes[n1].owner == None:
                        n = n1
                    else:
                        n = n2

                    t1 = 0
                    t2 = 0
                    t3 = 0
                    if self.game.boardLayout.nodes[n].t1:
                        t1 = 1
                    if self.game.boardLayout.nodes[n].t2:
                        t2 = 1
                    if self.game.boardLayout.nodes[n].t3:
                        t3 = 1
                    #avoid build road stupidly
                    if t1 + t2 + t3 >= 2:
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

            # Play a knight card
            n1 = self.game.boardLayout.tiles[self.game.boardLayout.robberpos].n1
            n2 = self.game.boardLayout.tiles[self.game.boardLayout.robberpos].n2
            n3 = self.game.boardLayout.tiles[self.game.boardLayout.robberpos].n3
            n4 = self.game.boardLayout.tiles[self.game.boardLayout.robberpos].n4
            n5 = self.game.boardLayout.tiles[self.game.boardLayout.robberpos].n5
            n6 = self.game.boardLayout.tiles[self.game.boardLayout.robberpos].n6
            owners = [self.game.boardLayout.nodes[n1].owner,self.game.boardLayout.nodes[n2].owner,self.game.boardLayout.nodes[n3].owner,self.game.boardLayout.nodes[n4].owner,self.game.boardLayout.nodes[n5].owner,self.game.boardLayout.nodes[n6].owner]

            if self.resources["MAY_PLAY_DEVCARD"] and ((self.resources["KNIGHT_CARDS"] > 0 and (int(self.playernum) in owners or self.resources["NUMKNIGHTS"] == 2)) or self.resources["KNIGHT_CARDS"] > 1):
                self.debug_print("May play devcard: {0} (3)".format(self.resources["MAY_PLAY_DEVCARD"]))
                response = PlayDevCardRequestMessage(self.gamename, 0)
                self.client.send_msg(response)
                self.resources["MAY_PLAY_DEVCARD"] = False
                self.played_knight = True
                self.debug_print("self.played_knight = True (2)")
            else:            
                # Roll Dices
                self.roll_dices()

                self.gamestate = 8

        elif self.gamestate == 7 and self.played_knight and name == "GameStateMessage" and int(message.state) == 15:

            # Roll Dices
            self.roll_dices()

            self.played_knight = False
            self.gamestate = 8
            
        elif self.gamestate == 7 and name == "DiscardRequestMessage":

            # Throw away cards here (message.numcards)
            self.discard_cards(int(message.numcards))
        
        elif self.gamestate == 7 and name == "MakeOfferMessage":

            # Handle Offers
            # Reject offer
            response = RejectOfferMessage(self.gamename, self.playernum)
            self.client.send_msg(response)

        # State 8 (dices have been rolled, might be forced to throw away cards, move the robber, choose player to steal from. otherwise play normally.
        elif self.gamestate == 8 and name == "DiscardRequestMessage":

            # Throw away cards here (message.numcards)
            self.discard_cards(int(message.numcards))
            
        # We need to move the robber, lets find a good spot!
        elif (self.played_knight or self.gamestate == 8) and name == "GameStateMessage" and int(message.state) == 33:

            self.play_robber()

            """if not self.rob_several and self.played_knight:
                self.roll_dices()
                self.played_knight = False
                self.debug_print("self.played_knight = False (3)")
                self.gamestate = 8"""
           
        elif (self.played_knight or self.gamestate == 8) and name == "ChoosePlayerRequestMessage":

            # Choose a player to steal from
            
            player_choices = []
            self.debug_print("Steal list: {0}".format(message.choices))
            for i,v in enumerate(message.choices):
                if v == 'true':
                    player_choices.append({'id': i, 'points': self.game.vp[i]})
            
            # Debug print steal list
            self.debug_print("Steal list with points: {0}".format(player_choices))
            
            # Find the best one
            best_id = -1
            best_points = -1
            for player in player_choices:
                if player['points'] > best_points:
                    best_points = player['points']
                    best_id = player['id']
            
            response = ChoosePlayerMessage(self.gamename, best_id)
            self.client.send_msg(response)
            
            """if self.played_knight:
                self.roll_dices()
                self.rob_several = False
                self.debug_print("self.rob_several = False (2)")
                self.played_knight = False
                self.debug_print("self.played_knight = False (4)")
                self.gamestate = 8"""

        elif self.gamestate == 8 and name == "GameStateMessage" and int(message.state) == 20:

            # Play normally
            # TODO: Do something!
            self.make_play()

    # the default playing method
    # TODO: Intelligent stuff
    def make_play(self):
        # Build with road building
        ENABLE_ROAD_CARD = False
        if ENABLE_ROAD_CARD and self.resources["ROAD_CARDS"] > 0 and self.resources["ROADS"] >= 2 and self.resources["MAY_PLAY_DEVCARD"] and not self.bought["roadcard"]:

            self.debug_print("May play devcard: {0} (1)".format(self.resources["MAY_PLAY_DEVCARD"]))
            response = PlayDevCardRequestMessage(self.gamename, 1)
            self.client.send_msg(response)

            self.resources["MAY_PLAY_DEVCARD"] = False
            
            plan = self.planner.make_plan(True)

            if plan:

                (build_spot, build_type) = plan
                logging.info("Building a {0} at {1}.".format(pieceToType[int(build_type)], hex(build_spot)))
                response = PutPieceMessage(self.gamename,self.playernum,build_type,build_spot)
                self.client.send_msg(response)
                
                # Disable building at this node
                if build_type == 0:
                    self.game.buildableRoads.roads[build_spot] = False

                plan = self.planner.make_plan(True)

                if plan and build_spot != plan[0]:

                    (build_spot, build_type) = plan

                    response = PutPieceMessage(self.gamename,self.playernum,build_type,build_spot)
                    self.client.send_msg(response)
                    
                    if build_type == 0:
                        self.game.buildableRoads.roads[build_spot] = False
        
        plan = self.planner.make_plan(False)

        self.debug_print(plan)

        if plan:
            (build_spot, build_type) = plan
            logging.info("Building a {0} at {1}.".format(pieceToType[int(build_type)], hex(build_spot)))

            response = BuildRequestMessage(self.gamename,build_type)
            self.client.send_msg(response)

            response = PutPieceMessage(self.gamename,self.playernum,build_type,build_spot)
            self.client.send_msg(response)

        #cannot afford city. buy developement card.
        #elif self.resources["DEV_CARDS"] > 0 \
        #   and ((self.resources["SETTLEMENTS"] > 0 and self.resources["SHEEP"] > 1 and self.resources["WHEAT"] > 1) \
        #   or (self.resources["SETTLEMENTS"] == 0 and self.resources["CITIES"] > 0 and self.resources["WHEAT"] > 3)) \
        #   and (self.planner.canAffordCard() or self.planner.canAffordWithTrade(3)):

        elif self.resources["DEV_CARDS"] > 0 and (self.planner.canAffordCard() or (self.total_resources() >= 6 and self.planner.canAffordWithTrade(3))):

        #elif self.resources["DEV_CARDS"] > 0 and self.total_resources() > 9 and self.planner.canAffordCard():

        #elif self.resources["DEV_CARDS"] > 0 and self.planner.canAffordCard() and (not self.planner.roads_until_settlement or self.resources["SETTLEMENTS"] == 0 or (self.planner.roads_until_settlement >= 0 and self.resources["WHEAT"] > 1 and self.resources["SHEEP"] > 1)) and (self.resources["SETTLEMENTS"] == 5 or (self.resources["SETTLEMENTS"] <= 5 and self.resources["ORE"] > 3 and self.resources["WHEAT"] > 2)):

            response = BuyCardRequestMessage(self.gamename)
            self.client.send_msg(response)

        else:
            if True and self.resources["MONOPOLY_CARDS"] > 0 and self.resources["MAY_PLAY_DEVCARD"] \
                 and not self.bought["monopolycard"]:
                #logging.critical("Playing monopoly card")
                self.client.send_msg(PlayDevCardRequestMessage(self.gamename, 3))
                self.client.send_msg(MonopolyPickMessage(self.gamename, 1))
                self.resources["MAY_PLAY_DEVCARD"] = False

            elif True and self.resources["RESOURCE_CARDS"] > 0 and self.resources["MAY_PLAY_DEVCARD"] \
                 and not self.bought["resourcecard"] and not self.bought["monopolycard"]:
                #logging.critical("Playing discovery card")
                resources = [1, 0, 0, 0, 1]
                self.client.send_msg(PlayDevCardRequestMessage(self.gamename, 2))
                self.client.send_msg(DiscoveryPickMessage(self.gamename, resources))
                self.resources["MAY_PLAY_DEVCARD"] = False

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
    
    def play_robber(self):

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
            
            # We don't want to place it on the desert
            if (tile_number == 0):
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
            num_players = {0: False, 1: False, 2: False, 3: False}
            num_different = 0.0
                
            if (n1.owner != None):
                num_settlements += 1.0 * n1.type
                num_players[n1.owner] = True
            if (n2.owner != None):
                num_settlements += 1.0 * n2.type
                num_players[n2.owner] = True
            if (n3.owner != None):
                num_settlements += 1.0 * n3.type
                num_players[n3.owner] = True
            if (n4.owner != None):
                num_settlements += 1.0 * n4.type
                num_players[n4.owner] = True
            if (n5.owner != None):
                num_settlements += 1.0 * n5.type
                num_players[n5.owner] = True
            if (n6.owner != None):
                num_settlements += 1.0 * n6.type
                num_players[n6.owner] = True
                    
            if num_players[0]:
                num_different += 1.0
            if num_players[1]:
                num_different += 1.0
            if num_players[2]:
                num_different += 1.0
            if num_players[3]:
                num_different += 1.0               
                
            robber_scale += num_settlements / 6.0 # (Maximum number of settlements around a tile is 3!)
            if (num_settlements > 0.0):
                robber_scale += 1.0 - num_different / 4.0
                
            # Append to possible tiles
            possible_tiles.append({'id': k, 'scale': robber_scale, 'num_players': num_different})
            
        # Loop possible_tiles and find best one
        best_tile_id = -1
        best_tile_scale = -1
        best_choice = None
            
        self.debug_print("Possible tiles to move robber to:")
        for tile in possible_tiles:
            self.debug_print("       id: {0}, scale: {1}".format(hex(tile['id']), tile['scale']))
            if (tile['scale'] > best_tile_scale):
                best_tile_scale = tile['scale']
                best_tile_id = tile['id']
                best_choice = tile
        self.debug_print("       ---")
        self.debug_print("       id: {0}, scale: {1} Seemed best!".format(hex(best_tile_id), best_tile_scale))
            
        # Now move robber to the best spot!
        response = MoveRobberMessage(self.gamename, self.playernum, best_tile_id)
        self.client.send_msg(response)

        """if self.played_knight and best_choice['num_players'] > 1.0:
            self.rob_several = True
            self.debug_print("self.rob_several = True (3)")"""

    def roll_dices(self):
        response = RollDiceMessage(self.gamename)
        self.client.send_msg(response)

        items = self.resources.items()
        self.debug_print("Have resources: {0} = {1}".format(items[0][0], items[0][1]))

        for res, val in items[1:]:
            if res != "UNKNOWN":
                self.debug_print("                {0} = {1}".format(res, val))

        self.bought["roadcard"] = False
        self.bought["resourcecard"] = False
        self.bought["monopolycard"] = False

    def discard_cards(self, numcards):

        response = None

        # got many settlements out and cities left to build
        #if (self.resources["SETTLEMENTS"] <= 1 or self.planner.roads_until_settlement >= 0) and self.resources["CITIES"] > 0:
        if self.resources["SETTLEMENTS"] <= 1 and self.resources["CITIES"] > 0:

            clay = 0
            wood = 0
            sheep = 0
            if self.harbor_list[1] == 0:
                clay = min(self.resources["CLAY"], numcards)
            if self.harbor_list[5] == 0:
                wood = min(self.resources["WOOD"], numcards - clay)
            if self.harbor_list[3] == 0:
                sheep = min(max(self.resources["SHEEP"] - 1,0), numcards - clay - wood)

            if self.harbor_list[1] == 1:
                clay = min(self.resources["CLAY"], numcards - wood - sheep)
            if self.harbor_list[5] == 1:
                wood = min(self.resources["WOOD"], numcards - clay - sheep)
            if self.harbor_list[3] == 1:
                sheep = min(max(self.resources["SHEEP"] - 1,0), numcards - clay - wood)
                
            ore = min(max(self.resources["ORE"] - 3,0), numcards - clay - wood - sheep)
            wheat = min(max(self.resources["WHEAT"] - 2,0), numcards - clay - wood - sheep - ore)

            if clay + wood + sheep + ore + wheat < numcards:
                sheep = self.resources["SHEEP"]

            if clay + wood + sheep + ore + wheat < numcards:
                ore = min(max(self.resources["ORE"] - 2,0), numcards - clay - wood - sheep)

            response = DiscardMessage(self.gamename, clay, ore, sheep, wheat, wood, 0)
            
        else:

            ore = 0
            
            if self.harbor_list[2] == 0:
                ore = min(self.resources["ORE"], numcards)
            
            clay = min(max(self.resources["CLAY"] - 1,0), numcards - ore)
            sheep = min(max(self.resources["SHEEP"] - 1,0), numcards - clay - ore)
            wheat = min(max(self.resources["WHEAT"] - 1,0), numcards - clay - ore - sheep)
            wood = min(max(self.resources["WOOD"] - 1,0), numcards - clay - ore - sheep - wheat)

            if self.harbor_list[2] == 1:
                ore = min(self.resources["ORE"], numcards - clay - sheep- wheat - wood)

            response = DiscardMessage(self.gamename, clay, ore, sheep, wheat, wood, 0)

        self.client.send_msg(response)
