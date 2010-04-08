import pdb

class Game:
    def __init__(self, gameboard):
        self.gameboard = gameboard # save raw gameboad
        self.parse_board()         # parse gameboard and create internal representation
    
    def parse_board(self):
        for elt in self.gameboard:
            print(elt)
            #pass # TODO: parse the gameboard information sent by the server


class Message:
    def __init__(self):
        pass
        
    @staticmethod
    def parse(text):
        return None

class NullMessage(Message):
    id = 1000
    def __init__(self):
        pass
        
    @staticmethod
    def parse(text):
        pass

class NewChannelMessage(Message):
    id = 1001
    def __init__(self):
        pass
         
    @staticmethod
    def parse(text):
        pass
       
class MembersMessage(Message):
    id = 1002
    def __init__(self):
        pass
        
    @staticmethod
    def parse(text):
        pass

# Done
class ChannelsMessage(Message):
    id = 1003
    def __init__(self):
        self.channels = []
            
    @staticmethod
    def parse(text):
        self.channels = text.split(",")
        return self

class JoinMessage(Message):
    id = 1004
    def __init__(self):
        pass
        
    @staticmethod
    def parse(text):
        pass
 
class TextMsgMessage(Message):
    id = 1005
    def __init__(self):
        pass
        
    @staticmethod
    def parse(text):
        pass

class LeaveMessage(Message):
    id = 1006
    def __init__(self):
        pass
        
    @staticmethod
    def parse(text):
        pass

class DeleteChannelMessage(Message):
    id = 1007
    def __init__(self):
        pass
        
    @staticmethod
    def parse(text):
        pass

class LeaveAllMessage(Message):
    id = 1008
    def __init__(self):
        pass
        
    @staticmethod
    def parse(text):
        pass

class PutPieceMessage(Message):
    id = 1009
    def __init__(self):
        pass
        
    @staticmethod
    def parse(text):
        pass

class GameTextMsgMessage(Message):
    id = 1010
    def __init__(self):
        pass
        
    @staticmethod
    def parse(text):
        pass

class LeaveGameMessage(Message):
    id = 1011
    def __init__(self):
        pass
        
    @staticmethod
    def parse(text):
        pass

class SitdownMessage(Message):
    id = 1012
    def __init__(self):
        pass
        
    @staticmethod
    def parse(text):
        pass

class JoinGameMessage(Message):
    id = 1013
    def __init__(self):
        pass
        
    @staticmethod
    def parse(text):
        pass

class BoardLayoutMessage(Message):
    id = 1014
    def __init__(self):
        pass
        
    @staticmethod
    def parse(text):
        pass

class DeleteGameMessage(Message):
    id = 1015
    def __init__(self):
        pass
       
    @staticmethod 
    def parse(text):
        pass


class NewGameMessage(Message):
    id = 1016
    def __init__(self):
        pass
        
    @staticmethod
    def parse(text):
        return NewGameMessage

class GameMembersMessage(Message):
    id = 1017
    def __init__(self):
        pass
        
    @staticmethod
    def parse(text):
        pass

class StartGameMessage(Message):
    id = 1018
    def __init__(self):
        pass
        
    @staticmethod
    def parse(text):
        pass

# Done
class GamesMessage(Message):
    id = 1019
    def __init__(self):
        self.games = []
        
    @staticmethod
    def parse(text):
        self.games = text.split(",")
        return self

class JoinAuthMessage(Message):
    id = 1020
    def __init__(self):
        pass
        
    @staticmethod
    def parse(text):
        pass

class JoinGameAuthMessage(Message):
    id = 1021
    def __init__(self):
        pass
        
    @staticmethod
    def parse(text):
        pass

class ImARobotMessage(Message):
    id = 1022
    def __init__(self):
        pass
        
    @staticmethod
    def parse(text):
        pass

class JoinGameRequestMessage(Message):
    id = 1023
    def __init__(self):
        pass
        
    @staticmethod
    def parse(text):
        pass

class PlayerElementMessage(Message):
    id = 1024
    def __init__(self):
        pass
        
    @staticmethod
    def parse(text):
        pass

class GameStateMessage(Message):
    id = 1025
    def __init__(self):
        pass
        
    @staticmethod
    def parse(text):
        pass

class TurnMessage(Message):
    id = 1026
    def __init__(self):
        pass
        
    @staticmethod
    def parse(text):
        pass

class SetupDoneMessage(Message):
    id = 1027
    def __init__(self):
        pass
        
    @staticmethod
    def parse(text):
        pass

class DiceResultMessage(Message):
    id = 1028
    def __init__(self):
        pass
        
    @staticmethod
    def parse(text):
        pass

class DiscardRequestMessage(Message):
    id = 1029
    def __init__(self):
        pass
        
    @staticmethod
    def parse(text):
        pass

class RollDiceRequestMessage(Message):
    id = 1030
    def __init__(self):
        pass
        
    @staticmethod
    def parse(text):
        pass

class RollDiceMessage(Message):
    id = 1031
    def __init__(self):
        pass
        
    @staticmethod
    def parse(text):
        pass

class EndTurnMessage(Message):
    id = 1032
    def __init__(self):
        pass
        
    @staticmethod
    def parse(text):
        pass

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
    def __init__(self):
        pass
        
    @staticmethod
    def parse(text):
        pass

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



def test():
    i = 0
    for g in globals():
        cg = globals()[g]
        if str(g).endswith("Message") and hasattr(cg, "id"):
            print globals()[g].id
            i += 1
    print i
#    pdb.set_trace()

test()







def ToMessage(raw_msg):
    msg = raw_msg.decode('utf8')
    
    try:
        sep = msg.find(Sep.SEP1)
        id = msg[2:sep]
        rst = msg[sep+1:]
        return (id, rst)
    except:
        return None

def MakeMessage(raw_msg):
    highByte = chr(len(raw_msg) / 256)
    lowByte = chr(len(raw_msg) % 256)
    return highByte + lowByte + raw_msg