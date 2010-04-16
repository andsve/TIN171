import pdb

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


class Message:
    def __init__(self):
        pass
        
    def to_cmd(self):
        pass
        
    @staticmethod
    def parse(text):
        return None

class NullMessage(Message):
    id = 1000
    def __init__(self):
        pass

    def to_cmd(self):
        return "{0}|".format(self.id)        
        
    @staticmethod
    def parse(text):
        pass

class NewChannelMessage(Message):
    id = 1001
    def __init__(self, channel):
        self.channel = channel
         
    def to_cmd(self):
        return "{0}|{1}".format(self.id, self.channel)
         
    @staticmethod
    def parse(text):
        return NewChannelMessage(text)
       
class MembersMessage(Message):
    id = 1002
    def __init__(self, channel, members):
        self.channel = channel
        self.members = members
    
    def to_cmd(self):
        return "{0}|{1},{2}".format(self.id, self.channel
                                   ,",".join(self.members))
    @staticmethod
    def parse(text):
        data = text.split(",")
        ch, mem = data[0], data[1:]
        return MembersMessage(ch, mem)

class ChannelsMessage(Message):
    id = 1003
    def __init__(self, channels):
        self.channels = channels

    def to_cmd(self):
        return "{0}|{1}".format(self.id, ",".join(self.channels))

    @staticmethod
    def parse(text):
        channels = text.split(",")
        return ChannelsMessage(channels)

class JoinMessage(Message):
    id = 1004
    def __init__(self, nickname, password, host, game):
        self.nickname = nickname
        self.password = password
        self.host = host
        self.game = game
        
    def to_cmd(self):
        pwd = "\t" if self.password == "" else self.password
        return "{0}|{1},{2},{3},{4}".format(self.id, self.nickname, pwd
                                            ,self.host, self.game)
        
    @staticmethod
    def parse(text):
        data = text.split(",")
        data[1] = "" if data[1] == "\t" else ""
        return JoinMessage(*data)
 
class TextMsgMessage(Message):
    id = 1005
    def __init__(self, channel, nickname, textmessage):
        self.channel = channel
        self.nickname = nickname
        self.message = textmessage
        
    def to_cmd(self):
        return "{0}|{1}\xc0\x80{2}\xc0\x80{3}".format(self.id, self.channel
                                         ,self.nickname, self.message)
        
    @staticmethod
    def parse(text):
        # private static String sep2 = "" + (char) 0; // why?
        data = text.split("\xc0\x80")
        return TextMsgMessage(data[0], data[1], data[2])
        

class LeaveMessage(Message):
    id = 1006
    def __init__(self, nickname, hostname, channel):
        self.nickname = nickname
        self.hostname = hostname
        self.channel = channel
        
    def to_cmd(self):
        return "{0}|{1}{2}{3}".format(self.id, self.nickname
                                     ,self.hostname, self.channel)
        
    @staticmethod
    def parse(text):
        data = text.split(",")
        return LeaveMessage(data[0], data[1], data[2])

class DeleteChannelMessage(Message):
    id = 1007
    def __init__(self, channel):
        self.channel = channel
        
    def to_cmd(self):
        return "{0}|{1}".format(self.id, self.channel)
        
    @staticmethod
    def parse(text):
        return DeleteChannelMessage(text)

class LeaveAllMessage(Message):
    id = 1008
    def __init__(self):
        pass
        
    def to_cmd(self):
        return "{0}".format(self.id)
        
    @staticmethod
    def parse(text):
        return LeaveAllMessage()

class PutPieceMessage(Message):
    id = 1009
    def __init__(self, game, piecetype, playernum, coords):
        self.game = game
        self.piecetype = piecetype
        self.playernum = playernum
        self.coords = coords
        
    def to_cmd(self):
        return "{0}|{1},{2},{3},{4}".format(self.id, self.game
                                           ,self.piecetype, self.playernum
                                           ,self.coords)
        
    @staticmethod
    def parse(text):
        data = text.split(",")
        return PutPieceMessage(data[0], data[1], data[2], data[3])

class GameTextMsgMessage(Message):
    id = 1010
    def __init__(self, game, nickname, textmessage):
        self.game = game
        self.nickname = nickname
        self.message = textmessage
        
    def to_cmd(self):
        return "{0}|{1}\xc0\x80{2}\xc0\x80{3}".format(self.id, self.game
                                         ,self.nickname, self.message)
        
    @staticmethod
    def parse(text):
        # private static String sep2 = "" + (char) 0; // why?
        data = text.split("\xc0\x80")
        return GameTextMsgMessage(data[0], data[1], data[2])

class LeaveGameMessage(Message):
    id = 1011
    def __init__(self, nickname, hostname, game):
        self.nickname = nickname
        self.hostname = hostname
        self.game = game
        
    def to_cmd(self):
        return "{0}|{1}{2}{3}".format(self.id, self.nickname
                                     ,self.hostname, self.channel)
        
    @staticmethod
    def parse(text):
        data = text.split(",")
        return LeaveGameMessage(data[0], data[1], data[2])

class SitDownMessage(Message):
    id = 1012
    def __init__(self, game, nickname, playernum, isrobot):
        self.game = game
        self.nickname = nickname
        self.playernum = playernum
        self.isrobot = isrobot
        
    def to_cmd(self):
        return "{0}|{1},{2},{3},{4}".format(self.id, self.game, self.nickname
                                       ,self.playernum, str(self.isrobot).lower())
        
    @staticmethod
    def parse(text):
        data = text.split(",")
        gn = data[0] # game name
        nn = data[1] # nick name
        pn = data[2] # seat number
        rf = False if data[3] == "false" else True # is robot
        return SitDownMessage(gn, nn, pn, rf)

class JoinGameMessage(Message):
    id = 1013
    def __init__(self, nickname, password, host, game):
        self.nickname = nickname
        self.password = password
        self.host = host
        self.game = game
        
    def to_cmd(self):
        pwd = "\t" if self.password == "" else self.password
        return "{0}|{1},{2},{3},{4}".format(self.id, self.nickname, pwd
                                        ,self.host, self.game)
        
    @staticmethod
    def parse(text):
        data = text.split(",")
        data[1] = "" if data[1] == "\t" else ""
        return JoinGameMessage(*data)

class BoardLayoutMessage(Message):
    id = 1014
    def __init__(self, board):
        self.board = board
        
    def to_cmd(self):
        return "{0}|{1}".format(self.id, ",".join(self.board))
        
    @staticmethod
    def parse(text):
        board = text.split(",")
        return BoardLayoutMessage(board)

class DeleteGameMessage(Message):
    id = 1015
    def __init__(self, game):
        self.game = game
        
    def to_cmd(self):
        return "{0}|{1}".format(self.id, self.game)
       
    @staticmethod 
    def parse(text):
        return DeleteGameMessage(text)


class NewGameMessage(Message):
    id = 1016
    def __init__(self, game):
        self.game = game
        
    def to_cmd(self):
        return "{0}|{1}".format(self.id, self.game)
       
    @staticmethod 
    def parse(text):
        return NewGameMessage(text)

class GameMembersMessage(Message):
    id = 1017
    def __init__(self, game, members):
        self.game = game
        self.members = members
        
    def to_cmd(self):
        members = ",".join(self.members)
        return "{0}|{1},{2}".format(self.id, self.game, members)
        
    @staticmethod
    def parse(text):
        pass

class StartGameMessage(Message):
    id = 1018
    def __init__(self, game):
        self.game = game
        
    def to_cmd(self):
        return "{0}|{1}".format(self.id, self.game)
        
    @staticmethod
    def parse(text):
        return StartGameMessage(text)

class GamesMessage(Message):
    id = 1019
    def __init__(self, games):
        self.games = games

    def to_cmd(self):
        return "{0}|{1}".format(self.id, ",".join(self.games))

    @staticmethod
    def parse(text):
        games = text.split(",")
        return GamesMessage(games)

class JoinAuthMessage(Message):
    id = 1020
    def __init__(self, nick, channel):
        self.nickname = nickname
        self.channel = channel
        
    def to_cmd(self):
        return "{0}|{1},{2}".format(self.id, self.nickname, self.channel)
        
    @staticmethod
    def parse(text):
        nickname, channel = text.split(",")
        return JoinAuthMessage(nickname, channel)

class JoinGameAuthMessage(Message):
    id = 1021
    def __init__(self, game):
        self.game = game
       
    def to_cmd(self):
        return "{0}|{1}".format(self.id, self.game)
        
    @staticmethod
    def parse(text):
        return JoinGameAuthMessage(text)

class ImARobotMessage(Message):
    id = 1022
    def __init__(self, nickname):
        self.nickname = nickname
        
    def to_cmd(self):
        return "{0}|{1}".format(self.id, self.nickname)
        
    @staticmethod
    def parse(text):
        return ImARobotMessage(text)

class JoinGameRequestMessage(Message):
    id = 1023
    def __init__(self, game, playernum):
        self.game = game
        self.playernum = playernum
    
    def to_cmd(self):
        return "{0}|{1},{2}".format(self.game, self.playernum)
        
    @staticmethod
    def parse(text):
        game, playernum = text.split(",")
        return JoinGameRequestMessage(game, playernum)

class PlayerElementMessage(Message):
    id = 1024
    etype = {
            '1': 'CLAY',
            '2': 'ORE',
            '3': 'SHEEP',
            '4': 'WHEAT',
            '5': 'WOOD',
            '6': 'UNKNOWN',
            '10': 'ROADS',
            '11': 'SETTLEMENTS',
            '12': 'CITIES',
            '15': 'NUMKNIGHTS',
            '100': 'SET',
            '101': 'GAIN',
            '102': 'LOSE' 
    }
    def __init__(self, game, playernum, action, element, value):
        self.game = game
        self.playernum = playernum
        self.action = action
        self.element = element
        self.value = value
        
    def to_cmd(self):
        for i, v in self.etype.items():
            if self.action == v:
                ac = i
            elif self.element == v:
                el = i
        return "{0}|{1},{2},{3},{4},{5}".format(self.id, self.game, self.playernum, ac, el, self.value)
        
    @staticmethod
    def parse(text):
        game, playernum, action, element, value = text.split(',')
        ac = PlayerElementMessage.etype[action]
        el = PlayerElementMessage.etype[element]
        return PlayerElementMessage(game, playernum
                                    , ac, el
                                    , int(value))

class GameStateMessage(Message):
    id = 1025
    def __init__(self, game, state):
        self.game = game
        self.state = state
        
    def to_cmd(self):
        return "{0}|{1},{2}".format(self.id, self.game, self.state)
        
    @staticmethod
    def parse(text):
        g, s = text.split(",")
        return GameStateMessage(g, s)

class TurnMessage(Message):
    id = 1026
    def __init__(self, game, playernum):
        self.game = game
        self.playernum = playernum
        
    def to_cmd(self):
        return "{0}|{1},{2}".format(self.id, self.game, self.playernum)
        
    @staticmethod
    def parse(text):
        gn, pn = text.split(",")
        return TurnMessage(gn, pn)

class SetupDoneMessage(Message):
    id = 1027
    def __init__(self, game):
        self.game = game
        
    def to_cmd(self):
        return "{0}|{1}".format(self.id, self.game)
        
    @staticmethod
    def parse(text):
        return SetupDoneMessage(text)

class DiceResultMessage(Message):
    id = 1028
    def __init__(self, game, result):
        self.game = game
        self.result = result
        
    def to_cmd(self):
        return "{0}|{1},{2}".format(self.id, self.game, self.result)
        
    @staticmethod
    def parse(text):
        game, result = text.split(",")
        return DiceResultMessage(game, int(result))

class DiscardRequestMessage(Message):
    id = 1029
    def __init__(self, game, numcards):
        self.game = game
        self.numcards = numcards
        
    def to_cmd(self):
        return "{0}|{1},{2}".format(self.id, self.game, self.numcards)
        
    @staticmethod
    def parse(text):
        game, numcards = text.split(",")
        return DiscardRequestMessage(game, int(numcards))

class RollDiceRequestMessage(Message):
    id = 1030
    def __init__(self, game):
        self.game = game
        
    def to_cmd(self):
        return "{0}|{1}".format(self.id, self.game)
        
    @staticmethod
    def parse(text):
        return RollDiceRequestMessage(text)

class RollDiceMessage(Message):
    id = 1031
    def __init__(self, game):
        self.game = game
        
    def to_cmd(self):
        return "{0}|{1}".format(self.id, self.game)
        
    @staticmethod
    def parse(text):
        return RollDiceMessage(text)

class EndTurnMessage(Message):
    id = 1032
    def __init__(self, game):
        self.game = game
        
    def to_cmd(self):
        return "{0}|{1}".format(self.id, self.game)
        
    @staticmethod
    def parse(text):
        return EndTurnMessage(text)

class DiscardMessage(Message):
    id = 1033
    def __init__(self, game, clay, ore, sheep, wheat, wood, unknown):
        self.game = game
        self.clay = clay
        self.sheep = sheep
        self.wheat = wheat
        self.wood = wood
        self.unknown = unknown
    
    def to_cmd(self):
        return "{0}|{1},{2},{3},{4},{5},{6}".format(self.game, self.clay, self.sheep
                                                    ,self.wheat, self.wood, self.unknown)
    
    @staticmethod
    def parse(text):
        g, c, s, wh, wo, u = map(int, text.split(","))
        return DiscardMessage(g, c, s, wh, wo, u)
        
class MoveRobberMessage(Message):
    id = 1034
    def __init__(self, game, playernum, coords):
        self.game = game
        self.playernum = playernum
        self.coords = coords
        
    def to_cmd(self):
        return "{0}|{1},{2},{3}".format(self.id, self.game, self.playernum, self.coords)
    
    @staticmethod
    def parse(text):
        g, pn, coords = text.split(",")
        return MoveRobberMessage(g, int(pn), coords)
 
class ChoosePlayerMessage(Message):
    id = 1035  
    def __init__(self, game, choice):
        self.game = game
        self.choice = choice
        
    def to_cmd(self):
        return "{0}|{1},{2}".format(self.id, self.game, self.choice)
             
    @staticmethod
    def parse(text):
        game, choice = text.split(",")
        return ChoosePlayerMessage(game, int(choice))
   
class ChoosePlayerRequestMessage(Message):
    id = 1036
    def __init__(self, game, choices):
        self.game = game
        self.choices = choices
        
    def to_cmd(self):
        return "{0}|{1},{2}".format(self.id, self.game
                                    ,",".join(self.choices))
        
    @staticmethod
    def parse(text):
        data = text.split(",")
        game, choices = data[0], data[1:]
        return ChoosePlayerRequestMessage(game, choices)

class RejectOfferMessage(Message):
    id = 1037
    def __init__(self, game, playernum):
        self.game = game
        self.playernum = playernum
        
    def to_cmd(self):
        return "{0}|{1},{2}".format(self.id, self.game, self.playernum)
        
    @staticmethod
    def parse(text):
        g, pn = text.split(",")
        return RejectOfferMessage(g, int(pn))

class ClearOfferMessage(Message):
    id = 1038  
    def __init__(self, game, playernum):
        self.game = game
        self.playernum = playernum
        
    def to_cmd(self):
        return "{0}|{1},{2}".format(self.id, self.game, self.playernum)
    
    @staticmethod
    def parse(text):
        game, playernum = text.split(",")
        return ClearOfferMessage(game, int(playernum))

class AcceptOfferMessage(Message):
    id = 1039 
    def __init__(self, game, acc_player, off_player):
        self.game = game
        self.accepting = acc_player
        self.offering = off_player
        
    def to_cmd(self):
        return "{0}|{1},{2},{3}".format(self.id, self.game
                                        ,self.accepting, self.offering)
        
    @staticmethod
    def parse(text):
        game, accept, offer = text.split(",")
        return AcceptOfferMessage(game, int(accept), int(offer))

# TODO: See SOCResourceConstants.java for value order
class BankTradeMessage(Message):
    id = 1040
    def __init__(self, game, give, get):
        self.game = game
        self.give = give
        self.get = get
        
    def to_cmd(self):
        return "{0}|{1},{2},{3}".format(self.id, self.game
                                        ,','.join(self.give)
                                        ,','.join(self.get))
        
    @staticmethod
    def parse(text):
        data = text.split(",")
        game = data[0]
        give = map(int, data[1:6])
        got = map(int, data[6:11])
        return BankTradeMessage(game, give, get)

# TODO: Implement if needed
class MakeOfferMessage(Message):
    id = 1041
    def __init__(self):
        pass
        
    @staticmethod
    def parse(text):
        pass

class ClearTradeMsgMessage(Message):
    id = 1042
    def __init__(self, game, playernum):
        self.game = game
        self.playernum = playernum
        
    def to_cmd(self):
        return "{0}|{1}".format(self.id, self.playernum)
        
    @staticmethod
    def parse(text):
        game, player = text.split(",")
        return ClearTradeMsgMessage(game, int(player))

class BuildRequestMessage(Message):
    id = 1043
    def __init__(self, game, piecetype):
        self.game = game
        self.piecetype = piecetype
        
    def to_cmd(self):
        return "{0}|{1},{2}".format(self.id, self.game, self.piecetype)
        
    @staticmethod
    def parse(text):
        game, pt = text.split(",")
        return BuildRequestMessage(game, int(pt))

class CancelBuildRequestMessage(Message):
    id = 1044 
    def __init__(self, game, piecetype):
        self.game = game
        self.piecetype = piecetype
        
    def to_cmd(self):
        return "{0}|{1},{2}".format(self.id, self.game, self.piecetype)
        
    @staticmethod
    def parse(text):
        game, pt = text.split(",")
        return CancelBuildRequestMessage(game, int(pt))

class BuyCardRequestMessage(Message):
    id = 1045  
    def __init__(self, game):
        self.game = game
        
    def to_cmd(self):
        return "{0}|{1}".format(self.id, self.game)
        
    @staticmethod
    def parse(text):
        return BuyCardRequestMessage(text)

# TODO: See SOCDevCard.java
class DevCardMessage(Message):
    id = 1046
    def __init__(self, game, playernum, action, cardtype):
        self.game = game
        self.playernum = playernum
        self.action = action
        self.cardtype = cardtype
        
    def to_cmd(self):
        return "{0}|{1},{2},{3},{4}".format(self.id, self.game
                                            ,self.playernum, self.action
                                            ,self.cardtype)
              
    @staticmethod
    def parse(text):
        g, pn, ac, ct = text.split(",")
        return DevCardmessage(g, int(pn), int(ac), int(ct))
   
class DevCardCountMessage(Message):
    id = 1047
    def __init__(self, game, count):
        self.game = game
        self.count = count
     
    def to_cmd(self):
        return "{0}|{1},{2}".format(self.id, self.game, self.count)
     
    @staticmethod
    def parse(text):
        game, count = text.split(",")
        return DevCardCountMessage(game, int(count))

class SetPlayedDevCardMessage(Message):
    id = 1048
    def __init__(self, game, playernum, cardflag):
        self.game = game
        self.playernum = playernum
        self.cardflag = cardflag
        
    def to_cmd(self):
        return "{0}|{1},{2},{3}".format(self.id, self.game, self.playernum, str(self.cardflag).lower())
        
    @staticmethod
    def parse(text):
        g, p, c = text.split(",")
        cf = True if c.lower() == "true" else False
        return SetPlayedDevCardMessage(g, p, cf)

# TODO: Lookup how cards are represented
class PlayDevCardRequestMessage(Message):
    id = 1049
    def __init__(self, game, card):
        self.game = game
        self.card = card       
    
    def to_cmd(self):
        return "{0}|{1},{2}".format(self.id, self.game, self.card)
              
    @staticmethod
    def parse(text):
        g, c = text.split(",")
        return PlayDevCardRequestMessage(g, c)
   
# TODO: Not needed yet.
class DiscoveryPickMessage(Message):
    id = 1052
    def __init__(self):
        pass
        
    @staticmethod
    def parse(text):
        pass

# TODO: Not needed yet.
class MonopolyPickMessage(Message):
    id = 1053
    def __init__(self):
        pass
        
    @staticmethod
    def parse(text):
        pass

class FirstPlayerMessage(Message):
    id = 1054
    def __init__(self, game, seatnum):
        self.game = game
        self.seatnum = seatnum
                 
    def to_cmd(self):
        return "{0}|{1},{2}".format(self.id, self.game, self.seatnum)
                 
    @staticmethod
    def parse(text):
        game, seat = text.split(",")
        return FirstPlayerMessage(game, int(seat))

class SetTurnMessage(Message):
    id = 1055
    def __init__(self, game, seatnum):
        self.game = game
        self.seatnum = seatnum
                 
    def to_cmd(self):
        return "{0}|{1},{2}".format(self.id, self.game, self.seatnum)
                 
    @staticmethod
    def parse(text):
        game, seat = text.split(",")
        return SetTurnMessage(game, int(seat))

class RobotDismissMessage(Message):
    id = 1056
    def __init__(self, game):
        self.game = game
        
    def to_cmd(self):
        return "{0}|{1}".format(self.id, self.game)
        
    @staticmethod
    def parse(text):
        return RobotDismissMessage(text)

class PotentialSettlementsMessage(Message):
    id = 1057
    def __init__(self, game, playernum, settlements):
        self.game = game
        self.playernum = playernum
        self.settlements = settlements
        
    def to_cmd(self):
        return "{0}|{1},{2},{3}".format(self.id, self.game, self.playernum
                                        ,','.join(self.settlements))
                 
    @staticmethod
    def parse(text):
        data = text.split(",")
        game, pn = data[0], data[1]
        settlements = map(int, data[2:])
        return PotentialSettlementsMessage(game, int(pn), settlements)
        

class ChangeFaceMessage(Message):
    id = 1058
    def __init__(self, game, playernum, faceid):
        self.game = game
        self.playernum = playernum
        self.faceid = faceid
        
    def to_cmd(self):
        return "{0}|{1},{2},{3}".format(self.id, self.game, self.playernum, self.faceid)
        
    @staticmethod
    def parse(text):
        g, pn, fi = text.split(",")
        return ChangeFaceMessage(g, pn, fi)

# TODO
class RejectConnectionMessage(Message):
    id = 1059
    def __init__(self):
        pass 
                
    @staticmethod
    def parse(text):
        pass

class LastSettlementMessage(Message):
    id = 1060
    def __init__(self, game, playernum, coords):
        self.game = game
        self.playernum = playernum
        self.coords = coords
        
    def to_cmd(self):
        return "{0}|{1},{2},{3}".format(self.id, self.game
                                        ,self.playernum, self.coords)
        
    @staticmethod
    def parse(text):
        g, pn, co = text.split(",")
        return LastSettlementMessage(g, int(pn), int(co))

# TODO: 
class GameStatsMessage(Message):
    id = 1061
    def __init__(self):
        pass
        
    @staticmethod
    def parse(text):
        pass

# TODO: 
class BCastTextMsgMessage(Message):
    id = 1062
    def __init__(self):
        pass
        
    @staticmethod
    def parse(text):
        pass

class ResourceCountMessage(Message):
    id = 1063
    def __init__(self, game, playernum, count):
        self.game = game
        self.playernum = playernum
        self.count = count
        
    def to_cmd(self):
        return "{0}|{1},{2},{3}".format(self.id, self.game, self.playernum
                                        ,self.count)
                
    @staticmethod
    def parse(text):
        g, pn, c = text.split(",")
        return ResourceCountMessage(g, int(pn), int(c))

# TODO: Fix later
class AdminPingMessage(Message):
    id = 1064
    def __init__(self):
        pass
        
    @staticmethod
    def parse(text):
        pass

# TODO: Fix later
class AdminResetMessage(Message):
    id = 1065
    def __init__(self):
        pass
        
    @staticmethod
    def parse(text):
        pass

class LongestRoadMessage(Message):
    id = 1066
    def __init__(self, game, playernum):
        self.game = game
        self.playernum = playernum
        
    def to_cmd(self):
        return "{0}|{1},{2}".format(self.id, self.game, self.playernum)
        
    @staticmethod
    def parse(text):
        game, pn = text.split(",")
        return LongestRoadMessage(game, int(pn))

class LargestArmyMessage(Message):
    id = 1067
    def __init__(self, game, playernum):
        self.game = game
        self.playernum = playernum
        
    def to_cmd(self):
        return "{0}|{1},{2}".format(self.id, self.game, self.playernum)
        
    @staticmethod
    def parse(text):
        game, pn = text.split(",")
        return LargestArmyMessage(game, int(pn))

# TODO: Fix later
class SetSeatLockMessage(Message):
    id = 1068
    def __init__(self):
        pass
        
    @staticmethod
    def parse(text):
        pass

class StatusMessageMessage(Message):
    id = 1069
    def __init__(self):
        pass
        
    @staticmethod
    def parse(text):
        pass

class CreateAccountMessage(Message):
    id = 1070
    def __init__(self):
        pass
             
    @staticmethod
    def parse(text):
        pass
   
class UpdateRobotParamsMessage(Message):
    id = 1071
    def __init__(self):
        pass
        
    @staticmethod
    def parse(text):
        pass

# TODO: Fix later/ignore
class ServerPingMessage(Message):
    id = 9999  
    def __init__(self):
        pass 

    @staticmethod
    def parse(text):
        pass

class BoardLayout:

    roadList = []
    nodeList = []
    def __init__(self):
        """roadList[ord('\x22')] = RoadNode('\x22','\x23','\x32')
        roadList[ord('\x23')] = RoadNode('\x23','\x23','\x34')
        roadList[ord('\x24')] = RoadNode('\x24','\x25','\x34')
        roadList[ord('\x25')] = RoadNode('\x25','\x25','\x36')
        roadList[ord('\x26')] = RoadNode('\x26','\x27','\x36')
        roadList[ord('\x27')] = RoadNode('\x27','\x27','\x38')
        roadList[ord('\x32')] = RoadNode('\x32','\x32','\x43')
        roadList[ord('\x34')] = RoadNode('\x34','\x34','\x45')
        roadList[ord('\x36')] = RoadNode('\x36','\x36','\x47')
        roadList[ord('\x38')] = RoadNode('\x38','\x38','\x49')
        roadList[ord('\x42')] = RoadNode('\x42','\x43','\x52')
        roadList[ord('\x43')] = RoadNode('\x43','\x43','\x54')
        roadList[ord('\x44')] = RoadNode('\x44','\x45','\x54')
        roadList[ord('\x45')] = RoadNode('\x45','\x45','\x56')
        roadList[ord('\x46')] = RoadNode('\x46','\x47','\x56')
        roadList[ord('\x47')] = RoadNode('\x47','\x47','\x58')
        roadList[ord('\x48')] = RoadNode('\x48','\x49','\x58')
        roadList[ord('\x49')] = RoadNode('\x49','\x49','\x5a')
        roadList[ord('\x52')] = RoadNode('\x52','\x52','\x63')
        roadList[ord('\x54')] = RoadNode('\x54','\x54','\x65')
        roadList[ord('\x56')] = RoadNode('\x56','\x56','\x67')
        roadList[ord('\x58')] = RoadNode('\x58','\x58','\x69')
        roadList[ord('\x5a')] = RoadNode('\x5a','\x5a','\x6b')
        roadList[ord('\x62')] = RoadNode('\x62','\x63','\x72')
        roadList[ord('\x63')] = RoadNode('\x63','\x63','\x74')
        roadList[ord('\x64')] = RoadNode('\x64','\x65','\x74')
        roadList[ord('\x65')] = RoadNode('\x65','\x65','\x76')
        roadList[ord('\x66')] = RoadNode('\x66','\x67','\x76')
        roadList[ord('\x67')] = RoadNode('\x67','\x67','\x78')
        roadList[ord('\x68')] = RoadNode('\x68','\x69','\x78')
        roadList[ord('\x69')] = RoadNode('\x69','\x69','\x7a')
        roadList[ord('\x6a')] = RoadNode('\x6a','\x6b','\x7a')
        roadList[ord('\x6b')] = RoadNode('\x6b','\x6b','\x7c')
        roadList[ord('\x72')] = RoadNode('\x72','\x72','\x83')
        roadList[ord('\x74')] = RoadNode('\x74','\x74','\x85')
        roadList[ord('\x76')] = RoadNode('\x76','\x76','\x87')
        roadList[ord('\x78')] = RoadNode('\x78','\x78','\x89')
        roadList[ord('\x7a')] = RoadNode('\x7a','\x7a','\x8b')
        roadList[ord('\x7c')] = RoadNode('\x7c','\x7c','\x8d')
        roadList[ord('\x83')] = RoadNode('\x83','\x83','\x94')
        roadList[ord('\x84')] = RoadNode('\x84','\x85','\x94')
        roadList[ord('\x85')] = RoadNode('\x85','\x85','\x96')
        roadList[ord('\x86')] = RoadNode('\x86','\x87','\x96')
        roadList[ord('\x87')] = RoadNode('\x87','\x87','\x98')
        roadList[ord('\x88')] = RoadNode('\x88','\x89','\x98')
        roadList[ord('\x89')] = RoadNode('\x89','\x89','\x9a')
        roadList[ord('\x8a')] = RoadNode('\x8a','\x8b','\x9a')
        roadList[ord('\x8b')] = RoadNode('\x8b','\x8b','\x9c')
        roadList[ord('\x8c')] = RoadNode('\x8c','\x8d','\x9c')
        roadList[ord('\x94')] = RoadNode('\x94','\x94','\xa5')
        roadList[ord('\x96')] = RoadNode('\x96','\x96','\xa7')
        roadList[ord('\x98')] = RoadNode('\x98','\x98','\xa9')
        roadList[ord('\x9a')] = RoadNode('\x9a','\x9a','\xab')
        roadList[ord('\x9c')] = RoadNode('\x9c','\x9c','\xad')
        roadList[ord('\xa5')] = RoadNode('\xa5','\xa5','\xb6')
        roadList[ord('\xa6')] = RoadNode('\xa6','\xa7','\xb6')
        roadList[ord('\xa7')] = RoadNode('\xa7','\xa7','\xb8')
        roadList[ord('\xa8')] = RoadNode('\xa8','\xa9','\xb8')
        roadList[ord('\xa9')] = RoadNode('\xa9','\xa9','\xba')
        roadList[ord('\xaa')] = RoadNode('\xaa','\xab','\xba')
        roadList[ord('\xab')] = RoadNode('\xab','\xab','\xbc')
        roadList[ord('\xac')] = RoadNode('\xac','\xad','\xbc')
        roadList[ord('\xb6')] = RoadNode('\xb6','\xb6','\xc7')
        roadList[ord('\xb8')] = RoadNode('\xb8','\xb8','\xc9')
        roadList[ord('\xba')] = RoadNode('\xba','\xba','\xcb')
        roadList[ord('\xbc')] = RoadNode('\xbc','\xbc','\xcd')
        roadList[ord('\xc7')] = RoadNode('\xc7','\xc7','\xd8')
        roadList[ord('\xc8')] = RoadNode('\xc8','\xc9','\xd8')
        roadList[ord('\xc9')] = RoadNode('\xc9','\xc9','\xda')
        roadList[ord('\xca')] = RoadNode('\xca','\xcb','\xda')
        roadList[ord('\xcb')] = RoadNode('\xcb','\xcb','\xdc')
        roadList[ord('\xcc')] = RoadNode('\xcc','\xcd','\xdc')
        
        nodeList[ord('\x23')] = BoardNode('\x23','\x22','\x23',None)
        nodeList[ord('\x25')] = BoardNode('\x25','\x24','\x25',None)
        nodeList[ord('\x27')] = BoardNode('\x27','\x26','\x27',None)
        nodeList[ord('\x32')] = BoardNode('\x32','\x22','\x32',None)
        nodeList[ord('\x34')] = BoardNode('\x34','\x23','\x24','\x34')
        nodeList[ord('\x36')] = BoardNode('\x36','\x25','\x26','\x36')
        nodeList[ord('\x38')] = BoardNode('\x38','\x27','\x38',None)
        nodeList[ord('\x43')] = BoardNode('\x43','\x32','\x42','\x43')
        nodeList[ord('\x45')] = BoardNode('\x45','\x34','\x44','\x45')
        nodeList[ord('\x47')] = BoardNode('\x47','\x36','\x46','\x47')
        nodeList[ord('\x49')] = BoardNode('\x49','\x38','\x48','\x49')
        nodeList[ord('\x52')] = BoardNode('\x52','\x42','\x52',None)
        nodeList[ord('\x54')] = BoardNode('\x54','\x43','\x44','\x54')
        nodeList[ord('\x56')] = BoardNode('\x56','\x45','\x46','\x56')
        nodeList[ord('\x58')] = BoardNode('\x58','\x47','\x48','\x58')
        nodeList[ord('\x5a')] = BoardNode('\x5a','\x49','\x5a',None)
        nodeList[ord('\x63')] = BoardNode('\x63','\x52','\x62','\x63')
        nodeList[ord('\x65')] = BoardNode('\x65','\x54','\x64','\x65')
        nodeList[ord('\x67')] = BoardNode('\x67','\x56','\x66','\x67')
        nodeList[ord('\x69')] = BoardNode('\x69','\x58','\x68','\x69')
        nodeList[ord('\x6b')] = BoardNode('\x6b','\x5a','\x6a','\x6b')
        nodeList[ord('\x72')] = BoardNode('\x72','\x62','\x72',None)
        nodeList[ord('\x74')] = BoardNode('\x74','\x63','\x64','\x74')
        nodeList[ord('\x76')] = BoardNode('\x76','\x65','\x66','\x76')
        nodeList[ord('\x78')] = BoardNode('\x78','\x67','\x68','\x78')
        nodeList[ord('\x7a')] = BoardNode('\x7a','\x69','\x6a','\x7a')
        nodeList[ord('\x7c')] = BoardNode('\x7c','\x6b','\x7c',None)
        nodeList[ord('\x83')] = BoardNode('\x83','\x72','\x83',None)
        nodeList[ord('\x85')] = BoardNode('\x85','\x74','\x84','\x85')
        nodeList[ord('\x87')] = BoardNode('\x87','\x76','\x86','\x87')
        nodeList[ord('\x89')] = BoardNode('\x89','\x78','\x88','\x89')
        nodeList[ord('\x8b')] = BoardNode('\x8b','\x7a','\x8a','\x8b')
        nodeList[ord('\x8d')] = BoardNode('\x8d','\x7c','\x8c',None)
        nodeList[ord('\x94')] = BoardNode('\x94','\x83','\x84','\x94')
        nodeList[ord('\x96')] = BoardNode('\x96','\x85','\x86','\x96')
        nodeList[ord('\x98')] = BoardNode('\x98','\x87','\x88','\x98')
        nodeList[ord('\x9a')] = BoardNode('\x9a','\x89','\x8a','\x9a')
        nodeList[ord('\x9c')] = BoardNode('\x9c','\x8b','\x8c','\x9c')
        nodeList[ord('\xa5')] = BoardNode('\xa5','\x94','\xa5',None)
        nodeList[ord('\xa7')] = BoardNode('\xa7','\x96','\xa6','\xa7')
        nodeList[ord('\xa9')] = BoardNode('\xa9','\x98','\xa8','\xa9')
        nodeList[ord('\xab')] = BoardNode('\xab','\x9a','\xaa','\xab')
        nodeList[ord('\xad')] = BoardNode('\xad','\x9c','\xac',None)
        nodeList[ord('\xb6')] = BoardNode('\xb6','\xa5','\xa6','\xb6')
        nodeList[ord('\xb8')] = BoardNode('\xb8','\xa7','\xa8','\xb8')
        nodeList[ord('\xba')] = BoardNode('\xba','\xa9','\xaa','\xba')
        nodeList[ord('\xbc')] = BoardNode('\xbc','\xab','\xac','\xbc')
        nodeList[ord('\xc7')] = BoardNode('\xc7','\xb6','\xc7',None)
        nodeList[ord('\xc9')] = BoardNode('\xc9','\xb8','\xc8','\xc9')
        nodeList[ord('\xcb')] = BoardNode('\xcb','\xba','\xca','\xcb')
        nodeList[ord('\xcd')] = BoardNode('\xcd','\xbc','\xcc',None)
        nodeList[ord('\xd8')] = BoardNode('\xd8','\xc7','\xc8',None)
        nodeList[ord('\xda')] = BoardNode('\xda','\xc9','\xca',None)
        nodeList[ord('\xdc')] = BoardNode('\xdc','\xcb','\xcc',None)"""       


class RoadNode:

    id = None
    n1 = None
    n2 = None
    owner = None
    def __init__(self, name, neighbour1, neighbour2):
        id = name
        n1 = neighbour1
        n2 = neighbour2

class BoardNode:

    id = None
    n1 = None
    n2 = None
    n3 = None
    harbor = None
    resource1 = None
    resource2 = None
    resource3 = None
    
    def __init__(self, name, neighbour1, neighbour2, neighbour3):
        id = name
        n1 = neighbour1
        n2 = neighbour2
        n3 = neighbour3
