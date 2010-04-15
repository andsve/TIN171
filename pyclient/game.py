import pdb

class Game:
    def __init__(self):
        # Initiate gameboard when the message is recieved?
        #self.gameboard = gameboard # save raw gameboad
        #self.parse_board()         # parse gameboard and create internal representation
        self.messagetbl = {}
        self.init_parser()
    
    def init_parser(self):
        self.messagetbl = {}
        for g in globals():
            cg = globals()[g]
            if str(g).endswith("Message") and hasattr(cg, "id"):
                self.messagetbl[str(cg.id)] = (cg, g)
    
    def parse_message(self, msg):
        id, txt = msg[:4], msg[5:]
        message_class, name = self.messagetbl[id] 
        return (name, message_class.parse(txt))
    
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
        print data
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
    def __init__(self):
        pass
        
    @staticmethod
    def parse(text):
        pass

class MoveRobberMessage(Message):
    id = 1034
    def __init__(self):
        pass
    
    @staticmethod
    def parse(text):
        pass
 
class ChoosePlayerMessage(Message):
    id = 1035  
    def __init__(self):
        pass    
             
    @staticmethod
    def parse(text):
        pass
   
class ChoosePlayerRequestMessage(Message):
    id = 1036
    def __init__(self):
        pass
        
    @staticmethod
    def parse(text):
        pass

class RejectOfferMessage(Message):
    id = 1037
    def __init__(self):
        pass
        
    @staticmethod
    def parse(text):
        pass

class ClearOfferMessage(Message):
    id = 1038  
    def __init__(self):
        pass
        
    @staticmethod
    def parse(text):
        pass

class AcceptOfferMessage(Message):
    id = 1039 
    def __init__(self):
        pass
        
    @staticmethod
    def parse(text):
        pass

class BankTradeMessage(Message):
    id = 1040
    def __init__(self):
        pass
        
    @staticmethod
    def parse(text):
        pass

class MakeOfferMessage(Message):
    id = 1041
    def __init__(self):
        pass
        
    @staticmethod
    def parse(text):
        pass

class ClearTradeMsgMessage(Message):
    id = 1042
    def __init__(self):
        pass
        
    @staticmethod
    def parse(text):
        pass

class BuildRequestMessage(Message):
    id = 1043
    def __init__(self):
        pass
        
    @staticmethod
    def parse(text):
        pass

class CancelBuildRequestMessage(Message):
    id = 1044 
    def __init__(self):
        pass
        
    @staticmethod
    def parse(text):
        pass

class BuyCardRequestMessage(Message):
    id = 1045  
    def __init__(self):
        pass
        
    @staticmethod
    def parse(text):
        pass

class DevCardMessage(Message):
    id = 1046
    def __init__(self):
        pass
              
    @staticmethod
    def parse(text):
        pass
   
class DevCardCountMessage(Message):
    id = 1047
    def __init__(self):
        pass
        
    @staticmethod
    def parse(text):
        pass

class SetPlayedDevCardMessage(Message):
    id = 1048
    def __init__(self):
        pass
        
    @staticmethod
    def parse(text):
        pass

class PlayDevCardRequestMessage(Message):
    id = 1049
    def __init__(self):
        pass
              
    @staticmethod
    def parse(text):
        pass
   
class DiscoveryPickMessage(Message):
    id = 1052
    def __init__(self):
        pass
        
    @staticmethod
    def parse(text):
        pass

class MonopolyPickMessage(Message):
    id = 1053
    def __init__(self):
        pass
        
    @staticmethod
    def parse(text):
        pass

class FirstPlayerMessage(Message):
    id = 1054
    def __init__(self):
        pass
                 
    @staticmethod
    def parse(text):
        pass

class SetTurnMessage(Message):
    id = 1055
    def __init__(self):
        pass
        
    @staticmethod
    def parse(text):
        pass

class RobotDismissMessage(Message):
    id = 1056
    def __init__(self):
        pass
        
    @staticmethod
    def parse(text):
        pass

class PotentialSettlementsMessage(Message):
    id = 1057
    def __init__(self):
        pass
                 
    @staticmethod
    def parse(text):
        pass

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
        print text
        g, pn, fi = text.split(",")
        return ChangeFaceMessage(g, pn, fi)

class RejectConnectionMessage(Message):
    id = 1059
    def __init__(self):
        pass 
                
    @staticmethod
    def parse(text):
        pass

class LastSettlementMessage(Message):
    id = 1060
    def __init__(self):
        pass
        
    @staticmethod
    def parse(text):
        pass

class GameStatsMessage(Message):
    id = 1061
    def __init__(self):
        pass
        
    @staticmethod
    def parse(text):
        pass

class BCastTextMsgMessage(Message):
    id = 1062
    def __init__(self):
        pass
        
    @staticmethod
    def parse(text):
        pass

class ResourceCountMessage(Message):
    id = 1063
    def __init__(self):
        pass
                
    @staticmethod
    def parse(text):
        pass

class AdminPingMessage(Message):
    id = 1064
    def __init__(self):
        pass
        
    @staticmethod
    def parse(text):
        pass

class AdminResetMessage(Message):
    id = 1065
    def __init__(self):
        pass
        
    @staticmethod
    def parse(text):
        pass

class LongestRoadMessage(Message):
    id = 1066
    def __init__(self):
        pass
        
    @staticmethod
    def parse(text):
        pass

class LargestArmyMessage(Message):
    id = 1067
    def __init__(self):
        pass
        
    @staticmethod
    def parse(text):
        pass

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

class ServerPingMessage(Message):
    id = 9999  
    def __init__(self):
        pass 

    @staticmethod
    def parse(text):
        pass