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
        
        self.scores = {}
        
    def get_resource_name(self, name, is_harbour = False):
        if is_harbour:
            suffix = "H"
        else:
            suffix = ""
            
        if type(name) == type(1):
            from jsettlers_utils import elementIdToType
            if 0 < name < 6:
                name = elementIdToType[str(name)]
            elif is_harbour and name == 6:
                name = "3FOR1"
            else:
                logging.critical("Supplied integer {0} is not valid. Must be in range(1..6).")
            return name + suffix
        else:
            name = name.upper()
            if is_harbour and not name.endswith("H"):
                name = name + suffix
            return name.upper()
            
    def set_resource_score(self, resource, score):
        name = self.get_resource_name(resource)
        self.scores[name] = score
    
    def add_resource_score(self, resource, score):
        name = self.get_resource_name(resource)
        self.scores[name] += score
            
    def get_resource_score(self, resource):
        name = self.get_resource_name(resource)
        return self.scores[name]

    def set_harbour_score(self, harbour, score):
        name = self.get_resource_name(harbour, True)
        self.scores[name] = score
            
    def add_harbour_score(self, harbour, score):
        name = self.get_resource_name(harbour, True)
        self.scores[name] += score
            
    def get_harbour_score(self, harbour):
        name = self.get_resource_name(harbour, True)
        return self.scores[name]
    
    def make_plan(self):
        from jsettlers_utils import  elementIdToType, pieceToType
        self.scores = copy.deepcopy(self.default_scores)
        
        # Determine what resources we are gaining
        for n in self.nodes:
            node = self.game.boardLayout.nodes[n]
            
            # If we have a certain harbour, raise the score for that resource
            if 0 < node.harbor < 6:
                self.add_resource_score(node.harbor, 1)
                
            # If we have a 3 for 1 harbour: lower the score for building a new one
            elif node.harbor == 6:
                self.set_harbour_score(node.harbor, 0.5)
                
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
                    self.add_resource_score(tile.resource, -score_mod)
                    self.add_harbour_score(tile.resource, 1.5 * score_mod)
           
        possible_roads = []
        possible_roads += self.roads
        buildable_roads = self.game.buildableRoads.roads
        for r in buildable_roads:
            if buildable_roads[r] and r not in possible_roads:
                possible_roads.append(r)

        self.nodeScore = {} 
        logging.info("Possible roads: {0}".format(map(hex, possible_roads)))
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
            self.debug_print("Best location: {0}".format(best_node.id))
            
            roads = [self.game.boardLayout.roads[r] for r in [best_node.n1, best_node.n2, best_node.n3] if r != None]
            for road in roads:
                self.debug_print("Road {0} belongs to: {1}".format(road.id, road.owner))

            if any(r.owner and int(r.owner) == int(self.game.playernum) for r in roads):
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
                    if 0 < node.harbor < 7:
                        temp_score = self.get_harbour_score(node.harbor)
                    else:
                        temp_score = 0
                    
                    tiles = [self.game.boardLayout.tiles[t] for t in [node.t1, node.t2, node.t3] if t != None]
                    
                   # Reference
                   # elif t1 and self.game.boardLayout.tiles[t1].resource == 3:
                   #     tempScore += self.scores["SHEEP"]
                   #     if node.harbor == 3:
                   #         tempScore += self.probabilities[self.game.boardLayout.tiles[t1].number]
                    for tile in tiles:
                        if 0 < tile.resource < 6:
                            # Add resource score for all resource types
                            temp_score += self.get_resource_score(tile.resource)
                            
                            # If it's a harbour (?), add probability assigned to the neighbouring tile.
                            if 0 < node.harbor < 6:
                                temp_score += self.probabilities[tile.number]

                    self.cityScore[n] = temp_score

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
        road_node = self.game.boardLayout.roads[road]

        #check if the road is actually unbuildable due to an enemy settlement
        if road in self.game.buildableRoads.roads and ((self.game.boardLayout.nodes[n1].owner and int(self.game.boardLayout.nodes[n1].owner) != int(self.game.playernum)) or (self.game.boardLayout.nodes[n2].owner and int(self.game.boardLayout.nodes[n2].owner) != int(self.game.playernum))):
            return
                    
        
        for n in [n1, n2]:
            node = self.game.boardLayout.nodes[n]
            is_buildable = self.game.buildableNodes.nodes[n]
            if is_buildable:
                if 0 < node.harbor < 7:
                    temp_score = self.get_harbour_score(node.harbor)
                else:
                    temp_score = 0
                
                tiles = [self.game.boardLayout.tiles[t] for t in [node.t1, node.t2, node.t3] if t != None]
                for tile in tiles:
                    if 0 < tile.resource < 6:
                        # Add resource score for all resource types
                        temp_score += self.get_resource_score(tile.resource)
                        
                        # If it's a harbour (?), add probability assigned to the neighbouring tile.
                        if 0 < node.harbor < 6:
                            temp_score += self.probabilities[tile.number]

                temp_score += (3 - depth)
                if depth == 0 and road_node.owner == None:
                    temp_score -= 1

                if n not in self.nodeScore or temp_score > self.nodeScore[n]:
                    self.nodeScore[n] = temp_score
                
            #only look for settlement point maximum 3 roads away
            if depth < 3:
                d = 1
                if depth == 0 and road_node.owner == None:
                    d = 2
                    
                roads = [self.game.boardLayout.roads[r] for r in \
                            [node.n1, node.n2, node.n3] if r != None]
                
                # Explore roads
                for r in roads:
                    if r.owner == None:
                        self.calcNeighbourScore(r.id, depth + d)
                
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
                left_to_trade = clay_needed + wood_needed + sheep_needed + wheat_needed

                while left_to_trade > 0:
                
                    if ore_gives > 0 and left_to_trade > 0:
                        if clay_needed > 0:
                            self.client.send_msg(BankTradeMessage(self.gamename,[0,ore_trade,0,0,0],[1,0,0,0,0]))
                            clay_needed -= 1
                        elif wood_needed > 0:
                            self.client.send_msg(BankTradeMessage(self.gamename,[0,ore_trade,0,0,0],[0,0,0,0,1]))
                            wood_needed -= 1
                        elif sheep_needed > 0:
                            self.client.send_msg(BankTradeMessage(self.gamename,[0,ore_trade,0,0,0],[0,0,1,0,0]))
                            sheep_needed -= 1
                        elif wheat_needed > 0:
                            self.client.send_msg(BankTradeMessage(self.gamename,[0,ore_trade,0,0,0],[0,0,0,1,0]))
                            wheat_needed -= 1

                        ore_gives -= 1
                        left_to_trade -= 1

                    if wheat_gives > 0 and left_to_trade > 0:
                        if clay_needed > 0:
                            self.client.send_msg(BankTradeMessage(self.gamename,[0,0,0,wheat_trade,0],[1,0,0,0,0]))
                            clay_needed -= 1
                        elif wood_needed > 0:
                            self.client.send_msg(BankTradeMessage(self.gamename,[0,0,0,wheat_trade,0],[0,0,0,0,1]))
                            wood_needed -= 1
                        elif sheep_needed > 0:
                            self.client.send_msg(BankTradeMessage(self.gamename,[0,0,0,wheat_trade,0],[0,0,1,0,0]))
                            sheep_needed -= 1
                        elif wheat_needed > 0:
                            self.client.send_msg(BankTradeMessage(self.gamename,[0,0,0,wheat_trade,0],[0,0,0,1,0]))
                            wheat_needed -= 1

                        wheat_gives -= 1
                        left_to_trade -= 1
                    if sheep_gives > 0 and left_to_trade > 0:
                        if clay_needed > 0:
                            self.client.send_msg(BankTradeMessage(self.gamename,[0,0,sheep_trade,0,0],[1,0,0,0,0]))
                            clay_needed -= 1
                        elif wood_needed > 0:
                            self.client.send_msg(BankTradeMessage(self.gamename,[0,0,sheep_trade,0,0],[0,0,0,0,1]))
                            wood_needed -= 1
                        elif sheep_needed > 0:
                            self.client.send_msg(BankTradeMessage(self.gamename,[0,0,sheep_trade,0,0],[0,0,1,0,0]))
                            sheep_needed -= 1
                        elif wheat_needed > 0:
                            self.client.send_msg(BankTradeMessage(self.gamename,[0,0,sheep_trade,0,0],[0,0,0,1,0]))
                            wheat_needed -= 1

                        sheep_gives -= 1
                        left_to_trade -= 1

                    if wood_gives > 0 and left_to_trade > 0:
                        if clay_needed > 0:
                            self.client.send_msg(BankTradeMessage(self.gamename,[0,0,0,0,wood_trade],[1,0,0,0,0]))
                            clay_needed -= 1
                        elif wood_needed > 0:
                            self.client.send_msg(BankTradeMessage(self.gamename,[0,0,0,0,wood_trade],[0,0,0,0,1]))
                            wood_needed -= 1
                        elif sheep_needed > 0:
                            self.client.send_msg(BankTradeMessage(self.gamename,[0,0,0,0,wood_trade],[0,0,1,0,0]))
                            sheep_needed -= 1
                        elif wheat_needed > 0:
                            self.client.send_msg(BankTradeMessage(self.gamename,[0,0,0,0,wood_trade],[0,0,0,1,0]))
                            wheat_needed -= 1

                        wood_gives -= 1
                        left_to_trade -= 1

                    if clay_gives > 0 and left_to_trade > 0:
                        if clay_needed > 0:
                            self.client.send_msg(BankTradeMessage(self.gamename,[clay_trade,0,0,0,0],[1,0,0,0,0]))
                            clay_needed -= 1
                        elif wood_needed > 0:
                            self.client.send_msg(BankTradeMessage(self.gamename,[clay_trade,0,0,0,0],[0,0,0,0,1]))
                            wood_needed -= 1
                        elif sheep_needed > 0:
                            self.client.send_msg(BankTradeMessage(self.gamename,[clay_trade,0,0,0,0],[0,0,1,0,0]))
                            sheep_needed -= 1
                        elif wheat_needed > 0:
                            self.client.send_msg(BankTradeMessage(self.gamename,[clay_trade,0,0,0,0],[0,0,0,1,0]))
                            wheat_needed -= 1

                        clay_gives -= 1
                        left_to_trade -= 1

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
                left_to_trade = clay_needed + wood_needed

                while left_to_trade > 0:
                
                    if ore_gives > 0 and left_to_trade > 0:
                        if clay_needed > 0:
                            self.client.send_msg(BankTradeMessage(self.gamename,[0,ore_trade,0,0,0],[1,0,0,0,0]))
                            clay_needed -= 1
                        elif wood_needed > 0:
                            self.client.send_msg(BankTradeMessage(self.gamename,[0,ore_trade,0,0,0],[0,0,0,0,1]))
                            wood_needed -= 1

                        ore_gives -= 1
                        left_to_trade -= 1

                    if wheat_gives > 0 and left_to_trade > 0:
                        if clay_needed > 0:
                            self.client.send_msg(BankTradeMessage(self.gamename,[0,0,0,wheat_trade,0],[1,0,0,0,0]))
                            clay_needed -= 1
                        elif wood_needed > 0:
                            self.client.send_msg(BankTradeMessage(self.gamename,[0,0,0,wheat_trade,0],[0,0,0,0,1]))
                            wood_needed -= 1

                        wheat_gives -= 1
                        left_to_trade -= 1

                    if sheep_gives > 0 and left_to_trade > 0:
                        if clay_needed > 0:
                            self.client.send_msg(BankTradeMessage(self.gamename,[0,0,sheep_trade,0,0],[1,0,0,0,0]))
                            clay_needed -= 1
                        elif wood_needed > 0:
                            self.client.send_msg(BankTradeMessage(self.gamename,[0,0,sheep_trade,0,0],[0,0,0,0,1]))
                            wood_needed -= 1

                        sheep_gives -= 1
                        left_to_trade -= 1

                    if wood_gives > 0 and left_to_trade > 0:
                        if clay_needed > 0:
                            self.client.send_msg(BankTradeMessage(self.gamename,[0,0,0,0,wood_trade],[1,0,0,0,0]))
                            clay_needed -= 1
                        elif wood_needed > 0:
                            self.client.send_msg(BankTradeMessage(self.gamename,[0,0,0,0,wood_trade],[0,0,0,0,1]))
                            wood_needed -= 1

                        wood_gives -= 1
                        left_to_trade -= 1

                    if clay_gives > 0 and left_to_trade > 0:
                        if clay_needed > 0:
                            self.client.send_msg(BankTradeMessage(self.gamename,[clay_trade,0,0,0,0],[1,0,0,0,0]))
                            clay_needed -= 1
                        elif wood_needed > 0:
                            self.client.send_msg(BankTradeMessage(self.gamename,[clay_trade,0,0,0,0],[0,0,0,0,1]))
                            wood_needed -= 1

                        clay_gives -= 1
                        left_to_trade -= 1
                        
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
                left_to_trade = wheat_needed + ore_needed

                while left_to_trade > 0:
                
                    if ore_gives > 0 and left_to_trade > 0:
                        
                        if ore_needed > 0:
                            self.client.send_msg(BankTradeMessage(self.gamename,[0,ore_trade,0,0,0],[0,1,0,0,0]))
                            ore_needed -= 1
                        elif wheat_needed > 0:
                            self.client.send_msg(BankTradeMessage(self.gamename,[0,ore_trade,0,0,0],[0,0,0,1,0]))
                            wheat_needed -= 1

                        ore_gives -= 1
                        left_to_trade -= 1

                    if wheat_gives > 0 and left_to_trade > 0:

                        if ore_needed > 0:
                            self.client.send_msg(BankTradeMessage(self.gamename,[0,0,0,wheat_trade,0],[0,1,0,0,0]))
                            ore_needed -= 1
                        elif wheat_needed > 0:
                            self.client.send_msg(BankTradeMessage(self.gamename,[0,0,0,wheat_trade,0],[0,0,0,1,0]))
                            wheat_needed -= 1

                        wheat_gives -= 1
                        left_to_trade -= 1
                    if sheep_gives > 0 and left_to_trade > 0:

                        if ore_needed > 0:
                            self.client.send_msg(BankTradeMessage(self.gamename,[0,0,sheep_trade,0,0],[0,1,0,0,0]))
                            ore_needed -= 1
                        elif wheat_needed > 0:
                            self.client.send_msg(BankTradeMessage(self.gamename,[0,0,sheep_trade,0,0],[0,0,0,1,0]))
                            wheat_needed -= 1

                        sheep_gives -= 1
                        left_to_trade -= 1

                    if wood_gives > 0 and left_to_trade > 0:

                        if ore_needed > 0:
                            self.client.send_msg(BankTradeMessage(self.gamename,[0,0,0,0,wood_trade],[0,1,0,0,0]))
                            ore_needed -= 1
                        elif wheat_needed > 0:
                            self.client.send_msg(BankTradeMessage(self.gamename,[0,0,0,0,wood_trade],[0,0,0,1,0]))
                            wheat_needed -= 1

                        wood_gives -= 1
                        left_to_trade -= 1

                    if clay_gives > 0 and left_to_trade > 0:

                        if ore_needed > 0:
                            self.client.send_msg(BankTradeMessage(self.gamename,[clay_trade,0,0,0,0],[0,1,0,0,0]))
                            ore_needed -= 1
                        elif wheat_needed > 0:
                            self.client.send_msg(BankTradeMessage(self.gamename,[clay_trade,0,0,0,0],[0,0,0,1,0]))
                            wheat_needed -= 1

                        clay_gives -= 1
                        left_to_trade -= 1
                        
                return True

        return False
