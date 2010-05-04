from utils import cprint
from messages import *
import copy
import logging

class Planner:
    def __init__(self, game, gamename, resources, nodes, roads, client):

        self.game = game
        self.gamename = gamename
        self.nodes = nodes
        self.roads = roads
        self.resources = resources
        self.client = client

        self.probabilities = {
            0: 0,
            2: 1/36.0,
            3: 2/36.0,
            4: 3/36.0,
            5: 4/36.0,
            6: 5/36.0,
            7: 6/36.0,
            8: 5/36.0,
            9: 4/36.0,
            10: 3/36.0,
            11: 2/36.0,
            12: 1/36.0
            }

        #resources["CLAY"]
        #resources["ORE"]
        #resources["SHEEP"]
        #resources["WHEAT"]
        #resources["WOOD"]

        self.default_scores = {
             "WOOD":   1
            ,"CLAY":   1
            ,"SHEEP":  1
            ,"WHEAT":  1
            ,"ORE":    1
            ,"WOODH":  1
            ,"CLAYH":  1
            ,"SHEEPH": 1
            ,"WHEATH": 1
            ,"OREH":   1
            ,"3FOR1H": 1
        }
        
    def make_plan(self):
        from jsettlers_utils import  elementIdToType, pieceToType
        self.scores = copy.deepcopy(self.default_scores)
        self.nodeScore = {} # move
        
        # Determine what resources we are gaining
        for n in self.nodes:
            node = self.game.boardLayout.nodes[n]
            htype = node.harbor
            htype_name = elementIdToType.setdefault(str(htype), "NO HARBOUR")
            
            # If we have a certain harbour, raise the score for that resource
            if 0 < htype < 6:
                self.scores[htype_name] += 1
                
            # If we have a 3 for 1 harbour: lower the score for building a new one
            elif htype == 6:
                self.scores[htype_name] = 0.5
                
            tiles = [self.game.boardLayout.tiles[t] for t in [node.t1, node.t2, node.t3] if t != None]

            city_bonus = 1
            if node.type == 2:
                city_bonus = 2
            
            #if we have a settlement where we get a resource, lower the score for that resource
            #if we have a settlement where we get a resource, raise the score for that harbor.
            for tile in tiles:
                if 0 < tile.resource < 6:
                    res_name  = elementIdToType[str(tile.resource)]
                    score_mod = self.probabilities.setdefault(tile.number, 0) * city_bonus
                    self.scores[res_name] -= score_mod
                    self.scores[res_name + "H"] += 2 * score_mod
           
        self.node_scores = {}
        possible_roads = [] # use a set?

        possible_roads += self.roads

        buildable_roads = self.game.buildableRoads.roads
        for r in buildable_roads:
            if buildable_roads[r] and r not in possible_roads:
                possible_roads.append(r)

        for r in possible_roads:
            self.calcNeighbourScore(r, 0)

        best_node = None
        if len(self.nodeScore) > 0:
            tempList = sorted(self.nodeScore.items(), cmp=lambda a,b: int(1000*b[1]) - int(1000*a[1]))
            (best_pos, score) = tempList[0]
            best_node = self.game.boardLayout.nodes[best_pos]
            for i, item in enumerate(tempList):
                (node,score) = item
                self.debug_print("{0}. {1} ({2})".format(i,hex(node),score))
        else:
            self.debug_print("No good spots found!")

        # Find out how to build to that node
        if best_node:
            self.debug_print("Best location: {0}".format(hex(best_node.id)))
            
            roads = [self.game.boardLayout.roads[r] for r in [best_node.n1, best_node.n2, best_node.n3] if r != None]
            for road in roads:
                self.debug_print("Road {0} belongs to: {1}".format(hex(road.id), road.owner))

            # If we own any of the roads
            if any(r.owner and r.owner == int(self.game.playernum) for r in roads):
                if self.resources["SETTLEMENTS"] > 0 and self.canAffordSettlement():
                    self.debug_print("Can build settlement, sending...")
                    return (best_node.id, 1)
                elif self.resources["SETTLEMENTS"] > 0 and self.canAffordWithTrade(1):
                    self.debug_print("Can afford s after trade...")
                    return (best_node.id, 1)
                else:
                    self.debug_print("Cannot afford settlement.")
                    self.debug_print("Wood: {0}".format(self.resources["WOOD"]))
                    self.debug_print("Clay: {0}".format(self.resources["CLAY"]))
                    self.debug_print("Sheep: {0}".format(self.resources["SHEEP"]))
                    self.debug_print("Wheat: {0}".format(self.resources["WHEAT"]))

            else:
                if self.resources["ROADS"] > 0 and self.canAffordRoad():
                    self.debug_print("Can build road, sending...")
                    return self.findClosestBuildableRoad([road.id for road in roads])
                elif self.resources["ROADS"] > 0 and self.canAffordWithTrade(0):
                    self.debug_print("Can afford road after trade...")
                    return self.findClosestBuildableRoad([road.id for road in roads])
                else:
                    self.debug_print("Cannot afford road.")
                    self.debug_print("Wood: {0}".format(self.resources["WOOD"]))
                    self.debug_print("Clay: {0}".format(self.resources["CLAY"]))

        # Cannot afford settlement and shouldn't/cannot build road. Try upgrading to city.

        if self.resources["CITIES"] > 0:
            self.cityScore = {}

            for n in self.nodes:
                node = self.game.boardLayout.nodes[n]
                if node.type == 1:
                    harbour = node.harbor
                    
                    if 0 < harbour < 6:
                        tempScore = self.scores[str(elementIdToType[harbour]) + "H"]
                    elif harbour == 6:
                        tempScore = self.scores["3FOR1H"]
                    else:
                        tempScore = 0

                    t1 = self.game.boardLayout.nodes[n].t1
                    t2 = self.game.boardLayout.nodes[n].t2
                    t3 = self.game.boardLayout.nodes[n].t3
                        
                    if t1 and self.game.boardLayout.tiles[t1].resource == 1:
                        tempScore += self.scores["CLAY"]
                        if self.game.boardLayout.nodes[n].harbor == 1:
                            tempScore += self.probabilities[self.game.boardLayout.tiles[t1].number]

                    elif t1 and self.game.boardLayout.tiles[t1].resource == 2:
                        tempScore += self.scores["ORE"]
                        if self.game.boardLayout.nodes[n].harbor == 2:
                            tempScore += self.probabilities[self.game.boardLayout.tiles[t1].number]

                    elif t1 and self.game.boardLayout.tiles[t1].resource == 3:
                        tempScore += self.scores["SHEEP"]
                        if self.game.boardLayout.nodes[n].harbor == 3:
                            tempScore += self.probabilities[self.game.boardLayout.tiles[t1].number]

                    elif t1 and self.game.boardLayout.tiles[t1].resource == 4:
                        tempScore += self.scores["WHEAT"]
                        if self.game.boardLayout.nodes[n].harbor == 4:
                            tempScore += self.probabilities[self.game.boardLayout.tiles[t1].number]

                    elif t1 and self.game.boardLayout.tiles[t1].resource == 5:
                        tempScore += self.scores["WOOD"]
                        if self.game.boardLayout.nodes[n].harbor == 5:
                            tempScore += self.probabilities[self.game.boardLayout.tiles[t1].number]
                       
                    if t2 and self.game.boardLayout.tiles[t2].resource == 1:
                        tempScore += self.scores["CLAY"]
                        if self.game.boardLayout.nodes[n].harbor == 1:
                            tempScore += self.probabilities[self.game.boardLayout.tiles[t2].number]

                    elif t2 and self.game.boardLayout.tiles[t2].resource == 2:
                        tempScore += self.scores["ORE"]
                        if self.game.boardLayout.nodes[n].harbor == 2:
                            tempScore += self.probabilities[self.game.boardLayout.tiles[t2].number]

                    elif t2 and self.game.boardLayout.tiles[t2].resource == 3:
                        tempScore += self.scores["SHEEP"]
                        if self.game.boardLayout.nodes[n].harbor == 3:
                            tempScore += self.probabilities[self.game.boardLayout.tiles[t2].number]

                    elif t2 and self.game.boardLayout.tiles[t2].resource == 4:
                        tempScore += self.scores["WHEAT"]
                        if self.game.boardLayout.nodes[n].harbor == 4:
                            tempScore += self.probabilities[self.game.boardLayout.tiles[t2].number]

                    elif t2 and self.game.boardLayout.tiles[t2].resource == 5:
                        tempScore += self.scores["WOOD"]
                        if self.game.boardLayout.nodes[n].harbor == 5:
                            tempScore += self.probabilities[self.game.boardLayout.tiles[t2].number]
                        
                    if t3 and self.game.boardLayout.tiles[t3].resource == 1:
                        tempScore += self.scores["CLAY"]
                        if self.game.boardLayout.nodes[n].harbor == 1:
                            tempScore += self.probabilites[self.game.boardLayout.tiles[t3].number]

                    elif t3 and self.game.boardLayout.tiles[t3].resource == 2:
                        tempScore += self.scores["ORE"]
                        if self.game.boardLayout.nodes[n].harbor == 2:
                            tempScore += self.probabilites[self.game.boardLayout.tiles[t3].number]

                    elif t3 and self.game.boardLayout.tiles[t3].resource == 3:
                        tempScore += self.scores["SHEEP"]
                        if self.game.boardLayout.nodes[n].harbor == 3:
                            tempScore += self.probabilites[self.game.boardLayout.tiles[t3].number]

                    elif t3 and self.game.boardLayout.tiles[t3].resource == 4:
                        tempScore += self.scores["WHEAT"]
                        if self.game.boardLayout.nodes[n].harbor == 4:
                            tempScore += self.probabilites[self.game.boardLayout.tiles[t3].number]

                    elif t3 and self.game.boardLayout.tiles[t3].resource == 5:
                        tempScore += self.scores["WOOD"]
                        if self.game.boardLayout.nodes[n].harbor == 5:
                            tempScore += self.probabilites[self.game.boardLayout.tiles[t3].number]

                    self.cityScore[n] = tempScore

            if len(self.cityScore) > 0:
                cityList = sorted(self.cityScore.items(), cmp=lambda a,b: int(1000*b[1]) - int(1000*a[1]))
                (bestNode, score) = cityList[0]

                if bestNode:
                    if self.canAffordCity():
                        self.debug_print("Can build city, sending...")
                        return (bestNode, 2)
                    elif self.canAffordWithTrade(2):
                        self.debug_print("Can afford c after trade...")
                        return (bestNode, 2)
                    else:
                        self.debug_print("Cannot afford city.")
                        self.debug_print("Wheat: {0}".format(self.resources["WHEAT"]))
                        self.debug_print("Ore: {0}".format(self.resources["ORE"]))

        return None


    def debug_print(self, msg):
        import logging
        logging.info(msg)

    def canAffordRoad(self):

        return self.resources["WOOD"] >= 1 and self.resources["CLAY"] >= 1

    def canAffordSettlement(self):

        return self.resources["WOOD"] >= 1 and self.resources["CLAY"] >= 1 and self.resources["SHEEP"] >= 1 and self.resources["WHEAT"] >= 1

    def canAffordCity(self):

        return self.resources["WHEAT"] >= 2 and self.resources["ORE"] >= 3
        
    def calcNeighbourScore(self, road, depth):

        n1 = self.game.boardLayout.roads[road].n1
        n2 = self.game.boardLayout.roads[road].n2

        if self.game.buildableNodes.nodes[n1]:

            if self.game.boardLayout.nodes[n1].harbor == 1:
                tempScore = self.scores["CLAYH"]

            elif self.game.boardLayout.nodes[n1].harbor == 2:
                tempScore = self.scores["OREH"]

            elif self.game.boardLayout.nodes[n1].harbor == 3:
                tempScore = self.scores["SHEEPH"]

            elif self.game.boardLayout.nodes[n1].harbor == 4:
                tempScore = self.scores["WHEATH"]

            elif self.game.boardLayout.nodes[n1].harbor == 5:
                tempScore = self.scores["WOODH"]

            elif self.game.boardLayout.nodes[n1].harbor == 6:
                tempScore = self.scores["3FOR1H"]

            else:
                tempScore = 0
            
            t1 = self.game.boardLayout.nodes[n1].t1
            t2 = self.game.boardLayout.nodes[n1].t2
            t3 = self.game.boardLayout.nodes[n1].t3
                
            if t1 and self.game.boardLayout.tiles[t1].resource == 1:
                tempScore += self.scores["CLAY"]
                if self.game.boardLayout.nodes[n1].harbor == 1:
                    tempScore += self.probabilities[self.game.boardLayout.tiles[t1].number]

            elif t1 and self.game.boardLayout.tiles[t1].resource == 2:
                tempScore += self.scores["ORE"]
                if self.game.boardLayout.nodes[n1].harbor == 2:
                    tempScore += self.probabilities[self.game.boardLayout.tiles[t1].number]

            elif t1 and self.game.boardLayout.tiles[t1].resource == 3:
                tempScore += self.scores["SHEEP"]
                if self.game.boardLayout.nodes[n1].harbor == 3:
                    tempScore += self.probabilities[self.game.boardLayout.tiles[t1].number]

            elif t1 and self.game.boardLayout.tiles[t1].resource == 4:
                tempScore += self.scores["WHEAT"]
                if self.game.boardLayout.nodes[n1].harbor == 4:
                    tempScore += self.probabilities[self.game.boardLayout.tiles[t1].number]

            elif t1 and self.game.boardLayout.tiles[t1].resource == 5:
                tempScore += self.scores["WOOD"]
                if self.game.boardLayout.nodes[n1].harbor == 5:
                    tempScore += self.probabilities[self.game.boardLayout.tiles[t1].number]
               
            if t2 and self.game.boardLayout.tiles[t2].resource == 1:
                tempScore += self.scores["CLAY"]
                if self.game.boardLayout.nodes[n1].harbor == 1:
                    tempScore += self.probabilities[self.game.boardLayout.tiles[t2].number]

            elif t2 and self.game.boardLayout.tiles[t2].resource == 2:
                tempScore += self.scores["ORE"]
                if self.game.boardLayout.nodes[n1].harbor == 2:
                    tempScore += self.probabilities[self.game.boardLayout.tiles[t2].number]

            elif t2 and self.game.boardLayout.tiles[t2].resource == 3:
                tempScore += self.scores["SHEEP"]
                if self.game.boardLayout.nodes[n1].harbor == 3:
                    tempScore += self.probabilities[self.game.boardLayout.tiles[t2].number]

            elif t2 and self.game.boardLayout.tiles[t2].resource == 4:
                tempScore += self.scores["WHEAT"]
                if self.game.boardLayout.nodes[n1].harbor == 4:
                    tempScore += self.probabilities[self.game.boardLayout.tiles[t2].number]

            elif t2 and self.game.boardLayout.tiles[t2].resource == 5:
                tempScore += self.scores["WOOD"]
                if self.game.boardLayout.nodes[n1].harbor == 5:
                    tempScore += self.probabilities[self.game.boardLayout.tiles[t2].number]
                
            if t3 and self.game.boardLayout.tiles[t3].resource == 1:
                tempScore += self.scores["CLAY"]
                if self.game.boardLayout.nodes[n1].harbor == 1:
                    tempScore += self.probabilites[self.game.boardLayout.tiles[t3].number]

            elif t3 and self.game.boardLayout.tiles[t3].resource == 2:
                tempScore += self.scores["ORE"]
                if self.game.boardLayout.nodes[n1].harbor == 2:
                    tempScore += self.probabilites[self.game.boardLayout.tiles[t3].number]

            elif t3 and self.game.boardLayout.tiles[t3].resource == 3:
                tempScore += self.scores["SHEEP"]
                if self.game.boardLayout.nodes[n1].harbor == 3:
                    tempScore += self.probabilites[self.game.boardLayout.tiles[t3].number]

            elif t3 and self.game.boardLayout.tiles[t3].resource == 4:
                tempScore += self.scores["WHEAT"]
                if self.game.boardLayout.nodes[n1].harbor == 4:
                    tempScore += self.probabilites[self.game.boardLayout.tiles[t3].number]

            elif t3 and self.game.boardLayout.tiles[t3].resource == 5:
                tempScore += self.scores["WOOD"]
                if self.game.boardLayout.nodes[n1].harbor == 5:
                    tempScore += self.probabilites[self.game.boardLayout.tiles[t3].number]

            tempScore += (4 - 2*depth)
            if depth == 0 and self.game.boardLayout.roads[road].owner == None:
                tempScore -= 1

            if n1 not in self.nodeScore or tempScore > self.nodeScore[n1]:
                self.nodeScore[n1] = tempScore
                
        #only look for settlement point maximum 2 roads away
        if depth < 2:
            d = 1
            if depth == 0 and self.game.boardLayout.roads[road].owner == None:
                d = 2
            r1 = self.game.boardLayout.nodes[n1].n1
            if r1 and self.game.boardLayout.roads[r1].owner == None:
                self.calcNeighbourScore(r1, depth + d)
            r2 = self.game.boardLayout.nodes[n1].n2
            if r2 and self.game.boardLayout.roads[r2].owner == None:
                self.calcNeighbourScore(r2, depth + d)
            r3 = self.game.boardLayout.nodes[n1].n3
            if r3 and self.game.boardLayout.roads[r3].owner == None:
                self.calcNeighbourScore(r3, depth + d)

        if self.game.buildableNodes.nodes[n2]:

            if self.game.boardLayout.nodes[n2].harbor == 1:
                tempScore = self.scores["CLAYH"]

            elif self.game.boardLayout.nodes[n2].harbor == 2:
                tempScore = self.scores["OREH"]

            elif self.game.boardLayout.nodes[n2].harbor == 3:
                tempScore = self.scores["SHEEPH"]

            elif self.game.boardLayout.nodes[n2].harbor == 4:
                tempScore = self.scores["WHEATH"]

            elif self.game.boardLayout.nodes[n2].harbor == 5:
                tempScore = self.scores["WOODH"]

            elif self.game.boardLayout.nodes[n2].harbor == 6:
                tempScore = self.scores["3FOR1H"]

            else:
                tempScore = 0
            
            t1 = self.game.boardLayout.nodes[n2].t1
            t2 = self.game.boardLayout.nodes[n2].t2
            t3 = self.game.boardLayout.nodes[n2].t3
                
            if t1 and self.game.boardLayout.tiles[t1].resource == 1:
                tempScore += self.scores["CLAY"]
                if self.game.boardLayout.nodes[n2].harbor == 1:
                    tempScore += self.probabilities[self.game.boardLayout.tiles[t1].number]

            elif t1 and self.game.boardLayout.tiles[t1].resource == 2:
                tempScore += self.scores["ORE"]
                if self.game.boardLayout.nodes[n2].harbor == 2:
                    tempScore += self.probabilities[self.game.boardLayout.tiles[t1].number]

            elif t1 and self.game.boardLayout.tiles[t1].resource == 3:
                tempScore += self.scores["SHEEP"]
                if self.game.boardLayout.nodes[n2].harbor == 3:
                    tempScore += self.probabilities[self.game.boardLayout.tiles[t1].number]

            elif t1 and self.game.boardLayout.tiles[t1].resource == 4:
                tempScore += self.scores["WHEAT"]
                if self.game.boardLayout.nodes[n2].harbor == 4:
                    tempScore += self.probabilities[self.game.boardLayout.tiles[t1].number]

            elif t1 and self.game.boardLayout.tiles[t1].resource == 5:
                tempScore += self.scores["WOOD"]
                if self.game.boardLayout.nodes[n2].harbor == 5:
                    tempScore += self.probabilities[self.game.boardLayout.tiles[t1].number]
               
            if t2 and self.game.boardLayout.tiles[t2].resource == 1:
                tempScore += self.scores["CLAY"]
                if self.game.boardLayout.nodes[n2].harbor == 1:
                    tempScore += self.probabilities[self.game.boardLayout.tiles[t2].number]

            elif t2 and self.game.boardLayout.tiles[t2].resource == 2:
                tempScore += self.scores["ORE"]
                if self.game.boardLayout.nodes[n2].harbor == 2:
                    tempScore += self.probabilities[self.game.boardLayout.tiles[t2].number]

            elif t2 and self.game.boardLayout.tiles[t2].resource == 3:
                tempScore += self.scores["SHEEP"]
                if self.game.boardLayout.nodes[n2].harbor == 3:
                    tempScore += self.probabilities[self.game.boardLayout.tiles[t2].number]

            elif t2 and self.game.boardLayout.tiles[t2].resource == 4:
                tempScore += self.scores["WHEAT"]
                if self.game.boardLayout.nodes[n2].harbor == 4:
                    tempScore += self.probabilities[self.game.boardLayout.tiles[t2].number]

            elif t2 and self.game.boardLayout.tiles[t2].resource == 5:
                tempScore += self.scores["WOOD"]
                if self.game.boardLayout.nodes[n2].harbor == 5:
                    tempScore += self.probabilities[self.game.boardLayout.tiles[t2].number]
                
            if t3 and self.game.boardLayout.tiles[t3].resource == 1:
                tempScore += self.scores["CLAY"]
                if self.game.boardLayout.nodes[n2].harbor == 1:
                    tempScore += self.probabilities[self.game.boardLayout.tiles[t3].number]

            elif t3 and self.game.boardLayout.tiles[t3].resource == 2:
                tempScore += self.scores["ORE"]
                if self.game.boardLayout.nodes[n2].harbor == 2:
                    tempScore += self.probabilities[self.game.boardLayout.tiles[t3].number]

            elif t3 and self.game.boardLayout.tiles[t3].resource == 3:
                tempScore += self.scores["SHEEP"]
                if self.game.boardLayout.nodes[n2].harbor == 3:
                    tempScore += self.probabilities[self.game.boardLayout.tiles[t3].number]

            elif t3 and self.game.boardLayout.tiles[t3].resource == 4:
                tempScore += self.scores["WHEAT"]
                if self.game.boardLayout.nodes[n2].harbor == 4:
                    tempScore += self.probabilities[self.game.boardLayout.tiles[t3].number]

            elif t3 and self.game.boardLayout.tiles[t3].resource == 5:
                tempScore += self.scores["WOOD"]
                if self.game.boardLayout.nodes[n2].harbor == 5:
                    tempScore += self.probabilities[self.game.boardLayout.tiles[t3].number]

            tempScore += (4 - 2*depth)
            if depth == 0 and self.game.boardLayout.roads[road].owner == None:
                tempScore -= 1

            if n2 not in self.nodeScore or tempScore > self.nodeScore[n2]:
                self.nodeScore[n2] = tempScore

        #only look for settlement point maximum 2 roads away
        if depth < 2:
            d = 1
            if depth == 0 and self.game.boardLayout.roads[road].owner == None:
                d = 2
            r1 = self.game.boardLayout.nodes[n2].n1
            if r1 and self.game.boardLayout.roads[r1].owner == None:
                self.calcNeighbourScore(r1, depth + d)
            r2 = self.game.boardLayout.nodes[n2].n2
            if r2 and self.game.boardLayout.roads[r2].owner == None:
                self.calcNeighbourScore(r2, depth + d)
            r3 = self.game.boardLayout.nodes[n2].n3
            if r3 and self.game.boardLayout.roads[r3].owner == None:
                self.calcNeighbourScore(r3, depth + d)

        return

    #finds the closest buildable road to a node
    def findClosestBuildableRoad(self, parents):

        for r in parents:

            if self.game.buildableRoads.roads[r]:
                return(r,0)
            
        for r in parents:

            n1 = self.game.boardLayout.roads[r].n1
            n2 = self.game.boardLayout.roads[r].n2

            r1 = self.game.boardLayout.nodes[n1].n1
            r2 = self.game.boardLayout.nodes[n1].n2
            r3 = self.game.boardLayout.nodes[n1].n3

            if r1 and self.game.buildableRoads.roads[r1]:
                return (r1, 0) 

            if r2 and self.game.buildableRoads.roads[r2]:
                return (r2, 0)

            if r3 and self.game.buildableRoads.roads[r3]:
                return (r3, 0)

            r1 = self.game.boardLayout.nodes[n2].n1
            r2 = self.game.boardLayout.nodes[n2].n2
            r3 = self.game.boardLayout.nodes[n2].n3

            if r1 and self.game.buildableRoads.roads[r1]:
                return (r1, 0) 

            if r2 and self.game.buildableRoads.roads[r2]:
                return (r2, 0)

            if r3 and self.game.buildableRoads.roads[r3]:
                return (r3, 0)

        return None

    def canAffordWithTrade(self,_type):

        wood_trade = 4
        clay_trade = 4
        wheat_trade = 4
        sheep_trade = 4
        ore_trade = 4
        h3for1_trade = 4

        for n in self.nodes:

            if self.game.boardLayout.nodes[n].harbor == 6:
                h3for1_trade = 3
                self.debug_print("Found 3for1 harbor")

            elif self.game.boardLayout.nodes[n].harbor == 1:
                clay_trade = 2
                self.debug_print("Found clay harbor")            
                
            elif self.game.boardLayout.nodes[n].harbor == 2:
                ore_trade = 2
                self.debug_print("Found ore harbor")

            elif self.game.boardLayout.nodes[n].harbor == 3:
                sheep_trade = 2
                self.debug_print("Found sheep harbor")

            elif self.game.boardLayout.nodes[n].harbor == 4:
                wheat_trade = 2
                self.debug_print("Found wheat harbor")
                
            elif self.game.boardLayout.nodes[n].harbor == 5:
                wood_trade = 2
                self.debug_print("Found wood harbor")

        wood_trade = min(wood_trade,h3for1_trade)
        clay_trade = min(clay_trade,h3for1_trade)
        wheat_trade = min(wheat_trade,h3for1_trade)
        sheep_trade = min(sheep_trade,h3for1_trade)
        ore_trade = min(ore_trade,h3for1_trade)

        if _type == 1:

            self.debug_print("Trying to trade for s...")
            clay_needed = max(0, 1 - self.resources["CLAY"])
            wood_needed = max(0, 1 - self.resources["WOOD"])
            sheep_needed = max(0, 1 - self.resources["SHEEP"])
            wheat_needed = max(0, 1 - self.resources["WHEAT"])
            self.debug_print("Missing {0} clay, {1} wood, {2} sheep, {3} wheat.".format(clay_needed,wood_needed,sheep_needed,wheat_needed))

            wood_gives = (max(0, self.resources["WOOD"] - 1)) / min(wood_trade, h3for1_trade)
            clay_gives = (max(0, self.resources["CLAY"] - 1)) / min(clay_trade, h3for1_trade)
            wheat_gives = (max(0, self.resources["WHEAT"] - 1)) / min(wheat_trade, h3for1_trade)
            ore_gives = self.resources["ORE"] / min(ore_trade, h3for1_trade)
            sheep_gives = (max(0, self.resources["SHEEP"] - 1)) / min(sheep_trade, h3for1_trade)

            self.debug_print("Might get:{0},{1},{2},{3},{4}".format(clay_gives,ore_gives,sheep_gives,wheat_gives,wood_gives))

            if (wood_gives + clay_gives + wheat_gives + ore_gives + sheep_gives) >= (clay_needed + wood_needed + sheep_needed + wheat_needed):
                ore_to_trade = 0
                wheat_to_trade = 0
                sheep_to_trade = 0
                wood_to_trade = 0
                clay_to_trade = 0
                left_to_trade = clay_needed + wood_needed + sheep_needed + wheat_needed

                while left_to_trade > 0:
                
                    if ore_gives > 0 and left_to_trade > 0:
                        ore_to_trade += ore_trade
                        ore_gives -= 1
                        left_to_trade -= 1

                    if wheat_gives > 0 and left_to_trade > 0:
                        wheat_to_trade += wheat_trade
                        wheat_gives -= 1
                        left_to_trade -= 1

                    if sheep_gives > 0 and left_to_trade > 0:
                        sheep_to_trade += sheep_trade
                        sheep_gives -= 1
                        left_to_trade -= 1

                    if wood_gives > 0 and left_to_trade > 0:
                        wood_to_trade += wood_trade
                        wood_gives -= 1
                        left_to_trade -= 1

                    if clay_gives > 0 and left_to_trade > 0:
                        clay_to_trade += clay_trade
                        clay_gives -= 1
                        left_to_trade -= 1

                response = BankTradeMessage(self.gamename,[clay_to_trade,ore_to_trade,sheep_to_trade,wheat_to_trade,wood_to_trade],[clay_needed,0,sheep_needed,wheat_needed,wood_needed])
                self.debug_print("Trade1: {0},{1}".format([clay_to_trade,ore_to_trade,sheep_to_trade,wheat_to_trade,wood_to_trade],[clay_needed,0,sheep_needed,wheat_needed,wood_needed]))
                self.client.send_msg(response)

                return True 

            return False

        elif _type == 0:

            self.debug_print("Trying to trade for road...")
            clay_needed = max(0, 1 - self.resources["CLAY"])
            wood_needed = max(0, 1 - self.resources["WOOD"])
            self.debug_print("Missing {0} clay, {1} wood.".format(clay_needed,wood_needed))

            wood_gives = (max(0, self.resources["WOOD"] - 1)) / min(wood_trade, h3for1_trade, 4)
            clay_gives = (max(0, self.resources["CLAY"] - 1)) / min(clay_trade, h3for1_trade, 4)
            wheat_gives = self.resources["WHEAT"] / min(wheat_trade, h3for1_trade, 4)
            ore_gives = self.resources["ORE"] / min(ore_trade, h3for1_trade, 4)
            sheep_gives = self.resources["SHEEP"] / min(sheep_trade, h3for1_trade, 4)

            self.debug_print("Might get:{0},{1},{2},{3},{4}".format(clay_gives,ore_gives,sheep_gives,wheat_gives,wood_gives))

            if wood_gives + clay_gives + wheat_gives + ore_gives + sheep_gives >= clay_needed + wood_needed:
                ore_to_trade = 0
                wheat_to_trade = 0
                sheep_to_trade = 0
                wood_to_trade = 0
                clay_to_trade = 0
                left_to_trade = clay_needed + wood_needed

                while left_to_trade > 0:
                
                    if ore_gives > 0 and left_to_trade > 0:
                        ore_to_trade += ore_trade
                        ore_gives -= 1
                        left_to_trade -= 1

                    if wheat_gives > 0 and left_to_trade > 0:
                        wheat_to_trade += wheat_trade
                        wheat_gives -= 1
                        left_to_trade -= 1

                    if sheep_gives > 0 and left_to_trade > 0:
                        sheep_to_trade += sheep_trade
                        sheep_gives -= 1
                        left_to_trade -= 1

                    if wood_gives > 0 and left_to_trade > 0:
                        wood_to_trade += wood_trade
                        wood_gives -= 1
                        left_to_trade -= 1

                    if clay_gives > 0 and left_to_trade > 0:
                        clay_to_trade += clay_trade
                        clay_gives -= 1
                        left_to_trade -= 1

                response = BankTradeMessage(self.gamename,[clay_to_trade,ore_to_trade,sheep_to_trade,wheat_to_trade,wood_to_trade],[clay_needed,0,0,0,wood_needed])
                self.debug_print("Trade2: {0},{1}".format([clay_to_trade,ore_to_trade,sheep_to_trade,wheat_to_trade,wood_to_trade],[clay_needed,0,0,0,wood_needed]))
                self.client.send_msg(response)

                return True

            return False

        elif _type == 2:

            self.debug_print("Trying to trade for city...")
            wheat_needed = max(0, 2 - self.resources["WHEAT"])
            ore_needed = max(0, 3 - self.resources["ORE"])
            self.debug_print("Missing {0} wheat, {1} ore.".format(wheat_needed,ore_needed))

            wood_gives = self.resources["WOOD"] / min(wood_trade, h3for1_trade, 4)
            clay_gives = self.resources["CLAY"] / min(clay_trade, h3for1_trade, 4)
            wheat_gives = (max(0, self.resources["WHEAT"] - 2)) / min(wheat_trade, h3for1_trade, 4)
            ore_gives = (max(0, self.resources["ORE"] - 3)) / min(ore_trade, h3for1_trade, 4)
            sheep_gives = self.resources["SHEEP"] / min(sheep_trade, h3for1_trade, 4)

            self.debug_print("Might get:{0},{1},{2},{3},{4}".format(clay_gives,ore_gives,sheep_gives,wheat_gives,wood_gives))

            if (wood_gives + clay_gives + wheat_gives + ore_gives + sheep_gives) >= (wheat_needed + ore_needed):
                ore_to_trade = 0
                wheat_to_trade = 0
                sheep_to_trade = 0
                wood_to_trade = 0
                clay_to_trade = 0
                left_to_trade = wheat_needed + ore_needed

                while left_to_trade > 0:
                
                    if ore_gives > 0 and left_to_trade > 0:
                        ore_to_trade += ore_trade
                        ore_gives -= 1
                        left_to_trade -= 1

                    if wheat_gives > 0 and left_to_trade > 0:
                        wheat_to_trade += wheat_trade
                        wheat_gives -= 1
                        left_to_trade -= 1

                    if sheep_gives > 0 and left_to_trade > 0:
                        sheep_to_trade += sheep_trade
                        sheep_gives -= 1
                        left_to_trade -= 1

                    if wood_gives > 0 and left_to_trade > 0:
                        wood_to_trade += wood_trade
                        wood_gives -= 1
                        left_to_trade -= 1

                    if clay_gives > 0 and left_to_trade > 0:
                        clay_to_trade += clay_trade
                        clay_gives -= 1
                        left_to_trade -= 1

                response = BankTradeMessage(self.gamename,[clay_to_trade,ore_to_trade,sheep_to_trade,wheat_to_trade,wood_to_trade],[0,ore_needed,0,wheat_needed,0])
                self.debug_print("Trade3: {0},{1}".format([clay_to_trade,ore_to_trade,sheep_to_trade,wheat_to_trade,wood_to_trade],[0,ore_needed,0,wheat_needed,0]))
                self.client.send_msg(response)

                return True

        return False
