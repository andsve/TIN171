from utils import cprint

class Planner:
    def __init__(self, game, resources, nodes, roads):

        self.game = game
        self.nodes = nodes
        self.roads = roads
        self.resources = resources

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

        self.scores = {}
        self.scores["WOOD"] = 1
        self.scores["CLAY"] = 1
        self.scores["SHEEP"] = 1
        self.scores["WHEAT"] = 1
        self.scores["ORE"] = 1
        self.scores["WOODH"] = 0
        self.scores["CLAYH"] = 0
        self.scores["SHEEPH"] = 0
        self.scores["WHEATH"] = 0
        self.scores["OREH"] = 0
        self.scores["3FOR1"] = 0.5

        self.output_prefix = "[DEBUG] planner.py ->"

    def debug_print(self, msg):
       cprint("{0} {1}".format(self.output_prefix, msg), 'yellow')


    def make_plan(self):

        # Determine what resources we are gaining
        for n in self.nodes:

            #if we already have a 3For1 harbor, lower the score for building a new one
            if self.game.boardLayout.nodes[n].harbor == 6:
                self.scores["3FOR1"] = 0.1

            #if we have a certain harbour, raise the score for that resource
            elif self.game.boardLayout.nodes[n].harbor == 1:
                self.scores["CLAY"] += 1
                
            elif self.game.boardLayout.nodes[n].harbor == 2:
                self.scores["ORE"] += 1

            elif self.game.boardLayout.nodes[n].harbor == 3:
                self.scores["SHEEP"] += 1

            elif self.game.boardLayout.nodes[n].harbor == 4:
                self.scores["WHEAT"] += 1
                
            elif self.game.boardLayout.nodes[n].harbor == 5:
                self.scores["WOOD"] += 1
           
            t1 = self.game.boardLayout.nodes[n].t1
            t2 = self.game.boardLayout.nodes[n].t2
            t3 = self.game.boardLayout.nodes[n].t3

            #if we have a settlement where we get a resource, lower the score for that resource
            #if we have a settlement where we get a resource, raise the score for that harbor
            #TODO: Account for cities
            if t1:
                if self.game.boardLayout.tiles[t1].resource == 1:
                    temp = self.probabilities[self.game.boardLayout.tiles[t1].number]
                    if temp:
                        self.scores["CLAY"] -= temp
                        self.scores["CLAYH"] += temp

                if self.game.boardLayout.tiles[t1].resource == 2:
                    temp = self.probabilities[self.game.boardLayout.tiles[t1].number]
                    if temp:
                        self.scores["ORE"] -= temp
                        self.scores["OREH"] += temp

                elif self.game.boardLayout.tiles[t1].resource == 3:
                    temp = self.probabilities[self.game.boardLayout.tiles[t1].number]
                    if temp:
                        self.scores["SHEEP"] -= temp
                        self.scores["SHEEPH"] += temp

                elif self.game.boardLayout.tiles[t1].resource == 4:
                    temp = self.probabilities[self.game.boardLayout.tiles[t1].number]
                    if temp:
                        self.scores["WHEAT"] -= temp
                        self.scores["WHEATH"] += temp
                        
                elif self.game.boardLayout.tiles[t1].resource == 5:
                    temp = self.probabilities[self.game.boardLayout.tiles[t1].number]
                    if temp:
                        self.scores["WOOD"] -= temp
                        self.scores["WOODH"] += temp

            if t2:
                if self.game.boardLayout.tiles[t2].resource == 1:
                    temp = self.probabilities[self.game.boardLayout.tiles[t2].number]
                    if temp:
                        self.scores["CLAY"] -= temp
                        self.scores["CLAYH"] += temp

                elif self.game.boardLayout.tiles[t2].resource == 2:
                    temp = self.probabilities[self.game.boardLayout.tiles[t2].number]
                    if temp:
                        self.scores["ORE"] -= temp
                        self.scores["OREH"] += temp

                elif self.game.boardLayout.tiles[t2].resource == 3:
                    temp = self.probabilities[self.game.boardLayout.tiles[t2].number]
                    if temp:
                        self.scores["SHEEP"] -= temp
                        self.scores["SHEEPH"] += temp

                elif self.game.boardLayout.tiles[t2].resource == 4:
                    temp = self.probabilities[self.game.boardLayout.tiles[t2].number]
                    if temp:
                        self.scores["WHEAT"] -= temp
                        self.scores["WHEATH"] += temp

                elif self.game.boardLayout.tiles[t2].resource == 5:
                    temp = self.probabilities[self.game.boardLayout.tiles[t2].number]
                    if temp:
                        self.scores["WOOD"] -= temp
                        self.scores["WOODH"] += temp
                    
            if t3:
                if self.game.boardLayout.tiles[t3].resource == 1:
                    temp = self.probabilities[self.game.boardLayout.tiles[t3].number]
                    if temp:
                        self.scores["CLAY"] -= temp
                        self.scores["CLAYH"] += temp

                elif self.game.boardLayout.tiles[t3].resource == 2:
                    temp = self.probabilities[self.game.boardLayout.tiles[t3].number]
                    if temp:
                        self.scores["ORE"] -= temp
                        self.scores["OREH"] += temp

                elif self.game.boardLayout.tiles[t3].resource == 3:
                    temp = self.probabilities[self.game.boardLayout.tiles[t3].number]
                    if temp:
                        self.scores["SHEEP"] -= temp
                        self.scores["SHEEPH"] += temp

                elif self.game.boardLayout.tiles[t3].resource == 4:
                    temp = self.probabilities[self.game.boardLayout.tiles[t3].number]
                    if temp:
                        self.scores["WHEAT"] -= temp
                        self.scores["WHEATH"] += temp

                elif self.game.boardLayout.tiles[t3].resource == 5:
                    temp = self.probabilities[self.game.boardLayout.tiles[t3].number]
                    if temp:
                        self.scores["WOOD"] -= temp
                        self.scores["WOODH"] += temp

        # determine score for possible settlement points close to any of our roads
        self.nodeScore = {}
        bestNode = None
        
        for r in self.roads:
            depth = 0

            self.calcNeighbourScore(r, depth)

        def cmp_fun(a,b):
            return int(b[1] - a[1])
      
        if len(self.nodeScore) > 0:

            tempList = sorted(self.nodeScore.items(), cmp=cmp_fun)
            (bestNode, score) = tempList[0]
            i = 1
            for item in tempList:
                (node,score) = item
                self.debug_print("{0}. {1} ({2})".format(i,hex(node),score))
                i += 1

        else:

            self.debug_print("No good spots found!")

        #find out how to build to that node
        if bestNode:

            self.debug_print("Best node at: {0}".format(hex(bestNode)))

            r1 = self.game.boardLayout.nodes[bestNode].n1
            r2 = self.game.boardLayout.nodes[bestNode].n2
            r3 = self.game.boardLayout.nodes[bestNode].n3

            self.debug_print("I am player {0}".format(self.game.playernum))

            if r1:
                self.debug_print("Road {0} belongs to: {1}".format(hex(r1), self.game.boardLayout.roads[r1].owner))

            if r2:
                self.debug_print("Road {0} belongs to: {1}".format(hex(r2), self.game.boardLayout.roads[r2].owner))

            if r3:
                self.debug_print("Road {0} belongs to: {1}".format(hex(r3), self.game.boardLayout.roads[r3].owner))

            if (r1 and self.game.boardLayout.roads[r1].owner and int(self.game.boardLayout.roads[r1].owner) == int(self.game.playernum)) or (r2 and self.game.boardLayout.roads[r2].owner and int(self.game.boardLayout.roads[r2].owner) == int(self.game.playernum)) or (r3 and self.game.boardLayout.roads[r3].owner and int(self.game.boardLayout.roads[r3].owner) == int(self.game.playernum)):
                if self.canAffordSettlement():
                    self.debug_print("Can build settlement, sending...")
                    return (bestNode, 1)
                else:
                    self.debug_print("Cannot afford settlement.")
                    self.debug_print("Wood: {0}".format(self.resources["WOOD"]))
                    self.debug_print("Clay: {0}".format(self.resources["CLAY"]))
                    self.debug_print("Sheep: {0}".format(self.resources["SHEEP"]))
                    self.debug_print("Wheat: {0}".format(self.resources["WHEAT"]))
                    return None

            tempList = []
            if r1:
                tempList.append(r1)
            if r2:
                tempList.append(r2)
            if r3:
                tempList.append(r3)
            if self.canAffordRoad():
                self.debug_print("Can build road, sending...")
                return self.findClosestBuildableRoad(tempList)
            else:
                self.debug_print("Cannot afford road.")
                self.debug_print("Wood: {0}".format(self.resources["WOOD"]))
                self.debug_print("Clay: {0}".format(self.resources["CLAY"]))
                return None
            
        else:
            return None
            
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
                tempScore = self.scores["3FOR1"]

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

            tempScore += (2 - depth)

            if n1 not in self.nodeScore or tempScore > self.nodeScore[n1]:
                self.nodeScore[n1] = tempScore
                
        #only look for settlement point maximum 2 roads away
        if depth < 2:
            r1 = self.game.boardLayout.nodes[n1].n1
            if r1 and self.game.boardLayout.roads[r1].owner == None:
                self.calcNeighbourScore(r1, depth + 1)
            r2 = self.game.boardLayout.nodes[n1].n2
            if r2 and self.game.boardLayout.roads[r2].owner == None:
                self.calcNeighbourScore(r2, depth + 1)
            r3 = self.game.boardLayout.nodes[n1].n3
            if r3 and self.game.boardLayout.roads[r3].owner == None:
                self.calcNeighbourScore(r3, depth + 1)

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
                tempScore = self.scores["3FOR1"]

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

            tempScore += (2 - depth)

            if n2 not in self.nodeScore or tempScore > self.nodeScore[n2]:
                self.nodeScore[n2] = tempScore

        #only look for settlement point maximum 2 roads away
        if depth < 2:
            r1 = self.game.boardLayout.nodes[n2].n1
            if r1 and self.game.boardLayout.roads[r1].owner == None:
                self.calcNeighbourScore(r1, depth + 1)
            r2 = self.game.boardLayout.nodes[n2].n2
            if r2 and self.game.boardLayout.roads[r2].owner == None:
                self.calcNeighbourScore(r2, depth + 1)
            r3 = self.game.boardLayout.nodes[n2].n3
            if r3 and self.game.boardLayout.roads[r3].owner == None:
                self.calcNeighbourScore(r3, depth + 1)

        return

    #finds the closest buildable road to a node
    def findClosestBuildableRoad(self, parents):

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
