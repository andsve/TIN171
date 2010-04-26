from messages import *

class Agent:
    def __init__(self, nickname, gamename, game, client):
        self.gamestate = 0 # 0 = not started, 1 = setup (settle placements), 2 = game running
        self.game = game
        self.gamename = gamename
        self.client = client
        self.nickname = nickname
        
        self.output_prefix = "[DEBUG] agent.py ->"
    
    def debug_print(self, msg):
        print "{0} {1}".format(self.output_prefix, msg)
    
    
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
                self.debug_print("We should place our settlements now!")
                # Try to build at pos 0x23!
                if (self.can_build_at_node(0x23)):
                    response = PutPieceMessage(self.gamename, self.playernum, 1, 0x23)
                    self.client.send_msg(response)
                else:
                    self.debug_print("Could not build at position 0x23!")
        #else:
            # Game is running!
            #print "LETS PLAY!"
        
        # DEBUG: 
        #if message:
        #    print "Agent: {0} - {1}".format(name, message.values())
    
    
    #
    # Auxiliary gameboard functions
    #
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
    
