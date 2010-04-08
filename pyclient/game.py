

class Game:
    def __init__(self):
        pass


class NullMessage:
    def __init__(self):
        self.id = 1000

class NewChannelMessage:
    def __init__(self):
        self.id = 1001
        
class MembersMessage:
    def __init__(self):
        self.id = 1002

class ChannelsMessage:
    def __init__(self):
        self.id = 1003
        
class JoinMessage:
    def __init__(self):
        self.id = 1004
        
class TextMsgMessage:
    def __init__(self):
        self.id = 1005

class LeaveMessage:
    def __init__(self):
        self.id = 1006

class DeleteChannelMessage:
    def __init__(self):
        self.id = 1007
        
class LeaveAllMessage:
    def __init__(self):
        self.id = 1008
        
class PutPieceMessage:
    def __init__(self):
        self.id = 1009
        
class GameTextMsgMessage:
    def __init__(self):
        self.id = 1010
        
class LeaveGameMessage:
    def __init__(self):
        self.id = 1011
        
class SitdownMessage:
    def __init__(self):
        self.id = 1012
        
class JoinGameMessage:
    def __init__(self):
        self.id = 1013
        
class BoardLayoutMessage:
    def __init__(self):
        self.id = 1014
        
class DeleteGameMessage:
    def __init__(self):
        self.id = 1015

class NewGameMessage:
    def __init__(self):
        self.id = 1016
        
class GameMembersMessage:
    def __init__(self):
        self.id = 1017

class StartGameMessage:
    def __init__(self):
        self.id = 1018

class GamesMessage:
    def __init__(self):
        self.id = 1019

class JoinAuthMessage:
    def __init__(self):
        self.id = 1020
        
class JoinGameAuthMessage:
    def __init__(self):
        self.id = 1021
        
class ImARobotMessage:
    def __init__(self):
        self.id = 1022

class JoinGameRequestMessage:
    def __init__(self):
        self.id = 1023

class PlayerElementMessage:
    def __init__(self):
        self.id = 1024

class GameStateMessage:
    def __init__(self):
        self.id = 1025

class TurnMessage:
    def __init__(self):
        self.id = 1026

class SetupDoneMessage:
    def __init__(self):
        self.id = 1027

class DiceResultMessage:
    def __init__(self):
        self.id = 1028

class DiscardRequestMessage:
    def __init__(self):
        self.id = 1029
        
class RollDiceRequestMessage:
    def __init__(self):
        self.id = 1030

class RollDiceMessage:
    def __init__(self):
        self.id = 1031

class EndTurnMessage:
    def __init__(self):
        self.id = 1032

class DiscardMessage:
    def __init__(self):
        self.id = 1033

class MoveRobberMessage:
    def __init__(self):
        self.id = 1034
        
class ChoosePlayerMessage:
    def __init__(self):
        self.id = 1035      
        
class ChoosePlayerRequestMessage:
    def __init__(self):
        self.id = 1036

class RejectOfferMessage:
    def __init__(self):
        self.id = 1037

class ClearOfferMessage:
    def __init__(self):
        self.id = 1038  

class AcceptOfferMessage:
    def __init__(self):
        self.id = 1039 

class BankTradeMessage:
    def __init__(self):
        self.id = 1040

class MakeOfferMessage:
    def __init__(self):
        self.id = 1041

class ClearTradeMsgMessage:
    def __init__(self):
        self.id = 1042

class BuildRequestMessage:
    def __init__(self):
        self.id = 1043

class CancelBuildRequestMessage:
    def __init__(self):
        self.id = 1044 

class BuyCardRequestMessage:
    def __init__(self):
        self.id = 1045  

class DevCardMessage:
    def __init__(self):
        self.id = 1046
         
class DevCardCountMessage:
    def __init__(self):
        self.id = 1047

class SetPlayedDevCardMessage:
    def __init__(self):
        self.id = 1048

class PlayDevCardRequestMessage:
    def __init__(self):
        self.id = 1049
         
class DiscoveryPickMessage:
    def __init__(self):
        self.id = 1052

class MonopolyPickMessage:
    def __init__(self):
        self.id = 1053

class FirstPlayerMessage:
    def __init__(self):
        self.id = 1054
         
class SetTurnMessage:
    def __init__(self):
        self.id = 1055

class RobotDismissMessage:
    def __init__(self):
        self.id = 1056

class PotentialSettlementsMessage:
    def __init__(self):
        self.id = 1057
         
class ChangeFaceMessage:
    def __init__(self):
        self.id = 1058

class RejectConnectionMessage:
    def __init__(self):
        self.id = 1059
        
class LastSettlementMessage:
    def __init__(self):
        self.id = 1060

class GameStatsMessage:
    def __init__(self):
        self.id = 1061

class BCastTextMsgMessage:
    def __init__(self):
        self.id = 1062

class ResourceCountMessage:
    def __init__(self):
        self.id = 1063
        
class AdminPingMessage:
    def __init__(self):
        self.id = 1064

class AdminResetMessage:
    def __init__(self):
        self.id = 1065

class LongestRoadMessage:
    def __init__(self):
        self.id = 1066

class LargestArmyMessage:
    def __init__(self):
        self.id = 1067

class SetSeatLockMessage:
    def __init__(self):
        self.id = 1068

class StatusMessageMessage:
    def __init__(self):
        self.id = 1069

class CreateAccountMessage:
    def __init__(self):
        self.id = 1070
        
class UpdateRobotParamsMessage:
    def __init__(self):
        self.id = 1071

class ServerPingMessage:
    def __init__(self):
        self.id = 9999   












def ToMessage(raw_msg):
    msg = raw_msg.decode('utf8')
    
    try:
        sep = msg.find(Sep.SEP1)
        self.id = msg[2:sep]
        rst = msg[sep+1:]
        return (id, rst)
    except:
        return None

def MakeMessage(raw_msg):
    highByte = chr(len(raw_msg) / 256)
    lowByte = chr(len(raw_msg) % 256)
    return highByte + lowByte + raw_msg