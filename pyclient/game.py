from messages import *

class Game:
    def __init__(self):
        # Initiate gameboard when the message is recieved?
        #self.gameboard = gameboard # save raw gameboad
        #self.parse_board()         # parse gameboard and create internal representation
        self.messagetbl = {}
        self.init_parser()
    
    def init_parser(self):
        """ Create a LUT for message id => message instance """
        self.messagetbl = {}
        for g in globals():
            cg = globals()[g]
            if str(g).endswith("Message") and hasattr(cg, "id"):
                self.messagetbl[str(cg.id)] = (cg, g)
    
    def parse_message(self, msg):
        """ Create a message from recieved data """
        id, txt = msg[:4], msg[5:]
        message_class, name = self.messagetbl[id]
        inst = message_class.parse(txt)
        self.update_game(name, inst)
        return (name, inst)
        
    def update_game(self, id, message):
        """ Update game state """
        
        # Look up how the data is exposed by matching the id with the
        # message-classes listed below. Some of them will need some tweaking
        # (i.e.BankTradeMessage - must map Jsettlers resource id -> resource name)
        
        if id == "BoardLayoutMessage":
            # Set game board
            self.boardLayout = BoardLayout()

            # Add resource to all neighbours
            if message.board[5] != 0:
             """self.boardLayout[ord('\x27')].addResource(message.board[5])
                self.boardLayout[ord('\x36')].addResource(message.board[5])
                self.boardLayout[ord('\x38')].addResource(message.board[5])
                self.boardLayout[ord('\x47')].addResource(message.board[5])
                self.boardLayout[ord('\x49')].addResource(message.board[5])
                self.boardLayout[ord('\x58')].addResource(message.board[5])"""
            
            pass               
            
        elif id == "PlayerElementMessage":
            # Update resources
            pass
            
    
    def parse_board(self):
        for elt in self.gameboard:
            print(elt)
            #pass # TODO: parse the gameboard information sent by the server

class RoadNode:
    def __init__(self, name, neighbour1, neighbour2):
        self.id = name
        self.n1 = neighbour1
        self.n2 = neighbour2
        self.owner = None

class BoardNode:
    def __init__(self, name, neighbour1, neighbour2, neighbour3):
        self.id = name
        self.n1 = neighbour1
        self.n2 = neighbour2
        self.n3 = neighbour3
        self.harbor = None
        self.resource1 = None
        self.resource2 = None
        self.resource3 = None

class BoardLayout:
    # Static look-up tables
    roadLUT = {
         '\x22': RoadNode('\x22','\x23','\x32')
        ,'\x23': RoadNode('\x23','\x23','\x34')
        ,'\x24': RoadNode('\x24','\x25','\x34')
        ,'\x25': RoadNode('\x25','\x25','\x36')
        ,'\x26': RoadNode('\x26','\x27','\x36')
        ,'\x27': RoadNode('\x27','\x27','\x38')
        ,'\x32': RoadNode('\x32','\x32','\x43')
        ,'\x34': RoadNode('\x34','\x34','\x45')
        ,'\x36': RoadNode('\x36','\x36','\x47')
        ,'\x38': RoadNode('\x38','\x38','\x49')
        ,'\x42': RoadNode('\x42','\x43','\x52')
        ,'\x43': RoadNode('\x43','\x43','\x54')
        ,'\x44': RoadNode('\x44','\x45','\x54')
        ,'\x45': RoadNode('\x45','\x45','\x56')
        ,'\x46': RoadNode('\x46','\x47','\x56')
        ,'\x47': RoadNode('\x47','\x47','\x58')
        ,'\x48': RoadNode('\x48','\x49','\x58')
        ,'\x49': RoadNode('\x49','\x49','\x5a')
        ,'\x52': RoadNode('\x52','\x52','\x63')
        ,'\x54': RoadNode('\x54','\x54','\x65')
        ,'\x56': RoadNode('\x56','\x56','\x67')
        ,'\x58': RoadNode('\x58','\x58','\x69')
        ,'\x5a': RoadNode('\x5a','\x5a','\x6b')
        ,'\x62': RoadNode('\x62','\x63','\x72')
        ,'\x63': RoadNode('\x63','\x63','\x74')
        ,'\x64': RoadNode('\x64','\x65','\x74')
        ,'\x65': RoadNode('\x65','\x65','\x76')
        ,'\x66': RoadNode('\x66','\x67','\x76')
        ,'\x67': RoadNode('\x67','\x67','\x78')
        ,'\x68': RoadNode('\x68','\x69','\x78')
        ,'\x69': RoadNode('\x69','\x69','\x7a')
        ,'\x6a': RoadNode('\x6a','\x6b','\x7a')
        ,'\x6b': RoadNode('\x6b','\x6b','\x7c')
        ,'\x72': RoadNode('\x72','\x72','\x83')
        ,'\x74': RoadNode('\x74','\x74','\x85')
        ,'\x76': RoadNode('\x76','\x76','\x87')
        ,'\x78': RoadNode('\x78','\x78','\x89')
        ,'\x7a': RoadNode('\x7a','\x7a','\x8b')
        ,'\x7c': RoadNode('\x7c','\x7c','\x8d')
        ,'\x83': RoadNode('\x83','\x83','\x94')
        ,'\x84': RoadNode('\x84','\x85','\x94')
        ,'\x85': RoadNode('\x85','\x85','\x96')
        ,'\x86': RoadNode('\x86','\x87','\x96')
        ,'\x87': RoadNode('\x87','\x87','\x98')
        ,'\x88': RoadNode('\x88','\x89','\x98')
        ,'\x89': RoadNode('\x89','\x89','\x9a')
        ,'\x8a': RoadNode('\x8a','\x8b','\x9a')
        ,'\x8b': RoadNode('\x8b','\x8b','\x9c')
        ,'\x8c': RoadNode('\x8c','\x8d','\x9c')
        ,'\x94': RoadNode('\x94','\x94','\xa5')
        ,'\x96': RoadNode('\x96','\x96','\xa7')
        ,'\x98': RoadNode('\x98','\x98','\xa9')
        ,'\x9a': RoadNode('\x9a','\x9a','\xab')
        ,'\x9c': RoadNode('\x9c','\x9c','\xad')
        ,'\xa5': RoadNode('\xa5','\xa5','\xb6')
        ,'\xa6': RoadNode('\xa6','\xa7','\xb6')
        ,'\xa7': RoadNode('\xa7','\xa7','\xb8')
        ,'\xa8': RoadNode('\xa8','\xa9','\xb8')
        ,'\xa9': RoadNode('\xa9','\xa9','\xba')
        ,'\xaa': RoadNode('\xaa','\xab','\xba')
        ,'\xab': RoadNode('\xab','\xab','\xbc')
        ,'\xac': RoadNode('\xac','\xad','\xbc')
        ,'\xb6': RoadNode('\xb6','\xb6','\xc7')
        ,'\xb8': RoadNode('\xb8','\xb8','\xc9')
        ,'\xba': RoadNode('\xba','\xba','\xcb')
        ,'\xbc': RoadNode('\xbc','\xbc','\xcd')
        ,'\xc7': RoadNode('\xc7','\xc7','\xd8')
        ,'\xc8': RoadNode('\xc8','\xc9','\xd8')
        ,'\xc9': RoadNode('\xc9','\xc9','\xda')
        ,'\xca': RoadNode('\xca','\xcb','\xda')
        ,'\xcb': RoadNode('\xcb','\xcb','\xdc')
        ,'\xcc': RoadNode('\xcc','\xcd','\xdc')}
    nodeLUT = {
         '\x23': BoardNode('\x23','\x22','\x23',None)
        ,'\x25': BoardNode('\x25','\x24','\x25',None)
        ,'\x27': BoardNode('\x27','\x26','\x27',None)
        ,'\x32': BoardNode('\x32','\x22','\x32',None)
        ,'\x34': BoardNode('\x34','\x23','\x24','\x34')
        ,'\x36': BoardNode('\x36','\x25','\x26','\x36')
        ,'\x38': BoardNode('\x38','\x27','\x38',None)
        ,'\x43': BoardNode('\x43','\x32','\x42','\x43')
        ,'\x45': BoardNode('\x45','\x34','\x44','\x45')
        ,'\x47': BoardNode('\x47','\x36','\x46','\x47')
        ,'\x49': BoardNode('\x49','\x38','\x48','\x49')
        ,'\x52': BoardNode('\x52','\x42','\x52',None)
        ,'\x54': BoardNode('\x54','\x43','\x44','\x54')
        ,'\x56': BoardNode('\x56','\x45','\x46','\x56')
        ,'\x58': BoardNode('\x58','\x47','\x48','\x58')
        ,'\x5a': BoardNode('\x5a','\x49','\x5a',None)
        ,'\x63': BoardNode('\x63','\x52','\x62','\x63')
        ,'\x65': BoardNode('\x65','\x54','\x64','\x65')
        ,'\x67': BoardNode('\x67','\x56','\x66','\x67')
        ,'\x69': BoardNode('\x69','\x58','\x68','\x69')
        ,'\x6b': BoardNode('\x6b','\x5a','\x6a','\x6b')
        ,'\x72': BoardNode('\x72','\x62','\x72',None)
        ,'\x74': BoardNode('\x74','\x63','\x64','\x74')
        ,'\x76': BoardNode('\x76','\x65','\x66','\x76')
        ,'\x78': BoardNode('\x78','\x67','\x68','\x78')
        ,'\x7a': BoardNode('\x7a','\x69','\x6a','\x7a')
        ,'\x7c': BoardNode('\x7c','\x6b','\x7c',None)
        ,'\x83': BoardNode('\x83','\x72','\x83',None)
        ,'\x85': BoardNode('\x85','\x74','\x84','\x85')
        ,'\x87': BoardNode('\x87','\x76','\x86','\x87')
        ,'\x89': BoardNode('\x89','\x78','\x88','\x89')
        ,'\x8b': BoardNode('\x8b','\x7a','\x8a','\x8b')
        ,'\x8d': BoardNode('\x8d','\x7c','\x8c',None)
        ,'\x94': BoardNode('\x94','\x83','\x84','\x94')
        ,'\x96': BoardNode('\x96','\x85','\x86','\x96')
        ,'\x98': BoardNode('\x98','\x87','\x88','\x98')
        ,'\x9a': BoardNode('\x9a','\x89','\x8a','\x9a')
        ,'\x9c': BoardNode('\x9c','\x8b','\x8c','\x9c')
        ,'\xa5': BoardNode('\xa5','\x94','\xa5',None)
        ,'\xa7': BoardNode('\xa7','\x96','\xa6','\xa7')
        ,'\xa9': BoardNode('\xa9','\x98','\xa8','\xa9')
        ,'\xab': BoardNode('\xab','\x9a','\xaa','\xab')
        ,'\xad': BoardNode('\xad','\x9c','\xac',None)
        ,'\xb6': BoardNode('\xb6','\xa5','\xa6','\xb6')
        ,'\xb8': BoardNode('\xb8','\xa7','\xa8','\xb8')
        ,'\xba': BoardNode('\xba','\xa9','\xaa','\xba')
        ,'\xbc': BoardNode('\xbc','\xab','\xac','\xbc')
        ,'\xc7': BoardNode('\xc7','\xb6','\xc7',None)
        ,'\xc9': BoardNode('\xc9','\xb8','\xc8','\xc9')
        ,'\xcb': BoardNode('\xcb','\xba','\xca','\xcb')
        ,'\xcd': BoardNode('\xcd','\xbc','\xcc',None)
        ,'\xd8': BoardNode('\xd8','\xc7','\xc8',None)
        ,'\xda': BoardNode('\xda','\xc9','\xca',None)
        ,'\xdc': BoardNode('\xdc','\xcb','\xcc',None)}     
        
    def __init__(self):
        pass
