"""

class Sep:
    SEP1 = "|"
    SEP2 = ","

class MessageIds:
    NULLMESSAGE = 1000
    NEWCHANNEL = 1001
    MEMBERS = 1002
    CHANNELS = 1003 
    JOIN = 1004 
    TEXTMSG = 1005 
    LEAVE = 1006 
    DELETECHANNEL = 1007 
    LEAVEALL = 1008 
    PUTPIECE = 1009 
    GAMETEXTMSG = 1010 
    LEAVEGAME = 1011 
    SITDOWN = 1012 
    JOINGAME = 1013 
    BOARDLAYOUT = 1014 
    DELETEGAME = 1015 
    NEWGAME = 1016 
    GAMEMEMBERS = 1017 
    STARTGAME = 1018 
    GAMES = 1019 
    JOINAUTH = 1020 
    JOINGAMEAUTH = 1021 
    IMAROBOT = 1022 
    JOINGAMEREQUEST = 1023 
    PLAYERELEMENT = 1024 
    GAMESTATE = 1025 
    TURN = 1026 
    SETUPDONE = 1027 
    DICERESULT = 1028 
    DISCARDREQUEST = 1029 
    ROLLDICEREQUEST = 1030 
    ROLLDICE = 1031 
    ENDTURN = 1032 
    DISCARD = 1033 
    MOVEROBBER = 1034 
    CHOOSEPLAYER = 1035 
    CHOOSEPLAYERREQUEST = 1036 
    REJECTOFFER = 1037 
    CLEAROFFER = 1038 
    ACCEPTOFFER = 1039 
    BANKTRADE = 1040 
    MAKEOFFER = 1041 
    CLEARTRADEMSG = 1042 
    BUILDREQUEST = 1043 
    CANCELBUILDREQUEST = 1044 
    BUYCARDREQUEST = 1045 
    DEVCARD = 1046 
    DEVCARDCOUNT = 1047 
    SETPLAYEDDEVCARD = 1048 
    PLAYDEVCARDREQUEST = 1049 
    DISCOVERYPICK = 1052 
    MONOPOLYPICK = 1053 
    FIRSTPLAYER = 1054 
    SETTURN = 1055 
    ROBOTDISMISS = 1056 
    POTENTIALSETTLEMENTS = 1057 
    CHANGEFACE = 1058 
    REJECTCONNECTION = 1059 
    LASTSETTLEMENT = 1060 
    GAMESTATS = 1061 
    BCASTTEXTMSG = 1062 
    RESOURCECOUNT = 1063 
    ADMINPING = 1064 
    ADMINRESET = 1065 
    LONGESTROAD = 1066 
    LARGESTARMY = 1067 
    SETSEATLOCK = 1068 
    STATUSMESSAGE = 1069 
    CREATEACCOUNT = 1070 
    UPDATEROBOTPARAMS = 1071 
    SERVERPING = 9999 

"""

"""Board-Layout-array*:
[0] = 17
[1] = 39
[2] = 5b
[3] = 7d
[4] = 15
[5] = 37
[6] = 59
[7] = 7b
[8] = 9d
[9] = 13
[10] = 35
[11] = 57
[12] = 79
[13] = 9b
[14] = bd
[15] = 11
[16] = 33
[17] = 55
[18] = 77
[19] = 99
[20] = bb
[21] = dd
[22] = 31
[23] = 53
[24] = 75
[25] = 97
[26] = b9
[27] = db
[28] = 51
[29] = 73
[30] = 95
[31] = b7
[32] = d9
[33] = 71
[34] = 93
[35] = b5
[36] = d7

* Same for Number-array

Board-indicators:
0 = Desert
1 = Clay
2 = Ore
3 = Sheep
4 = Grain
5 = Lumber
6 = EmptySea

7 = 3For1
8 = 3For1
9 = 3For1
10 = 3For1
11 = 3For1
12 = 3For1

17 = ClayHarbor
18 = OreHarbor
19 = SheepHarbor
20 = GrainHarbor
21 = LumberHarbor

33 = ClayHarbor
34 = OreHarbor
35 = SheepHarbor
36 = GrainHarbor
37 = LumberHarbor

49 = ClayHarbor
50 = OreHarbor
51 = SheepHarbor
52 = GrainHarbor
53 = LumberHarbor

65 = ClayHarbor
66 = OreHarbor
67 = SheepHarbor
68 = GrainHarbor
69 = LumberHarbor

81 = ClayHarbor
82 = OreHarbor
83 = SheepHarbor
84 = GrainHarbor
85 = LumberHarbor

97 = ClayHarbor
98 = OreHarbor
99 = SheepHarbor
100 = GrainHarbor
101 = LumberHarbor

Number-indicators:
-1 = Empty
0 = 2
1 = 3
2 = 4
3 = 5
4 = 6
5 = 8
6 = 9
7 = 10
8 = 11
9 = 12

"""

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
    
"""
NEWCHANNEL = 1001
    MEMBERS = 1002
    CHANNELS = 1003 
    JOIN = 1004 
    TEXTMSG = 1005 
    LEAVE = 1006 
    DELETECHANNEL = 1007 
    LEAVEALL = 1008 
    PUTPIECE = 1009 
    GAMETEXTMSG = 1010 
    LEAVEGAME = 1011 
    SITDOWN = 1012 
    JOINGAME = 1013 
    BOARDLAYOUT = 1014 
    DELETEGAME = 1015 
    NEWGAME = 1016 
    GAMEMEMBERS = 1017 
    STARTGAME = 1018 
    GAMES = 1019 
    JOINAUTH = 1020 
    JOINGAMEAUTH = 1021 
    IMAROBOT = 1022 
    JOINGAMEREQUEST = 1023 
    PLAYERELEMENT = 1024 
    GAMESTATE = 1025 
    TURN = 1026 
    SETUPDONE = 1027 
    DICERESULT = 1028 
    DISCARDREQUEST = 1029 
    ROLLDICEREQUEST = 1030 
    ROLLDICE = 1031 
    ENDTURN = 1032 
    DISCARD = 1033 
    MOVEROBBER = 1034 
    CHOOSEPLAYER = 1035 
    CHOOSEPLAYERREQUEST = 1036 
    REJECTOFFER = 1037 
    CLEAROFFER = 1038 
    ACCEPTOFFER = 1039 
    BANKTRADE = 1040 
    MAKEOFFER = 1041 
    CLEARTRADEMSG = 1042 
    BUILDREQUEST = 1043 
    CANCELBUILDREQUEST = 1044 
    BUYCARDREQUEST = 1045 
    DEVCARD = 1046 
    DEVCARDCOUNT = 1047 
    SETPLAYEDDEVCARD = 1048 
    PLAYDEVCARDREQUEST = 1049 
    DISCOVERYPICK = 1052 
    MONOPOLYPICK = 1053 
    FIRSTPLAYER = 1054 
    SETTURN = 1055 
    ROBOTDISMISS = 1056 
    POTENTIALSETTLEMENTS = 1057 
    CHANGEFACE = 1058 
    REJECTCONNECTION = 1059 
    LASTSETTLEMENT = 1060 
    GAMESTATS = 1061 
    BCASTTEXTMSG = 1062 
    RESOURCECOUNT = 1063 
    ADMINPING = 1064 
    ADMINRESET = 1065 
    LONGESTROAD = 1066 
    LARGESTARMY = 1067 
    SETSEATLOCK = 1068 
    STATUSMESSAGE = 1069 
    CREATEACCOUNT = 1070 
    UPDATEROBOTPARAMS = 1071 
    SERVERPING = 9999

"""
"""
       try
        {
            StringTokenizer st = new StringTokenizer(s, sep);

            /**
             * get the id that identifies the type of message
             */
            int msgId = Integer.parseInt(st.nextToken());

            /**
             * get the rest of the data
             */
            String data;

            try
            {
                data = st.nextToken();
            }
            catch (NoSuchElementException e)
            {
                data = "";
            }

            /**
             * convert the data part and create the message
             */
            switch (msgId)
            {
            case NULLMESSAGE:
                return null;

            case NEWCHANNEL:
                return SOCNewChannel.parseDataStr(data);

            case MEMBERS:
                return SOCMembers.parseDataStr(data);

            case CHANNELS:
                return SOCChannels.parseDataStr(data);

            case JOIN:
                return SOCJoin.parseDataStr(data);

            case TEXTMSG:
                return SOCTextMsg.parseDataStr(data);

            case LEAVE:
                return SOCLeave.parseDataStr(data);

            case DELETECHANNEL:
                return SOCDeleteChannel.parseDataStr(data);

            case LEAVEALL:
                return SOCLeaveAll.parseDataStr(data);

            case PUTPIECE:
                return SOCPutPiece.parseDataStr(data);

            case GAMETEXTMSG:
                return SOCGameTextMsg.parseDataStr(data);

            case LEAVEGAME:
                return SOCLeaveGame.parseDataStr(data);

            case SITDOWN:
                return SOCSitDown.parseDataStr(data);

            case JOINGAME:
                return SOCJoinGame.parseDataStr(data);

            case BOARDLAYOUT:
                return SOCBoardLayout.parseDataStr(data);

            case GAMES:
                return SOCGames.parseDataStr(data);

            case DELETEGAME:
                return SOCDeleteGame.parseDataStr(data);

            case NEWGAME:
                return SOCNewGame.parseDataStr(data);

            case GAMEMEMBERS:
                return SOCGameMembers.parseDataStr(data);

            case STARTGAME:
                return SOCStartGame.parseDataStr(data);

            case JOINAUTH:
                return SOCJoinAuth.parseDataStr(data);

            case JOINGAMEAUTH:
                return SOCJoinGameAuth.parseDataStr(data);

            case IMAROBOT:
                return SOCImARobot.parseDataStr(data);

            case JOINGAMEREQUEST:
                return SOCJoinGameRequest.parseDataStr(data);

            case PLAYERELEMENT:
                return SOCPlayerElement.parseDataStr(data);

            case GAMESTATE:
                return SOCGameState.parseDataStr(data);

            case TURN:
                return SOCTurn.parseDataStr(data);

            case SETUPDONE:
                return SOCSetupDone.parseDataStr(data);

            case DICERESULT:
                return SOCDiceResult.parseDataStr(data);

            case DISCARDREQUEST:
                return SOCDiscardRequest.parseDataStr(data);

            case ROLLDICEREQUEST:
                return SOCRollDiceRequest.parseDataStr(data);

            case ROLLDICE:
                return SOCRollDice.parseDataStr(data);

            case ENDTURN:
                return SOCEndTurn.parseDataStr(data);

            case DISCARD:
                return SOCDiscard.parseDataStr(data);

            case MOVEROBBER:
                return SOCMoveRobber.parseDataStr(data);

            case CHOOSEPLAYER:
                return SOCChoosePlayer.parseDataStr(data);

            case CHOOSEPLAYERREQUEST:
                return SOCChoosePlayerRequest.parseDataStr(data);

            case REJECTOFFER:
                return SOCRejectOffer.parseDataStr(data);

            case CLEAROFFER:
                return SOCClearOffer.parseDataStr(data);

            case ACCEPTOFFER:
                return SOCAcceptOffer.parseDataStr(data);

            case BANKTRADE:
                return SOCBankTrade.parseDataStr(data);

            case MAKEOFFER:
                return SOCMakeOffer.parseDataStr(data);

            case CLEARTRADEMSG:
                return SOCClearTradeMsg.parseDataStr(data);

            case BUILDREQUEST:
                return SOCBuildRequest.parseDataStr(data);

            case CANCELBUILDREQUEST:
                return SOCCancelBuildRequest.parseDataStr(data);

            case BUYCARDREQUEST:
                return SOCBuyCardRequest.parseDataStr(data);

            case DEVCARD:
                return SOCDevCard.parseDataStr(data);

            case DEVCARDCOUNT:
                return SOCDevCardCount.parseDataStr(data);

            case SETPLAYEDDEVCARD:
                return SOCSetPlayedDevCard.parseDataStr(data);

            case PLAYDEVCARDREQUEST:
                return SOCPlayDevCardRequest.parseDataStr(data);

            case DISCOVERYPICK:
                return SOCDiscoveryPick.parseDataStr(data);

            case MONOPOLYPICK:
                return SOCMonopolyPick.parseDataStr(data);

            case FIRSTPLAYER:
                return SOCFirstPlayer.parseDataStr(data);

            case SETTURN:
                return SOCSetTurn.parseDataStr(data);

            case ROBOTDISMISS:
                return SOCRobotDismiss.parseDataStr(data);

            case POTENTIALSETTLEMENTS:
                return SOCPotentialSettlements.parseDataStr(data);

            case CHANGEFACE:
                return SOCChangeFace.parseDataStr(data);

            case REJECTCONNECTION:
                return SOCRejectConnection.parseDataStr(data);

            case LASTSETTLEMENT:
                return SOCLastSettlement.parseDataStr(data);

            case GAMESTATS:
                return SOCGameStats.parseDataStr(data);

            case BCASTTEXTMSG:
                return SOCBCastTextMsg.parseDataStr(data);

            case RESOURCECOUNT:
                return SOCResourceCount.parseDataStr(data);

            case ADMINPING:
                return SOCAdminPing.parseDataStr(data);

            case ADMINRESET:
                return SOCAdminReset.parseDataStr(data);

            case LONGESTROAD:
                return SOCLongestRoad.parseDataStr(data);

            case LARGESTARMY:
                return SOCLargestArmy.parseDataStr(data);

            case SETSEATLOCK:
                return SOCSetSeatLock.parseDataStr(data);

            case STATUSMESSAGE:
                return SOCStatusMessage.parseDataStr(data);

            case CREATEACCOUNT:
                return SOCCreateAccount.parseDataStr(data);

            case UPDATEROBOTPARAMS:
                return SOCUpdateRobotParams.parseDataStr(data);

            case SERVERPING:
                return SOCServerPing.parseDataStr(data);

            default:
                return null;
            }
        }
        catch (Exception e)
        {
            System.err.println("toMsg ERROR - " + e);
            e.printStackTrace();

            return null;
        }
    }
"""
