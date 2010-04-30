class Message:
    def __init__(self):
        pass
        
    def to_cmd(self):
        pass
        
    def values(self):
        vars = filter(lambda x: x not in [
                                "__doc__", "__init__", "__module__"
                              , "to_cmd", "parse", "values", "id"]
                     , dir(self))
        return dict([(name, getattr(self, name)) for name in vars])
        
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
    def __init__(self, game, playernum, piecetype, coords):
        self.game = game
        self.piecetype = piecetype
        self.playernum = playernum
        self.coords = coords
        
    def to_cmd(self):
        return "{0}|{1},{2},{3},{4}".format(self.id, self.game
                                           ,self.playernum, self.piecetype
                                           ,self.coords)
        
    @staticmethod
    def parse(text):
        data = text.split(",")
        return PutPieceMessage(data[0], int(data[1])
                              ,int(data[2]), int(data[3]))

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
                                     ,self.hostname, self.game)
        
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
    def __init__(self, game, hexes, numbers, robberpos):
        self.game = game
        self.hexes = hexes
        self.numbers = numbers
        self.robberpos = robberpos
        
    def to_cmd(self):
        return "{0}|{1},{2},{3},{4}".format(self.id, self.game
                                            ,",".join(self.hexes)
                                            ,",".join(self.numbers)
                                            ,robberpos)
        
    @staticmethod
    def parse(text):
        data = text.split(",")
        game = data[0]
        hexes = map(int, data[1:38])
        numbers = map(int, data[39:39+37])
        robberpos = int(data[-1])
        return BoardLayoutMessage(game, hexes, numbers, robberpos)

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

        from utils import cprint
        output_prefix = "[DEBUG] messages.py ->"

        def debug_print(msg):
            cprint("{0} {1}".format(output_prefix, msg), 'green')
        
        game, playernum, action, element, value = text.split(',')
        ac = PlayerElementMessage.etype[action]
        el = PlayerElementMessage.etype[element]
        if int(playernum) == 1:
            debug_print("Got {0} ({1})".format(element, el))
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
        self.ore = ore
        self.sheep = sheep
        self.wheat = wheat
        self.wood = wood
        self.unknown = unknown
    
    def to_cmd(self):
        return "{0}|{1},{2},{3},{4},{5},{6},{7}".format(self.id, self.game, self.clay, self.ore, self.sheep, self.wheat, self.wood, self.unknown)
    
    @staticmethod
    def parse(text):
        g, c, o, s, wh, wo, u = map(int, text.split(","))
        return DiscardMessage(g, c, o, s, wh, wo, u)
        
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
        return MoveRobberMessage(g, int(pn), int(coords))
 
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

# TODO: FIX!
class MakeOfferMessage(Message):
    id = 1041
    def __init__(self, game, fr, to, give, get):
        self.game = game
        self.fr = fr
        self.to = to
        self.give = give
        self.get = get

    def to_cmd(self):
        return "{0}|{1},{2},{3},{4},{5}".format(self.id, self.game, self.fr
                                                ,','.join(self.to)
                                                ,','.join(self.give)
                                                ,','.join(self.get))
        
    @staticmethod
    def parse(text):
        data = text.split(",")
        game = data[0]
        fr = data[1]
        to = " "
        give = " "
        get = " "
        return MakeOfferMessage(game,fr,to,give,get)

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
        return DevCardMessage(g, int(pn), int(ac), int(ct))
   
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
    def __init__(self, game, playernum):
        self.game = game
        self.playernum = playernum
                 
    def to_cmd(self):
        return "{0}|{1},{2}".format(self.id, self.game, self.playernum)
                 
    @staticmethod
    def parse(text):
        game, playernum = text.split(",")
        return SetTurnMessage(game, int(playernum))

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
