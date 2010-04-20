class Agent:
    def __init__(self, nickname, game):
        self.gamestate = 0 # 0 = not started, 1 = setup (settle placements), 2 = game running
        self.game = game
        self.nickname = nickname
        
    # incomming messages from the message handler
    #  (i.e. alarms/signals/events from the game the agent needs to act on)
    def handle_message(self, name, message):
        
        if (name == "SitDownMessage" and message.nickname == self.nickname):
            print "THIS IS MEEEEEEEEEEEEE!"
        
        #if self.gamestate == 0:
        #    print "Game has not started yet, don't know what to do!"
        #elif self.gamestate == 1:
            # Setup state
            #aoe
        #else:
            # Game is running!
        #    print "LETS PLAY!"
        
        if message:
            print "Agent: {0} - {1}".format(name, message.values())
    
    
    #
    # Auxiliary gameboard functions
    #
    def can_build_at_node(self, node):
        # Returns 1 if it is possible to build a settlement at
        # this node, 0 otherwize.
        pass
    
    
    def resources_at_node(self, node):
        # Returns a list of resources for the specific node.
        pass
    
    
    def harbour_at_node(self, node):
        # Returns the type of harbour at the specific node,
        # returns 0 if the node isn't a harbour node.
        pass
    
    