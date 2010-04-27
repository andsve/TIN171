class Planner:
    def __init__(self, game, player, resources, nodes, roads):

        self.game = game
        self.player = player
        self.nodes = nodes
        self.roads = roads
        self.resources = resources

        #resources.LUMBER
        #resources.CLAY
        #resources.SHEEP
        #resources.GRAIN
        #resources.ORE

        self.scores = {}
        self.scores["LUMBER"] = 1
        self.scores["CLAY"] = 1
        self.scores["SHEEP"] = 1
        self.scores["GRAIN"] = 1
        self.scores["ORE"] = 1
        self.scores["LUMBERH"] = 0
        self.scores["CLAYH"] = 0
        self.scores["SHEEPH"] = 0
        self.scores["GRAINH"] = 0
        self.scores["OREH"] = 0
        self.scores["3FOR1"] = 1

        # Determine what resources we are gaining
        for n in nodes:

            #if we already have a 3For1 harbor, lower the score for building a new one
            if game.boardLayout.nodes[n].harbor == 6:
                self.scores["3FOR1"] == 0.1

            #if we have a certain harbour, raise the score for that resource
            elif game.boardLayout.nodes[n].harbor == 1:
                self.scores["LUMBER"] += 1

            elif game.boardLayout.nodes[n].harbor == 2:
                self.scores["CLAY"] += 1

            elif game.boardLayout.nodes[n].harbor == 3:
                self.scores["SHEEP"] += 1

            elif game.boardLayout.nodes[n].harbor == 4:
                self.scores["GRAIN"] += 1

            elif game.boardLayout.nodes[n].harbor == 5:
                self.scores["ORE"] += 1
           
            t1 = game.boardLayout.nodes[n].t1
            t2 = game.boardLayout.nodes[n].t2
            t3 = game.boardLayout.nodes[n].t3

            #if we have a settlement where we get a resource, lower the score for that resource
            #if we have a settlement where we get a resource, raise the score for that harbor
            #TODO: Account for cities
            if t1:
                if game.boardLayout.tiles[t1].resource == 1:
                    temp = numberProb(game.boardLayout.tiles[t1].number)
                    if temp:
                        self.scores["LUMBER"] -= temp
                        self.scores["LUMBERH"] += temp

                elif game.boardLayout.tiles[t1].resource == 2:
                    temp = numberProb(game.boardLayout.tiles[t1].number)
                    if temp:
                        self.scores["CLAY"] -= temp
                        self.scores["CLAYH"] += temp

                elif game.boardLayout.tiles[t1].resource == 3:
                    temp = numberProb(game.boardLayout.tiles[t1].number)
                    if temp:
                        self.scores["SHEEP"] -= temp
                        self.scores["SHEEPH"] += temp

                elif game.boardLayout.tiles[t1].resource == 4:
                    temp = numberProb(game.boardLayout.tiles[t1].number)
                    if temp:
                        self.scores["GRAIN"] -= temp
                        self.scores["GRAINH"] += temp
                    
                elif game.boardLayout.tiles[t1].resource == 5:
                    temp = numberProb(game.boardLayout.tiles[t1].number)
                    if temp:
                        self.scores["ORE"] -= temp
                        self.scores["OREH"] += temp

            if t2:
                if game.boardLayout.tiles[t2].resource == 1:
                    temp = numberProb(game.boardLayout.tiles[t2].number)
                    if temp:
                        self.scores["LUMBER"] -= temp
                        self.scores["LUMBERH"] += temp

                elif game.boardLayout.tiles[t2].resource == 2:
                    temp = numberProb(game.boardLayout.tiles[t2].number)
                    if temp:
                        self.scores["CLAY"] -= temp
                        self.scores["CLAYH"] += temp

                elif game.boardLayout.tiles[t2].resource == 3:
                    temp = numberProb(game.boardLayout.tiles[t2].number)
                    if temp:
                        self.scores["SHEEP"] -= temp
                        self.scores["SHEEPH"] += temp

                elif game.boardLayout.tiles[t2].resource == 4:
                    temp = numberProb(game.boardLayout.tiles[t2].number)
                    if temp:
                        self.scores["GRAIN"] -= temp
                        self.scores["GRAINH"] += temp
                    
                elif game.boardLayout.tiles[t2].resource == 5:
                    temp = numberProb(game.boardLayout.tiles[t2].number)
                    if temp:
                        self.scores["ORE"] -= temp
                        self.scores["OREH"] += temp

            if t3:
                if game.boardLayout.tiles[t3].resource == 1:
                    temp = numberProb(game.boardLayout.tiles[t3].number)
                    if temp:
                        self.scores["LUMBER"] -= temp
                        self.scores["LUMBERH"] += temp

                elif game.boardLayout.tiles[t3].resource == 2:
                    temp = numberProb(game.boardLayout.tiles[t3].number)
                    if temp:
                        self.scores["CLAY"] -= temp
                        self.scores["CLAYH"] += temp

                elif game.boardLayout.tiles[t3].resource == 3:
                    temp = numberProb(game.boardLayout.tiles[t3].number)
                    if temp:
                        self.scores["SHEEP"] -= temp
                        self.scores["SHEEPH"] += temp

                elif game.boardLayout.tiles[t3].resource == 4:
                    temp = numberProb(game.boardLayout.tiles[t3].number)
                    if temp:
                        self.scores["GRAIN"] -= temp
                        self.scores["GRAINH"] += temp
                    
                elif game.boardLayout.tiles[t3].resource == 5:
                    temp = numberProb(game.boardLayout.tiles[t3].number)
                    if temp:
                        self.scores["ORE"] -= temp
                        self.scores["OREH"] += temp

        # determine score for possible settlement points close to any of our roads
        self.nodeScore = {}
        
        for r in roads:
            depth = 0

            calcNeighbourScore(r, depth)

        def cmp_fun(a,b):
            return b[1] - a[1]

        (bestNode, score) = sorted(self.nodeScore.items(), cmp=cmp_fun)[0]

        #find out how to build to that node
        if bestNode:

            return findClosestBuildableRoad([bestNode])
            
        else:
            return None
            
    def canAffordRoad(self):

        return self.resources["LUMBER"] >= 1 and self.resources["CLAY"] >= 1

    def canAffordSettlement(self):

        return self.resources["LUMBER"] >= 1 and self.resources["CLAY"] >= 1 and self.resources["SHEEP"] >= 1 and self.resources["GRAIN"] >= 1

    def canAffordCity(self):

        return self.resources["GRAIN"] >= 2 and self.resources["ORE"] >= 3

    def numberProb(self, number):

        if number == 2 or number == 12:
            return 1/36.0

        elif number == 3 or number == 11:
            return 2/36.0

        elif number == 4 or number == 10:
            return 3/36.0

        elif number == 5 or number == 9:
            return 4/36.0

        elif number == 6 or number == 8:
            return 5/36.0

        elif number == 7:
            return 6/36.0

        else:
            return None
        
    def calcNeighbourScore(self, road, depth):

        n1 = self.game.boardLayout.roads[road].n1
        n2 = self.game.boardLayout.roads[road].n2

        if self.game.boardLayout.nodes[n1].owner == None:

            if self.game.boardLayout[n1].harbor == 1:
                tempScore = self.scores["LUMBERH"]

            elif self.game.boardLayout[n1].harbor == 2:
                tempScore = self.scores["CLAYH"]

            elif self.game.boardLayout[n1].harbor == 3:
                tempScore = self.scores["SHEEPH"]

            elif self.game.boardLayout[n1].harbor == 4:
                tempScore = self.scores["GRAINH"]

            elif self.game.boardLayout[n1].harbor == 5:
                tempScore = self.scores["OREH"]

            elif self.game.boardLayout[n1].harbor == 6:
                tempScore = self.scores["3FOR1H"]

            else:
                tempScore = 0
            
            t1 = self.game.boardLayout.nodes[n1].t1
            t2 = self.game.boardLayout.nodes[n1].t2
            t3 = self.game.boardLayout.nodes[n1].t3

            if t1 and self.game.boardLayout.tiles[t1].resource == 1:
                tempScore += self.scores["LUMBER"]
                if self.game.boardLayout[n1].harbor == 1:
                    tempScore += numberProb(self.game.boardLayout.tiles[t1].number)
                
            elif t1 and self.game.boardLayout.tiles[t1].resource == 2:
                tempScore += self.scores["CLAY"]
                if self.game.boardLayout[n1].harbor == 2:
                    tempScore += numberProb(self.game.boardLayout.tiles[t1].number)

            elif t1 and self.game.boardLayout.tiles[t1].resource == 3:
                tempScore += self.scores["SHEEP"]
                if self.game.boardLayout[n1].harbor == 3:
                    tempScore += numberProb(self.game.boardLayout.tiles[t1].number)

            elif t1 and self.game.boardLayout.tiles[t1].resource == 4:
                tempScore += self.scores["GRAIN"]
                if self.game.boardLayout[n1].harbor == 4:
                    tempScore += numberProb(self.game.boardLayout.tiles[t1].number)

            elif t1 and self.game.boardLayout.tiles[t1].resource == 5:
                tempScore += self.scores["ORE"]
                if self.game.boardLayout[n1].harbor == 5:
                    tempScore += numberProb(self.game.boardLayout.tiles[t1].number)

            if t2 and self.game.boardLayout.tiles[t2].resource == 1:
                tempScore += self.scores["LUMBER"]
                if self.game.boardLayout[n1].harbor == 1:
                    tempScore += numberProb(self.game.boardLayout.tiles[t2].number)
                
            elif t2 and self.game.boardLayout.tiles[t2].resource == 2:
                tempScore += self.scores["CLAY"]
                if self.game.boardLayout[n1].harbor == 2:
                    tempScore += numberProb(self.game.boardLayout.tiles[t2].number)

            elif t2 and self.game.boardLayout.tiles[t2].resource == 3:
                tempScore += self.scores["SHEEP"]
                if self.game.boardLayout[n1].harbor == 3:
                    tempScore += numberProb(self.game.boardLayout.tiles[t2].number)

            elif t2 and self.game.boardLayout.tiles[t2].resource == 4:
                tempScore += self.scores["GRAIN"]
                if self.game.boardLayout[n1].harbor == 4:
                    tempScore += numberProb(self.game.boardLayout.tiles[t2].number)

            elif t2 and self.game.boardLayout.tiles[t2].resource == 5:
                tempScore += self.scores["ORE"]
                if self.game.boardLayout[n1].harbor == 5:
                    tempScore += numberProb(self.game.boardLayout.tiles[t2].number)

            if t3 and self.game.boardLayout.tiles[t3].resource == 1:
                tempScore += self.scores["LUMBER"]
                if self.game.boardLayout[n1].harbor == 1:
                    tempScore += numberProb(self.game.boardLayout.tiles[t3].number)
                
            elif t3 and self.game.boardLayout.tiles[t3].resource == 2:
                tempScore += self.scores["CLAY"]
                if self.game.boardLayout[n1].harbor == 2:
                    tempScore += numberProb(self.game.boardLayout.tiles[t3].number)

            elif t3 and self.game.boardLayout.tiles[t3].resource == 3:
                tempScore += self.scores["SHEEP"]
                if self.game.boardLayout[n1].harbor == 3:
                    tempScore += numberProb(self.game.boardLayout.tiles[t3].number)

            elif t3 and self.game.boardLayout.tiles[t3].resource == 4:
                tempScore += self.scores["GRAIN"]
                if self.game.boardLayout[n1].harbor == 4:
                    tempScore += numberProb(self.game.boardLayout.tiles[t3].number)

            elif t3 and self.game.boardLayout.tiles[t3].resource == 5:
                tempScore += self.scores["ORE"]
                if self.game.boardLayout[n1].harbor == 5:
                    tempScore += numberProb(self.game.boardLayout.tiles[t3].number)

            tempScore += 2 - depth

            if n1 not in self.nodeScore or tempScore > self.nodeScore[n1]:
                self.nodeScore[n1] = tempScore

            if depth <= 1:
                r1 = self.game.boardLayout.nodes[n1].n1
                if r1:
                    calcNeighbourScore(r1, depth + 1)
                r2 = self.game.boardLayout.nodes[n1].n2
                if r2:
                    calcNeighbourScore(r2, depth + 1)
                r3 = self.game.boardLayout.nodes[n1].n3
                if r3:
                    calcNeighbourScore(r3, depth + 1)

        if self.game.boardLayout.nodes[n2].owner == None:
            
            if self.game.boardLayout[n2].harbor == 1:
                tempScore = self.scores["LUMBERH"]

            elif self.game.boardLayout[n2].harbor == 2:
                tempScore = self.scores["CLAYH"]

            elif self.game.boardLayout[n2].harbor == 3:
                tempScore = self.scores["SHEEPH"]

            elif self.game.boardLayout[n2].harbor == 4:
                tempScore = self.scores["GRAINH"]

            elif self.game.boardLayout[n2].harbor == 5:
                tempScore = self.scores["OREH"]

            elif self.game.boardLayout[n2].harbor == 6:
                tempScore = self.scores["3FOR1H"]

            else:
                tempScore = 0
            
            t1 = self.game.boardLayout.nodes[n2].t1
            t2 = self.game.boardLayout.nodes[n2].t2
            t3 = self.game.boardLayout.nodes[n2].t3

            if t1 and self.game.boardLayout.tiles[t1].resource == 1:
                tempScore += self.scores["LUMBER"]
                if self.game.boardLayout[n2].harbor == 1:
                    tempScore += numberProb(self.game.boardLayout.tiles[t1].number)
                
            elif t1 and self.game.boardLayout.tiles[t1].resource == 2:
                tempScore += self.scores["CLAY"]
                if self.game.boardLayout[n2].harbor == 2:
                    tempScore += numberProb(self.game.boardLayout.tiles[t1].number)

            elif t1 and self.game.boardLayout.tiles[t1].resource == 3:
                tempScore += self.scores["SHEEP"]
                if self.game.boardLayout[n2].harbor == 3:
                    tempScore += numberProb(self.game.boardLayout.tiles[t1].number)

            elif t1 and self.game.boardLayout.tiles[t1].resource == 4:
                tempScore += self.scores["GRAIN"]
                if self.game.boardLayout[n2].harbor == 4:
                    tempScore += numberProb(self.game.boardLayout.tiles[t1].number)

            elif t1 and self.game.boardLayout.tiles[t1].resource == 5:
                tempScore += self.scores["ORE"]
                if self.game.boardLayout[n2].harbor == 5:
                    tempScore += numberProb(self.game.boardLayout.tiles[t1].number)

            if t2 and self.game.boardLayout.tiles[t2].resource == 1:
                tempScore += self.scores["LUMBER"]
                if self.game.boardLayout[n2].harbor == 1:
                    tempScore += numberProb(self.game.boardLayout.tiles[t2].number)
                
            elif t2 and self.game.boardLayout.tiles[t2].resource == 2:
                tempScore += self.scores["CLAY"]
                if self.game.boardLayout[n2].harbor == 2:
                    tempScore += numberProb(self.game.boardLayout.tiles[t2].number)

            elif t2 and self.game.boardLayout.tiles[t2].resource == 3:
                tempScore += self.scores["SHEEP"]
                if self.game.boardLayout[n2].harbor == 3:
                    tempScore += numberProb(self.game.boardLayout.tiles[t2].number)

            elif t2 and self.game.boardLayout.tiles[t2].resource == 4:
                tempScore += self.scores["GRAIN"]
                if self.game.boardLayout[n2].harbor == 4:
                    tempScore += numberProb(self.game.boardLayout.tiles[t2].number)

            elif t2 and self.game.boardLayout.tiles[t2].resource == 5:
                tempScore += self.scores["ORE"]
                if self.game.boardLayout[n2].harbor == 5:
                    tempScore += numberProb(self.game.boardLayout.tiles[t2].number)

            if t3 and self.game.boardLayout.tiles[t3].resource == 1:
                tempScore += self.scores["LUMBER"]
                if self.game.boardLayout[n2].harbor == 1:
                    tempScore += numberProb(self.game.boardLayout.tiles[t3].number)
                
            elif t3 and self.game.boardLayout.tiles[t3].resource == 2:
                tempScore += self.scores["CLAY"]
                if self.game.boardLayout[n2].harbor == 2:
                    tempScore += numberProb(self.game.boardLayout.tiles[t3].number)

            elif t3 and self.game.boardLayout.tiles[t3].resource == 3:
                tempScore += self.scores["SHEEP"]
                if self.game.boardLayout[n2].harbor == 3:
                    tempScore += numberProb(self.game.boardLayout.tiles[t3].number)

            elif t3 and self.game.boardLayout.tiles[t3].resource == 4:
                tempScore += self.scores["GRAIN"]
                if self.game.boardLayout[n2].harbor == 4:
                    tempScore += numberProb(self.game.boardLayout.tiles[t3].number)

            elif t3 and self.game.boardLayout.tiles[t3].resource == 5:
                tempScore += self.scores["ORE"]
                if self.game.boardLayout[n2].harbor == 5:
                    tempScore += numberProb(self.game.boardLayout.tiles[t3].number)

            tempScore += 2 - depth

            if n2 not in self.nodeScore or tempScore > self.nodeScore[n2]:
                self.nodeScore[n2] = tempScore

            #only look for settlement point maximum 2 roads away
            if depth < 2:
                r1 = self.game.boardLayout.nodes[n2].n1
                if r1 and self.game.boardLayout.roads[r1].owner == None:
                    calcNeighbourScore(r1, depth + 1)
                r2 = self.game.boardLayout.nodes[n2].n2
                if r2 and self.game.boardLayout.roads[r2].owner == None:
                    calcNeighbourScore(r2, depth + 1)
                r3 = self.game.boardLayout.nodes[n2].n3
                if r3 and self.game.boardLayout.roads[r3].owner == None:
                    calcNeighbourScore(r3, depth + 1)

    #finds the closest buildable road to a node
    def findClosestBuildableRoad(self, parents):

        for p in parents:

            r1 = self.game.boardLayout.nodes[p].n1
            r2 = self.game.boardLayout.nodes[p].n2
            r3 = self.game.boardLayout.nodes[p].n3

            if (r1 and self.game.boardLayout.roads[r1].owner == self.player) or (r2 and self.game.boardLayout.roads[r2].owner == self.player) or (r3 and self.game.boardLayout.roads[r3].owner == self.player):
                return (p, 1)

            if r1 and self.game.boardLayout.roads[r1].owner == None:
                n1 = self.game.boardLayout.roads[r1].n1
                n2 = self.game.boardLayout.roads[r1].n2

                if n1 not in parents:
                    parents.append(n1)

                if n2 not in parents:
                    parents.append(n2)

            if r2 and self.game.boardLayout.roads[r2].owner == None:
                n1 = self.game.boardLayout.roads[r2].n1
                n2 = self.game.boardLayout.roads[r2].n2

                if n1 not in parents:
                    parents.append(n1)

                if n2 not in parents:
                    parents.append(n2)

            if r3 and self.game.boardLayout.roads[r3].owner == None:
                n1 = self.game.boardLayout.roads[r3].n1
                n2 = self.game.boardLayout.roads[r3].n2

                if n1 not in parents:
                    parents.append(n1)

                if n2 not in parents:
                    parents.append(n2)

        return findClosestBuildableRoad(self, parents)
