class Agent:
    def __init__(self, game):
        self.game = game
        
    def handle_message(self, name, message):
        if message:
            print "Agent: {0} - {1}".format(name, message.values())
        