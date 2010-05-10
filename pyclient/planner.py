from utils import cprint
from messages import *
import copy
import logging

class Planner:
    def __init__(self, game, stats, gamename, resources, nodes, roads, client, bought):

        self.game = game
        self.gamename = gamename
        self.stats = stats
        self.nodes = nodes
        self.roads = roads
        self.resources = resources
        self.client = client
        self.bought = bought

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
             "WOOD":   3
            ,"CLAY":   3
            ,"SHEEP":  3
            ,"WHEAT":  3
            ,"ORE":    3
            ,"WOODH":  0
            ,"CLAYH":  0
            ,"SHEEPH": 0
            ,"WHEATH": 0
            ,"OREH":   0
            ,"3FOR1H": 2
        }

        self.resource_list = [0,0,0,0,0,0]
        
        self.scores = {}

        self.longest_start = None
        self.longest_end = None
        self.longest_length = 0
        
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
    
    def make_plan(self, road_card):
        from jsettlers_utils import  elementIdToType, pieceToType
        self.scores = copy.deepcopy(self.default_scores)

        (self.longest_start, self.longest_end, self.longest_length) = self.find_longest_road()
        
        # Determine what resources we are gaining
        for n in self.nodes:
            node = self.game.boardLayout.nodes[n]
            
            # If we have a certain harbour, raise the score for that resource
            if 0 < node.harbor < 6:
                self.add_resource_score(node.harbor, 3)
                
            # If we have a 3 for 1 harbour: lower the score for building a new one
            elif node.harbor == 6:
                self.set_harbour_score(node.harbor, 0)
                
            tiles = [self.game.boardLayout.tiles[t] for t in [node.t1, node.t2, node.t3] if t != None]

            city_bonus = 1
            if node.type == 2:
                city_bonus = 2
            
            #if we have a settlement where we get a resource, lower the score for that resource
            #if we have a settlement where we get a resource, raise the score for that harbor.
            for tile in tiles:
                if 0 < tile.resource < 6:
                    self.resource_list[tile.resource] = 1
                    res_name  = elementIdToType[str(tile.resource)]
                    score_mod = self.probabilities.setdefault(tile.number, 0) * city_bonus
                    self.add_resource_score(tile.resource, -8 * score_mod)
                    self.add_harbour_score(tile.resource, 10*score_mod)
           
        possible_roads = []
        possible_roads += self.roads
        buildable_roads = self.game.buildableRoads.roads
        for r in buildable_roads:
            if buildable_roads[r] and r not in possible_roads:
                possible_roads.append(r)

        self.nodeScore = {} 
        logging.info("Possible roads: {0}".format(map(hex, possible_roads)))
        for r in possible_roads:
            self.calcNeighbourScore(r, 0, 0)

        best_node = None
        best_score = 0
        if len(self.nodeScore) > 0:
            tempList = sorted(self.nodeScore.items(), cmp=lambda a,b: int(1000*b[1]) - int(1000*a[1]))
            (best_pos, best_score) = tempList[0]
            best_node = self.game.boardLayout.nodes[best_pos]
            for i, item in enumerate(tempList):
                (node,score) = item
                self.debug_print("{0}. {1} ({2})".format(i,hex(node),score))
        else:
            self.debug_print("No good spots found!")      

        # Find out how to build to that node
        if best_node and ((road_card or self.resources["SETTLEMENTS"] > 0) and (best_score >= 3.5 or self.resources["SETTLEMENTS"] >= 4)):
            self.debug_print("Best location: {0}".format(hex(best_node.id)))
            
            roads = [self.game.boardLayout.roads[r] for r in [best_node.n1, best_node.n2, best_node.n3] if r != None]
            for road in roads:
                self.debug_print("Road {0} belongs to: {1}".format(road.id, road.owner))

            if not road_card and any(r.owner and int(r.owner) == int(self.game.playernum) for r in roads):
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

            elif not any(r.owner and int(r.owner) == int(self.game.playernum) for r in roads):
                if road_card or (self.resources["ROADS"] > 0 and self.canAffordRoad()):
                    self.debug_print("Can build road, sending...")
                    return self.findClosestBuildableRoad([road.id for road in roads], 0)
                elif self.resources["ROADS"] > 0 and self.canAffordWithTrade(0):
                    self.debug_print("Can afford road after trade...")
                    return self.findClosestBuildableRoad([road.id for road in roads], 0)
                else:
                    self.debug_print("Cannot afford road.")
                    self.debug_print("Wood: {0}".format(self.resources["WOOD"]))
                    self.debug_print("Clay: {0}".format(self.resources["CLAY"]))                

        # Cannot afford settlement and shouldn't/cannot build road. Try upgrading to city.

        if not road_card and self.resources["CITIES"] > 0:
            self.cityScore = {}

            for n in self.nodes:
                node = self.game.boardLayout.nodes[n]
                if node.type == 1:

                    temp_score = 0
                    
                    tiles = [self.game.boardLayout.tiles[t] for t in [node.t1, node.t2, node.t3] if t != None]
                    
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
                        self.debug_print("Can afford city after trade...")
                        return (bestNode, 2)
                    else:
                        self.debug_print("Cannot afford city.")
                        self.debug_print("Wheat: {0}".format(self.resources["WHEAT"]))
                        self.debug_print("Ore: {0}".format(self.resources["ORE"]))

        # try and build to build the longest road
        tempLongestRoad = 0
        tempRoad = None
        tempRoad2 = None
        if road_card or (self.resources["ROADS"] > 0 and self.resources["SETTLEMENTS"] <= 4 and self.resources["SETTLEMENTS"] + self.resources["CITIES"] <= 5 and self.canAffordRoad()):
            self.debug_print("Try to connect settlement hubs.")
            for road in self.game.buildableRoads.roads:
                for road2 in self.game.buildableRoads.roads:
                    if self.game.buildableRoads.roads[road] and self.game.buildableRoads.roads[road2]:
                        #self.debug_print("Changing owner for: {0} and {1}".format(hex(road),hex(road2)))
                        self.game.boardLayout.roads[road].owner = int(self.game.playernum)
                        self.game.boardLayout.roads[road2].owner = int(self.game.playernum)

                        (start, end, tempLength) = self.find_longest_road()

                        self.game.boardLayout.roads[road].owner = None
                        self.game.boardLayout.roads[road2].owner = None

                        if tempLength > self.longest_length and tempLength > tempLongestRoad:
                            tempLongestRoad = tempLength
                            tempRoad = road
                            tempRoad2 = road2
                            self.debug_print("Found a connection by {0} and {1}.".format(hex(road),hex(road2)))

        if tempLongestRoad > self.longest_length:

            self.game.boardLayout.roads[tempRoad].owner = int(self.game.playernum)
            (tempStart, tempEnd, tempLength) = self.find_longest_road()
            self.game.boardLayout.roads[tempRoad].owner = None
            self.game.boardLayout.roads[tempRoad2].owner = int(self.game.playernum)
            (tempStart, tempEnd, tempLength2) = self.find_longest_road()
            self.game.boardLayout.roads[tempRoad2].owner = None

            if tempLength >= tempLength2:
                return (tempRoad, 0)

            return(tempRoad2, 0)
            
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

    def canAffordCard(self):
        return self.resources["WHEAT"] >= 1 and self.resources["ORE"] >= 1 and self.resources["SHEEP"] >= 1
    
    def is_road_buildable(self, road):
        n1 = self.game.boardLayout.roads[road].n1
        n2 = self.game.boardLayout.roads[road].n2
        #check if the road is actually unbuildable due to an enemy settlement
        notMine =  (self.game.boardLayout.nodes[n1].owner != None and int(self.game.boardLayout.nodes[n1].owner) != int(self.game.playernum)) \
                or (self.game.boardLayout.nodes[n2].owner != None and int(self.game.boardLayout.nodes[n2].owner) != int(self.game.playernum))
        if road in self.game.buildableRoads.roads and notMine:
            return False
        return True

    def calcNeighbourScore(self, road, depth, i_l):
        
        n1 = self.game.boardLayout.roads[road].n1
        n2 = self.game.boardLayout.roads[road].n2
        road_node = self.game.boardLayout.roads[road]

        increase_longest = i_l

        if increase_longest == 0 and (self.longest_length == 1 or self.increases_longest(road)):
            increase_longest = 2

        if not self.is_road_buildable(road):
            return None
        
        for n in [n1, n2]:            
            node = self.game.boardLayout.nodes[n]
            is_buildable = self.game.buildableNodes.nodes[n]
            if is_buildable:
                if 0 < node.harbor < 7:
                    temp_score = self.get_harbour_score(node.harbor)
                else:
                    temp_score = 0

                temp_score += increase_longest
                
                tiles = [self.game.boardLayout.tiles[t] for t in [node.t1, node.t2, node.t3] if t != None]
                for tile in tiles:
                    if 0 < tile.resource < 6:
                        # Add resource score for all resource types
                        temp_score += self.get_resource_score(tile.resource)
                        # Add bonus if we are not getting that resource
                        temp_score += (1 - self.resource_list[tile.resource]) * 5

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
                    if r.owner == None and not ((self.game.boardLayout.nodes[r.n1].owner != None and int(self.game.boardLayout.nodes[r.n1].owner) != int(self.game.playernum)) or (self.game.boardLayout.nodes[r.n2].owner != None and int(self.game.boardLayout.nodes[r.n2].owner) != int(self.game.playernum))):
                        self.calcNeighbourScore(r.id, depth + d, increase_longest)
                
        return None

    #finds the closest buildable road to a node
    def findClosestBuildableRoad(self, parents, depth):
        self.debug_print("depth: {0}".format(depth))
        self.debug_print("parents: {0}".format(parents))

        import copy

        tempParents = [r for r in copy.deepcopy(parents) if self.is_road_buildable(r)]

        if depth > 3:
            return None
                         
        for r in tempParents:

            if self.game.buildableRoads.roads[r] and self.increases_longest(r):
                return(r,0)

        for r in tempParents:

            if self.game.buildableRoads.roads[r]:
                return(r,0)
            
        for r in tempParents:

            if depth < 3 and self.game.boardLayout.roads[r].owner == None:

                n1 = self.game.boardLayout.roads[r].n1
                n2 = self.game.boardLayout.roads[r].n2

                r1 = self.game.boardLayout.nodes[n1].n1
                r2 = self.game.boardLayout.nodes[n1].n2
                r3 = self.game.boardLayout.nodes[n1].n3

                if r1 and r1 not in parents:
                    parents.append(r1)
                if r2 and r2 not in parents:
                    parents.append(r2)
                if r3 and r3 not in parents:
                    parents.append(r3)

                r1 = self.game.boardLayout.nodes[n2].n1
                r2 = self.game.boardLayout.nodes[n2].n2
                r3 = self.game.boardLayout.nodes[n2].n3

                if r1 and r1 not in parents:
                    parents.append(r1)
                if r2 and r2 not in parents:
                    parents.append(r2)
                if r3 and r3 not in parents:
                    parents.append(r3)

        return self.findClosestBuildableRoad(parents, depth + 1)

    def canAffordWithTrade(self,_type):

        trade_cost = { "WOOD": 4
                     , "CLAY": 4
                     , "WHEAT": 4
                     , "SHEEP": 4
                     , "ORE": 4
                     , "3FOR1": 4}

        # Update trade_costs depending on what type of harbours we have access to.
        for n in self.nodes:
            node = self.game.boardLayout.nodes[n]
            if 0 < node.harbor < 7:
                htype = self.get_resource_name(node.harbor, True)
                rtype = htype[0:-1]
                logging.info("Found {0} harbour".format(htype))
                
                if rtype == "3FOR1":
                    trade_cost[rtype] = 3
                else:
                    trade_cost[rtype] = 2

        # Access to a 3 for 1 harbour will lower the costs for some resources
        for k,v in trade_cost.items():
            trade_cost[k] = min(v, trade_cost["3FOR1"])

        if _type == 0:
            self.debug_print("Trying to trade for road...")
            needed_resources = set(("CLAY", "WOOD"))
            needed_count = {"CLAY": 1, "WOOD": 1}
            
        elif _type == 1:
            self.debug_print("Trying to trade for settlement...")
            needed_resources = set(("CLAY", "SHEEP", "WHEAT", "WOOD"))
            needed_count = {"CLAY": 1, "SHEEP": 1, "WHEAT": 1, "WOOD": 1}
            
        elif _type == 2:
            self.debug_print("Trying to trade for city...")
            needed_resources = set(("WHEAT", "ORE"))
            needed_count = {"WHEAT": 2, "ORE": 3}
        elif _type == 3:
            self.debug_print("Trying to trade for development card...")
            needed_resources = set(("WHEAT", "SHEEP", "ORE"))
            needed_count = {"WHEAT": 1, "SHEEP": 1, "ORE": 1}            
        
        gives = {}
        needed = {}
        given_resources = set(("CLAY", "ORE", "SHEEP", "WHEAT", "WOOD"))
        
        # If we don't have any settlements left to build, don't trade wheat and ore
        keep = set()
        if self.resources["SETTLEMENTS"] == 0:
            keep = set(("WHEAT", "ORE"))
#            given_resources = given_resources - set(("WHEAT", "ORE"))
#            needed_resources = needed_resources - set(("WHEAT", "ORE"))
#        given_resources = given_resources - keep
        
        for resource in needed_resources:
            needed[resource] = max(0, needed_count[resource] - self.resources[resource])
            
        for resource in needed_resources:
            gives[resource] = max(0, self.resources[resource] - needed_count[resource]) / min(trade_cost[resource], trade_cost["3FOR1"], 4)
        for resource in given_resources - needed_resources - keep:
            gives[resource] = self.resources[resource] / min(trade_cost[resource], trade_cost["3FOR1"], 4)

        for resource in keep:
            gives[resource] = 0

        logging.info("Needed..: {0}".format(", ".join("{0}: {1}".format(k,v) for k,v in needed.items())))
        logging.info("Can give: {0}".format(", ".join(given_resources)))
        logging.info("Gives...: {0}".format(", ".join("{0}: {1}".format(k,v) for k,v in gives.items())))

        resource_card = 0
        if self.resources["RESOURCE_CARDS"] > 0 and self.resources["MAY_PLAY_DEVCARD"] and sum(needed.values()) >= 2 and not self.bought["resourcecard"]:
            self.debug_print("May play devcard: {0} (1)".format(self.resources["MAY_PLAY_DEVCARD"]))
            logging.info("Got Resource Card")
            resource_card = 0 # change to 2 when message is implemented

        if sum(gives.values()) >= sum(needed.values()) - resource_card:
            def get_resource_index(name):
                rlist = ("CLAY", "ORE", "SHEEP", "WHEAT", "WOOD")
                for i, n in enumerate(rlist):
                    if n == name:
                        return i
                                            
            # use resource card here to get two needed resources
            if resource_card == 2:
                resources = [0, 0, 0, 0, 0]
                while sum(resources) < 2:
                    for r,v in needed.items():
                        ri = get_resource_index(r)
                        if v > 0:
                            resources[ri] += 1
                            needed[r] -= 1
                logging.critical("Picking some resources.")
                self.debug_print("May play devcard: {0} (2)".format(self.resources["MAY_PLAY_DEVCARD"]))
                self.client.send_msg(PlayDevCardRequestMessage(self.gamename, 2))
                self.resources["MAY_PLAY_DEVCARD"] = False
                self.client.send_msg(DiscoveryPickMessage(self.gamename, resources))
                    
            
            left_to_trade = sum(needed.values())

            max_iterations = 10
            num_iterations = 0
            while left_to_trade > 0:
                if num_iterations > max_iterations:
                    logging.critical("WOOPSIE: Terminating loop.")
                    logging.critical("gives: {0}".format(gives))
                    logging.critical("needed: {0}".format(needed))
                    logging.critical("given_resources: {0}".format(given_resources))
                    logging.critical("needed_resources: {0}".format(needed_resources))
                    return False
                    
                for gres in given_resources:
                    if gives[gres] > 0 and left_to_trade > 0:
                        for nres in needed_resources:
                            if needed[nres] > 0 and left_to_trade > 0:
                                give = [0, 0, 0, 0, 0]
                                get  = [0, 0, 0, 0, 0]
                                give[get_resource_index(gres)] = trade_cost[gres]
                                get[get_resource_index(nres)] = 1

                                self.client.send_msg(BankTradeMessage(self.gamename, give, get))
                                needed[nres] -= 1
                                break
                        gives[gres] -= 1
                        left_to_trade -= 1
                num_iterations += 1
            return True
        return False

    def find_longest_road(self):

        import copy

        longest = []

        for r in self.roads:

            temp = self.longest_path([r])

            if len(temp) > len(longest):
                longest = copy.deepcopy(temp)

        return(longest[0], longest[-1], len(longest))

    def longest_path(self, visited):

        import copy

        r = visited[-1]

        nodes = [self.game.boardLayout.roads[r].n1,self.game.boardLayout.roads[r].n2]
        longest = copy.deepcopy(visited)
       
        for n in nodes:

            if self.game.boardLayout.nodes[n].owner == None or self.game.boardLayout.nodes[n].owner == int(self.game.playernum):

                if self.game.boardLayout.nodes[n].n1 and self.game.boardLayout.nodes[n].n1 not in visited and self.game.boardLayout.roads[self.game.boardLayout.nodes[n].n1].owner == int(self.game.playernum):
                    new_visited = copy.deepcopy(visited)
                    new_visited.append(self.game.boardLayout.nodes[n].n1)
                    temp = self.longest_path(new_visited)

                    if len(temp) > len(longest):
                        longest = copy.deepcopy(temp)

                if self.game.boardLayout.nodes[n].n2 and self.game.boardLayout.nodes[n].n2 not in visited and self.game.boardLayout.roads[self.game.boardLayout.nodes[n].n2].owner == int(self.game.playernum):
                    new_visited = copy.deepcopy(visited)
                    new_visited.append(self.game.boardLayout.nodes[n].n2)
                    temp = self.longest_path(new_visited)

                    if len(temp) > len(longest):
                        longest = copy.deepcopy(temp)

                if self.game.boardLayout.nodes[n].n3 and self.game.boardLayout.nodes[n].n3 not in visited and self.game.boardLayout.roads[self.game.boardLayout.nodes[n].n3].owner == int(self.game.playernum):
                    new_visited = copy.deepcopy(visited)
                    new_visited.append(self.game.boardLayout.nodes[n].n3)
                    temp = self.longest_path(new_visited)

                    if len(temp) > len(longest):
                        longest = copy.deepcopy(temp)

        return longest

    def increases_longest(self, road):
        
        temp = self.longest_path([road])

        if len(temp) >= self.longest_length:
            return True

        return False
        
