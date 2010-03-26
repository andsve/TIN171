/**
 * Java Settlers - An online multiplayer version of the game Settlers of Catan
 * Copyright (C) 2003  Robert S. Thomas
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
 *
 * The author of this program can be reached at thomas@infolab.northwestern.edu
 **/
package soc.robot;

import soc.client.SOCDisplaylessPlayerClient;

import soc.disableDebug.D;

import soc.game.SOCBoard;
import soc.game.SOCGame;
import soc.game.SOCPlayer;

import soc.message.SOCAcceptOffer;
import soc.message.SOCAdminPing;
import soc.message.SOCAdminReset;
import soc.message.SOCBoardLayout;
import soc.message.SOCChangeFace;
import soc.message.SOCChoosePlayerRequest;
import soc.message.SOCClearOffer;
import soc.message.SOCClearTradeMsg;
import soc.message.SOCDeleteGame;
import soc.message.SOCDevCard;
import soc.message.SOCDevCardCount;
import soc.message.SOCDiceResult;
import soc.message.SOCDiscardRequest;
import soc.message.SOCFirstPlayer;
import soc.message.SOCGameMembers;
import soc.message.SOCGameState;
import soc.message.SOCGameTextMsg;
import soc.message.SOCImARobot;
import soc.message.SOCJoinGame;
import soc.message.SOCJoinGameAuth;
import soc.message.SOCJoinGameRequest;
import soc.message.SOCLargestArmy;
import soc.message.SOCLeaveAll;
import soc.message.SOCLeaveGame;
import soc.message.SOCLongestRoad;
import soc.message.SOCMakeOffer;
import soc.message.SOCMessage;
import soc.message.SOCMoveRobber;
import soc.message.SOCPlayerElement;
import soc.message.SOCPotentialSettlements;
import soc.message.SOCPutPiece;
import soc.message.SOCRejectOffer;
import soc.message.SOCResourceCount;
import soc.message.SOCRobotDismiss;
import soc.message.SOCServerPing;
import soc.message.SOCSetPlayedDevCard;
import soc.message.SOCSetTurn;
import soc.message.SOCSitDown;
import soc.message.SOCStartGame;
import soc.message.SOCTurn;
import soc.message.SOCUpdateRobotParams;

import soc.util.CappedQueue;
import soc.util.CutoffExceededException;
import soc.util.SOCRobotParameters;

import java.io.DataInputStream;
import java.io.DataOutputStream;

import java.net.Socket;

import java.util.Enumeration;
import java.util.Hashtable;
import java.util.Vector;


/**
 * This is a client that can play Settlers of Catan.
 *
 * @author Robert S Thomas
 */
public class SOCRobotClient extends SOCDisplaylessPlayerClient
{
    /**
     * constants for debug recording
     */
    public static final String CURRENT_PLANS = "CURRENT_PLANS";
    public static final String CURRENT_RESOURCES = "RESOURCES";

    /**
     * the thread the reads incomming messages
     */
    private Thread reader;

    /**
     * the current robot parameters for robot brains
     */
    private SOCRobotParameters currentRobotParameters;

    /**
     * the robot's "brains" for diferent games
     */
    private Hashtable robotBrains = new Hashtable();

    /**
     * the message queues for the different brains
     */
    private Hashtable brainQs = new Hashtable();

    /**
     * a table of requests from the server to sit at games
     */
    private Hashtable seatRequests = new Hashtable();

    /**
     * number of games this bot has played
     */
    protected int gamesPlayed;

    /**
     * number of games finished
     */
    protected int gamesFinished;

    /**
     * number of games this bot has won
     */
    protected int gamesWon;

    /**
     * number of clean brain kills
     */
    protected int cleanBrainKills;

    /**
     * start time
     */
    protected long startTime;

    /**
     * used to maintain connection
     */
    SOCRobotResetThread resetThread;

    /**
     * Constructor for connecting to the specified host, on the specified port
     *
     * @param h  host
     * @param p  port
     * @param nn nickname for robot
     * @param pw password for robot
     */
    public SOCRobotClient(String h, int p, String nn, String pw)
    {
        gamesPlayed = 0;
        gamesFinished = 0;
        gamesWon = 0;
        cleanBrainKills = 0;
        startTime = System.currentTimeMillis();
        host = h;
        port = p;
        nickname = nn;
        password = pw;
    }

    /**
     * Initialize the robot player
     */
    public void init()
    {
        try
        {
            s = new Socket(host, port);
            s.setSoTimeout(300000);
            in = new DataInputStream(s.getInputStream());
            out = new DataOutputStream(s.getOutputStream());
            connected = true;
            reader = new Thread(this);
            reader.start();

            //resetThread = new SOCRobotResetThread(this);
            //resetThread.start();
            put(SOCImARobot.toCmd(nickname));
        }
        catch (Exception e)
        {
            ex = e;
            System.err.println("Could not connect to the server: " + ex);
        }
    }

    /**
     * disconnect and then try to reconnect
     */
    public void disconnectReconnect()
    {
        D.ebugPrintln("(*)(*)(*)(*)(*)(*)(*) disconnectReconnect()");
        ex = null;

        try
        {
            connected = false;
            s.close();
            s = new Socket(host, port);
            in = new DataInputStream(s.getInputStream());
            out = new DataOutputStream(s.getOutputStream());
            connected = true;
            reader = new Thread(this);
            reader.start();

            //resetThread = new SOCRobotResetThread(this);
            //resetThread.start();
            put(SOCImARobot.toCmd(nickname));
        }
        catch (Exception e)
        {
            ex = e;
            System.err.println("disconnectReconnect error: " + ex);
        }
    }

    /**
     * Treat the incoming messages
     *
     * @param mes    the message
     */
    public void treat(SOCMessage mes)
    {
        D.ebugPrintln("IN - " + mes);

        try
        {
            switch (mes.getType())
            {
            /**
             * server ping
             */
            case SOCMessage.SERVERPING:
                handleSERVERPING((SOCServerPing) mes);

                break;

            /**
             * admin ping
             */
            case SOCMessage.ADMINPING:
                handleADMINPING((SOCAdminPing) mes);

                break;

            /**
             * admin reset
             */
            case SOCMessage.ADMINRESET:
                handleADMINRESET((SOCAdminReset) mes);

                break;

            /**
             * update the current robot parameters
             */
            case SOCMessage.UPDATEROBOTPARAMS:
                handleUPDATEROBOTPARAMS((SOCUpdateRobotParams) mes);

                break;

            /**
             * join game authorization
             */
            case SOCMessage.JOINGAMEAUTH:
                handleJOINGAMEAUTH((SOCJoinGameAuth) mes);

                break;

            /**
             * someone joined a game
             */
            case SOCMessage.JOINGAME:
                handleJOINGAME((SOCJoinGame) mes);

                break;

            /**
             * someone left a game
             */
            case SOCMessage.LEAVEGAME:
                handleLEAVEGAME((SOCLeaveGame) mes);

                break;

            /**
             * game has been destroyed
             */
            case SOCMessage.DELETEGAME:
                handleDELETEGAME((SOCDeleteGame) mes);

                break;

            /**
             * list of game members
             */
            case SOCMessage.GAMEMEMBERS:
                handleGAMEMEMBERS((SOCGameMembers) mes);

                break;

            /**
             * game text message
             */
            case SOCMessage.GAMETEXTMSG:
                handleGAMETEXTMSG((SOCGameTextMsg) mes);

                break;

            /**
             * someone is sitting down
             */
            case SOCMessage.SITDOWN:
                handleSITDOWN((SOCSitDown) mes);

                break;

            /**
             * receive a board layout
             */
            case SOCMessage.BOARDLAYOUT:
                handleBOARDLAYOUT((SOCBoardLayout) mes);

                break;

            /**
             * message that the game is starting
             */
            case SOCMessage.STARTGAME:
                handleSTARTGAME((SOCStartGame) mes);

                break;

            /**
             * update the state of the game
             */
            case SOCMessage.GAMESTATE:
                handleGAMESTATE((SOCGameState) mes);

                break;

            /**
             * set the current turn
             */
            case SOCMessage.SETTURN:
                handleSETTURN((SOCSetTurn) mes);

                break;

            /**
             * set who the first player is
             */
            case SOCMessage.FIRSTPLAYER:
                handleFIRSTPLAYER((SOCFirstPlayer) mes);

                break;

            /**
             * update who's turn it is
             */
            case SOCMessage.TURN:
                handleTURN((SOCTurn) mes);

                break;

            /**
             * receive player information
             */
            case SOCMessage.PLAYERELEMENT:
                handlePLAYERELEMENT((SOCPlayerElement) mes);

                break;

            /**
             * receive resource count
             */
            case SOCMessage.RESOURCECOUNT:
                handleRESOURCECOUNT((SOCResourceCount) mes);

                break;

            /**
             * the latest dice result
             */
            case SOCMessage.DICERESULT:
                handleDICERESULT((SOCDiceResult) mes);

                break;

            /**
             * a player built something
             */
            case SOCMessage.PUTPIECE:
                handlePUTPIECE((SOCPutPiece) mes);

                break;

            /**
             * the robber moved
             */
            case SOCMessage.MOVEROBBER:
                handleMOVEROBBER((SOCMoveRobber) mes);

                break;

            /**
             * the server wants this player to discard
             */
            case SOCMessage.DISCARDREQUEST:
                handleDISCARDREQUEST((SOCDiscardRequest) mes);

                break;

            /**
             * the server wants this player to choose a player to rob
             */
            case SOCMessage.CHOOSEPLAYERREQUEST:
                handleCHOOSEPLAYERREQUEST((SOCChoosePlayerRequest) mes);

                break;

            /**
             * a player has made an offer
             */
            case SOCMessage.MAKEOFFER:
                handleMAKEOFFER((SOCMakeOffer) mes);

                break;

            /**
             * a player has cleared her offer
             */
            case SOCMessage.CLEAROFFER:
                handleCLEAROFFER((SOCClearOffer) mes);

                break;

            /**
             * a player has rejected an offer
             */
            case SOCMessage.REJECTOFFER:
                handleREJECTOFFER((SOCRejectOffer) mes);

                break;

            /**
             * a player has accepted an offer
             */
            case SOCMessage.ACCEPTOFFER:
                handleACCEPTOFFER((SOCAcceptOffer) mes);

                break;

            /**
             * the trade message needs to be cleared
             */
            case SOCMessage.CLEARTRADEMSG:
                handleCLEARTRADEMSG((SOCClearTradeMsg) mes);

                break;

            /**
             * the current number of development cards
             */
            case SOCMessage.DEVCARDCOUNT:
                handleDEVCARDCOUNT((SOCDevCardCount) mes);

                break;

            /**
             * a dev card action, either draw, play, or add to hand
             */
            case SOCMessage.DEVCARD:
                handleDEVCARD((SOCDevCard) mes);

                break;

            /**
             * set the flag that tells if a player has played a
             * development card this turn
             */
            case SOCMessage.SETPLAYEDDEVCARD:
                handleSETPLAYEDDEVCARD((SOCSetPlayedDevCard) mes);

                break;

            /**
             * get a list of all the potential settlements for a player
             */
            case SOCMessage.POTENTIALSETTLEMENTS:
                handlePOTENTIALSETTLEMENTS((SOCPotentialSettlements) mes);

                break;

            /**
             * the server is requesting that we join a game
             */
            case SOCMessage.JOINGAMEREQUEST:
                handleJOINGAMEREQUEST((SOCJoinGameRequest) mes);

                break;

            /**
             * message that means the server wants us to leave the game
             */
            case SOCMessage.ROBOTDISMISS:
                handleROBOTDISMISS((SOCRobotDismiss) mes);

                break;
            }
        }
        catch (Exception e)
        {
            System.out.println("SOCRobotClient treat ERROR - " + e.getMessage());
            e.printStackTrace();
        }
    }

    /**
     * handle the server ping message
     * @param mes  the message
     */
    protected void handleSERVERPING(SOCServerPing mes)
    {
        /*
           D.ebugPrintln("(*)(*) ServerPing message = "+mes);
           D.ebugPrintln("(*)(*) ServerPing sleepTime = "+mes.getSleepTime());
           D.ebugPrintln("(*)(*) resetThread = "+resetThread);
           resetThread.sleepMore();
         */
    }

    /**
     * handle the admin ping message
     * @param mes  the message
     */
    protected void handleADMINPING(SOCAdminPing mes)
    {
        D.ebugPrintln("*** Admin Ping message = " + mes);

        SOCGame ga = (SOCGame) games.get(mes.getGame());

        //
        //  if the robot hears a PING and is in the game
        //  where the admin is, then just say "OK".
        //  otherwise, join the game that the admin is in
        //
        //  note: this is a hack because the bot never 
        //        leaves the game and the game must be 
        //        killed by the admin
        //
        if (ga != null)
        {
            sendText(ga, "OK");
        }
        else
        {
            put(SOCJoinGame.toCmd(nickname, password, host, mes.getGame()));
        }
    }

    /**
     * handle the admin reset message
     * @param mes  the message
     */
    protected void handleADMINRESET(SOCAdminReset mes)
    {
        D.ebugPrintln("*** Admin Reset message = " + mes);
        disconnectReconnect();
    }

    /**
     * handle the update robot params message
     * @param mes  the message
     */
    protected void handleUPDATEROBOTPARAMS(SOCUpdateRobotParams mes)
    {
        currentRobotParameters = new SOCRobotParameters(mes.getRobotParameters());
        D.ebugPrintln("*** current robot parameters = " + currentRobotParameters);
    }

    /**
     * handle the "join game request" message
     * @param mes  the message
     */
    protected void handleJOINGAMEREQUEST(SOCJoinGameRequest mes)
    {
        D.ebugPrintln("**** handleJOINGAMEREQUEST ****");
        seatRequests.put(mes.getGame(), new Integer(mes.getPlayerNumber()));

        if (put(SOCJoinGame.toCmd(nickname, password, host, mes.getGame())))
        {
            D.ebugPrintln("**** sent SOCJoinGame ****");
        }
    }

    /**
     * handle the "join game authorization" message
     * @param mes  the message
     */
    protected void handleJOINGAMEAUTH(SOCJoinGameAuth mes)
    {
        gamesPlayed++;

        SOCGame ga = new SOCGame(mes.getGame(), true);
        games.put(mes.getGame(), ga);

        CappedQueue brainQ = new CappedQueue();
        brainQs.put(mes.getGame(), brainQ);

        SOCRobotBrain rb = new SOCRobotBrain(this, currentRobotParameters, ga, brainQ);
        robotBrains.put(mes.getGame(), rb);
    }

    /**
     * handle the "join game" message
     * @param mes  the message
     */
    protected void handleJOINGAME(SOCJoinGame mes) {}

    /**
     * handle the "leave game" message
     * @param mes  the message
     */
    protected void handleLEAVEGAME(SOCLeaveGame mes) {}

    /**
     * handle the "game members" message
     * @param mes  the message
     */
    protected void handleGAMEMEMBERS(SOCGameMembers mes)
    {
        /**
         * sit down to play
         */
        Integer pn = (Integer) seatRequests.get(mes.getGame());

        try
        {
            //wait(Math.round(Math.random()*1000));
        }
        catch (Exception e)
        {
            ;
        }

        put(SOCSitDown.toCmd(mes.getGame(), nickname, pn.intValue(), true));
    }

    /**
     * handle the "game text message" message
     * @param mes  the message
     */
    protected void handleGAMETEXTMSG(SOCGameTextMsg mes)
    {
        //D.ebugPrintln(mes.getNickname()+": "+mes.getText());
        if (mes.getText().startsWith(nickname + ":debug-off"))
        {
            SOCGame ga = (SOCGame) games.get(mes.getGame());
            SOCRobotBrain brain = (SOCRobotBrain) robotBrains.get(mes.getGame());

            if (brain != null)
            {
                brain.turnOffDRecorder();
                sendText(ga, "Debug mode OFF");
            }
        }

        if (mes.getText().startsWith(nickname + ":debug-on"))
        {
            SOCGame ga = (SOCGame) games.get(mes.getGame());
            SOCRobotBrain brain = (SOCRobotBrain) robotBrains.get(mes.getGame());

            if (brain != null)
            {
                brain.turnOnDRecorder();
                sendText(ga, "Debug mode ON");
            }
        }

        if (mes.getText().startsWith(nickname + ":current-plans") || mes.getText().startsWith(nickname + ":cp"))
        {
            SOCGame ga = (SOCGame) games.get(mes.getGame());
            SOCRobotBrain brain = (SOCRobotBrain) robotBrains.get(mes.getGame());

            if ((brain != null) && (brain.getDRecorder().isOn()))
            {
                Vector record = brain.getDRecorder().getRecord(CURRENT_PLANS);

                if (record != null)
                {
                    Enumeration enum = record.elements();

                    while (enum.hasMoreElements())
                    {
                        String str = (String) enum.nextElement();
                        sendText(ga, str);
                    }
                }
            }
        }

        if (mes.getText().startsWith(nickname + ":current-resources") || mes.getText().startsWith(nickname + ":cr"))
        {
            SOCGame ga = (SOCGame) games.get(mes.getGame());
            SOCRobotBrain brain = (SOCRobotBrain) robotBrains.get(mes.getGame());

            if ((brain != null) && (brain.getDRecorder().isOn()))
            {
                Vector record = brain.getDRecorder().getRecord(CURRENT_RESOURCES);

                if (record != null)
                {
                    Enumeration enum = record.elements();

                    while (enum.hasMoreElements())
                    {
                        String str = (String) enum.nextElement();
                        sendText(ga, str);
                    }
                }
            }
        }

        if (mes.getText().startsWith(nickname + ":last-plans") || mes.getText().startsWith(nickname + ":lp"))
        {
            SOCRobotBrain brain = (SOCRobotBrain) robotBrains.get(mes.getGame());

            if ((brain != null) && (brain.getDRecorder().isOn()))
            {
                Vector record = brain.getOldDRecorder().getRecord(CURRENT_PLANS);

                if (record != null)
                {
                    SOCGame ga = (SOCGame) games.get(mes.getGame());
                    Enumeration enum = record.elements();

                    while (enum.hasMoreElements())
                    {
                        String str = (String) enum.nextElement();
                        sendText(ga, str);
                    }
                }
            }
        }

        if (mes.getText().startsWith(nickname + ":last-resources") || mes.getText().startsWith(nickname + ":lr"))
        {
            SOCRobotBrain brain = (SOCRobotBrain) robotBrains.get(mes.getGame());

            if ((brain != null) && (brain.getDRecorder().isOn()))
            {
                Vector record = brain.getOldDRecorder().getRecord(CURRENT_RESOURCES);

                if (record != null)
                {
                    SOCGame ga = (SOCGame) games.get(mes.getGame());
                    Enumeration enum = record.elements();

                    while (enum.hasMoreElements())
                    {
                        String str = (String) enum.nextElement();
                        sendText(ga, str);
                    }
                }
            }
        }

        if (mes.getText().startsWith(nickname + ":last-move") || mes.getText().startsWith(nickname + ":lm"))
        {
            SOCRobotBrain brain = (SOCRobotBrain) robotBrains.get(mes.getGame());

            if ((brain != null) && (brain.getOldDRecorder().isOn()))
            {
                SOCPossiblePiece lastMove = brain.getLastMove();

                if (lastMove != null)
                {
                    String key = null;

                    switch (lastMove.getType())
                    {
                    case SOCPossiblePiece.CARD:
                        key = "DEVCARD";

                        break;

                    case SOCPossiblePiece.ROAD:
                        key = "ROAD" + lastMove.getCoordinates();

                        break;

                    case SOCPossiblePiece.SETTLEMENT:
                        key = "SETTLEMENT" + lastMove.getCoordinates();

                        break;

                    case SOCPossiblePiece.CITY:
                        key = "CITY" + lastMove.getCoordinates();

                        break;
                    }

                    Vector record = brain.getOldDRecorder().getRecord(key);

                    if (record != null)
                    {
                        SOCGame ga = (SOCGame) games.get(mes.getGame());
                        Enumeration enum = record.elements();

                        while (enum.hasMoreElements())
                        {
                            String str = (String) enum.nextElement();
                            sendText(ga, str);
                        }
                    }
                }
            }
        }

        if (mes.getText().startsWith(nickname + ":consider-move ") || mes.getText().startsWith(nickname + ":cm "))
        {
            SOCRobotBrain brain = (SOCRobotBrain) robotBrains.get(mes.getGame());

            if ((brain != null) && (brain.getOldDRecorder().isOn()))
            {
                String[] tokens = mes.getText().split(" ");
                String key = null;

                if (tokens[1].trim().equals("card"))
                {
                    key = "DEVCARD";
                }
                else if (tokens[1].equals("road"))
                {
                    key = "ROAD" + tokens[2].trim();
                }
                else if (tokens[1].equals("settlement"))
                {
                    key = "SETTLEMENT" + tokens[2].trim();
                }
                else if (tokens[1].equals("city"))
                {
                    key = "CITY" + tokens[2].trim();
                }

                Vector record = brain.getOldDRecorder().getRecord(key);

                if (record != null)
                {
                    SOCGame ga = (SOCGame) games.get(mes.getGame());
                    Enumeration enum = record.elements();

                    while (enum.hasMoreElements())
                    {
                        String str = (String) enum.nextElement();
                        sendText(ga, str);
                    }
                }
            }
        }

        if (mes.getText().startsWith(nickname + ":last-target") || mes.getText().startsWith(nickname + ":lt"))
        {
            SOCRobotBrain brain = (SOCRobotBrain) robotBrains.get(mes.getGame());

            if ((brain != null) && (brain.getDRecorder().isOn()))
            {
                SOCPossiblePiece lastTarget = brain.getLastTarget();

                if (lastTarget != null)
                {
                    String key = null;

                    switch (lastTarget.getType())
                    {
                    case SOCPossiblePiece.CARD:
                        key = "DEVCARD";

                        break;

                    case SOCPossiblePiece.ROAD:
                        key = "ROAD" + lastTarget.getCoordinates();

                        break;

                    case SOCPossiblePiece.SETTLEMENT:
                        key = "SETTLEMENT" + lastTarget.getCoordinates();

                        break;

                    case SOCPossiblePiece.CITY:
                        key = "CITY" + lastTarget.getCoordinates();

                        break;
                    }

                    Vector record = brain.getDRecorder().getRecord(key);

                    if (record != null)
                    {
                        SOCGame ga = (SOCGame) games.get(mes.getGame());
                        Enumeration enum = record.elements();

                        while (enum.hasMoreElements())
                        {
                            String str = (String) enum.nextElement();
                            sendText(ga, str);
                        }
                    }
                }
            }
        }

        if (mes.getText().startsWith(nickname + ":consider-target ") || mes.getText().startsWith(nickname + ":ct "))
        {
            SOCRobotBrain brain = (SOCRobotBrain) robotBrains.get(mes.getGame());

            if ((brain != null) && (brain.getDRecorder().isOn()))
            {
                String[] tokens = mes.getText().split(" ");
                String key = null;

                if (tokens[1].trim().equals("card"))
                {
                    key = "DEVCARD";
                }
                else if (tokens[1].equals("road"))
                {
                    key = "ROAD" + tokens[2].trim();
                }
                else if (tokens[1].equals("settlement"))
                {
                    key = "SETTLEMENT" + tokens[2].trim();
                }
                else if (tokens[1].equals("city"))
                {
                    key = "CITY" + tokens[2].trim();
                }

                Vector record = brain.getDRecorder().getRecord(key);

                if (record != null)
                {
                    SOCGame ga = (SOCGame) games.get(mes.getGame());
                    Enumeration enum = record.elements();

                    while (enum.hasMoreElements())
                    {
                        String str = (String) enum.nextElement();
                        sendText(ga, str);
                    }
                }
            }
        }

        if (mes.getText().startsWith(nickname + ":stats"))
        {
            SOCGame ga = (SOCGame) games.get(mes.getGame());
            sendText(ga, "Games played:" + gamesPlayed);
            sendText(ga, "Games finished:" + gamesFinished);
            sendText(ga, "Games won:" + gamesWon);
            sendText(ga, "Clean brain kills:" + cleanBrainKills);
            sendText(ga, "Brains running: " + robotBrains.size());

            Runtime rt = Runtime.getRuntime();
            sendText(ga, "Total Memory:" + rt.totalMemory());
            sendText(ga, "Free Memory:" + rt.freeMemory());
        }

        if (mes.getText().startsWith(nickname + ":gc"))
        {
            SOCGame ga = (SOCGame) games.get(mes.getGame());
            Runtime rt = Runtime.getRuntime();
            rt.gc();
            sendText(ga, "Free Memory:" + rt.freeMemory());
        }

        CappedQueue brainQ = (CappedQueue) brainQs.get(mes.getGame());

        if (brainQ != null)
        {
            try
            {
                brainQ.put(mes);
            }
            catch (CutoffExceededException exc)
            {
                D.ebugPrintln("CutoffExceededException" + exc);
            }
        }
    }

    /**
     * handle the "someone is sitting down" message
     * @param mes  the message
     */
    protected void handleSITDOWN(SOCSitDown mes)
    {
        /**
         * tell the game that a player is sitting
         */
        SOCGame ga = (SOCGame) games.get(mes.getGame());

        if (ga != null)
        {
            ga.addPlayer(mes.getNickname(), mes.getPlayerNumber());

            /**
             * set the robot flag
             */
            ga.getPlayer(mes.getPlayerNumber()).setRobotFlag(mes.isRobot());

            /**
             * let the robot brain find our player object if we sat down
             */
            if (nickname.equals(mes.getNickname()))
            {
                SOCRobotBrain brain = (SOCRobotBrain) robotBrains.get(mes.getGame());
                brain.setOurPlayerData();
                brain.start();

                /**
                 * change our face to the robot face
                 */
                put(SOCChangeFace.toCmd(ga.getName(), mes.getPlayerNumber(), 0));
            }
        }
    }

    /**
     * handle the "board layout" message
     * @param mes  the message
     */
    protected void handleBOARDLAYOUT(SOCBoardLayout mes)
    {
        SOCGame ga = (SOCGame) games.get(mes.getGame());

        if (ga != null)
        {
            SOCBoard bd = ga.getBoard();
            bd.setHexLayout(mes.getHexLayout());
            bd.setNumberLayout(mes.getNumberLayout());
            bd.setRobberHex(mes.getRobberHex());
        }
    }

    /**
     * handle the "start game" message
     * @param mes  the message
     */
    protected void handleSTARTGAME(SOCStartGame mes) {}

    /**
     * handle the "delete game" message
     * @param mes  the message
     */
    protected void handleDELETEGAME(SOCDeleteGame mes)
    {
        SOCRobotBrain brain = (SOCRobotBrain) robotBrains.get(mes.getGame());

        if (brain != null)
        {
            SOCGame ga = (SOCGame) games.get(mes.getGame());

            if (ga != null)
            {
                if (ga.getGameState() == SOCGame.OVER)
                {
                    gamesFinished++;

                    if (ga.getPlayer(nickname).getTotalVP() >= 10)
                    {
                        gamesWon++;
                    }
                }

                brain.kill();
                robotBrains.remove(mes.getGame());
                brainQs.remove(mes.getGame());
                games.remove(mes.getGame());
            }
        }
    }

    /**
     * handle the "game state" message
     * @param mes  the message
     */
    protected void handleGAMESTATE(SOCGameState mes)
    {
        SOCGame ga = (SOCGame) games.get(mes.getGame());

        if (ga != null)
        {
            CappedQueue brainQ = (CappedQueue) brainQs.get(mes.getGame());

            if (brainQ != null)
            {
                try
                {
                    brainQ.put(mes);
                }
                catch (CutoffExceededException exc)
                {
                    D.ebugPrintln("CutoffExceededException" + exc);
                }
            }
        }
    }

    /**
     * handle the "set turn" message
     * @param mes  the message
     */
    protected void handleSETTURN(SOCSetTurn mes)
    {
        CappedQueue brainQ = (CappedQueue) brainQs.get(mes.getGame());

        if (brainQ != null)
        {
            try
            {
                brainQ.put(mes);
            }
            catch (CutoffExceededException exc)
            {
                D.ebugPrintln("CutoffExceededException" + exc);
            }
        }
    }

    /**
     * handle the "set first player" message
     * @param mes  the message
     */
    protected void handleFIRSTPLAYER(SOCFirstPlayer mes)
    {
        CappedQueue brainQ = (CappedQueue) brainQs.get(mes.getGame());

        if (brainQ != null)
        {
            try
            {
                brainQ.put(mes);
            }
            catch (CutoffExceededException exc)
            {
                D.ebugPrintln("CutoffExceededException" + exc);
            }
        }
    }

    /**
     * handle the "turn" message
     * @param mes  the message
     */
    protected void handleTURN(SOCTurn mes)
    {
        CappedQueue brainQ = (CappedQueue) brainQs.get(mes.getGame());

        if (brainQ != null)
        {
            try
            {
                brainQ.put(mes);
            }
            catch (CutoffExceededException exc)
            {
                D.ebugPrintln("CutoffExceededException" + exc);
            }
        }
    }

    /**
     * handle the "player element" message
     * @param mes  the message
     */
    protected void handlePLAYERELEMENT(SOCPlayerElement mes)
    {
        CappedQueue brainQ = (CappedQueue) brainQs.get(mes.getGame());

        if (brainQ != null)
        {
            try
            {
                brainQ.put(mes);
            }
            catch (CutoffExceededException exc)
            {
                D.ebugPrintln("CutoffExceededException" + exc);
            }
        }
    }

    /**
     * handle "resource count" message
     * @param mes  the message
     */
    protected void handleRESOURCECOUNT(SOCResourceCount mes)
    {
        CappedQueue brainQ = (CappedQueue) brainQs.get(mes.getGame());

        if (brainQ != null)
        {
            try
            {
                brainQ.put(mes);
            }
            catch (CutoffExceededException exc)
            {
                D.ebugPrintln("CutoffExceededException" + exc);
            }
        }
    }

    /**
     * handle the "dice result" message
     * @param mes  the message
     */
    protected void handleDICERESULT(SOCDiceResult mes)
    {
        CappedQueue brainQ = (CappedQueue) brainQs.get(mes.getGame());

        if (brainQ != null)
        {
            try
            {
                brainQ.put(mes);
            }
            catch (CutoffExceededException exc)
            {
                D.ebugPrintln("CutoffExceededException" + exc);
            }
        }
    }

    /**
     * handle the "put piece" message
     * @param mes  the message
     */
    protected void handlePUTPIECE(SOCPutPiece mes)
    {
        CappedQueue brainQ = (CappedQueue) brainQs.get(mes.getGame());

        if (brainQ != null)
        {
            try
            {
                brainQ.put(mes);
            }
            catch (CutoffExceededException exc)
            {
                D.ebugPrintln("CutoffExceededException" + exc);
            }

            SOCGame ga = (SOCGame) games.get(mes.getGame());

            if (ga != null)
            {
                SOCPlayer pl = ga.getPlayer(mes.getPlayerNumber());
            }
        }
    }

    /**
     * handle the "move robber" message
     * @param mes  the message
     */
    protected void handleMOVEROBBER(SOCMoveRobber mes)
    {
        CappedQueue brainQ = (CappedQueue) brainQs.get(mes.getGame());

        if (brainQ != null)
        {
            try
            {
                brainQ.put(mes);
            }
            catch (CutoffExceededException exc)
            {
                D.ebugPrintln("CutoffExceededException" + exc);
            }
        }
    }

    /**
     * handle the "discard request" message
     * @param mes  the message
     */
    protected void handleDISCARDREQUEST(SOCDiscardRequest mes)
    {
        CappedQueue brainQ = (CappedQueue) brainQs.get(mes.getGame());

        if (brainQ != null)
        {
            try
            {
                brainQ.put(mes);
            }
            catch (CutoffExceededException exc)
            {
                D.ebugPrintln("CutoffExceededException" + exc);
            }
        }
    }

    /**
     * handle the "choose player request" message
     * @param mes  the message
     */
    protected void handleCHOOSEPLAYERREQUEST(SOCChoosePlayerRequest mes)
    {
        CappedQueue brainQ = (CappedQueue) brainQs.get(mes.getGame());

        if (brainQ != null)
        {
            try
            {
                brainQ.put(mes);
            }
            catch (CutoffExceededException exc)
            {
                D.ebugPrintln("CutoffExceededException" + exc);
            }
        }
    }

    /**
     * handle the "make offer" message
     * @param mes  the message
     */
    protected void handleMAKEOFFER(SOCMakeOffer mes)
    {
        CappedQueue brainQ = (CappedQueue) brainQs.get(mes.getGame());

        if (brainQ != null)
        {
            try
            {
                brainQ.put(mes);
            }
            catch (CutoffExceededException exc)
            {
                D.ebugPrintln("CutoffExceededException" + exc);
            }
        }
    }

    /**
     * handle the "clear offer" message
     * @param mes  the message
     */
    protected void handleCLEAROFFER(SOCClearOffer mes)
    {
        CappedQueue brainQ = (CappedQueue) brainQs.get(mes.getGame());

        if (brainQ != null)
        {
            try
            {
                brainQ.put(mes);
            }
            catch (CutoffExceededException exc)
            {
                D.ebugPrintln("CutoffExceededException" + exc);
            }
        }
    }

    /**
     * handle the "reject offer" message
     * @param mes  the message
     */
    protected void handleREJECTOFFER(SOCRejectOffer mes)
    {
        CappedQueue brainQ = (CappedQueue) brainQs.get(mes.getGame());

        if (brainQ != null)
        {
            try
            {
                brainQ.put(mes);
            }
            catch (CutoffExceededException exc)
            {
                D.ebugPrintln("CutoffExceededException" + exc);
            }
        }
    }

    /**
     * handle the "accept offer" message
     * @param mes  the message
     */
    protected void handleACCEPTOFFER(SOCAcceptOffer mes)
    {
        CappedQueue brainQ = (CappedQueue) brainQs.get(mes.getGame());

        if (brainQ != null)
        {
            try
            {
                brainQ.put(mes);
            }
            catch (CutoffExceededException exc)
            {
                D.ebugPrintln("CutoffExceededException" + exc);
            }
        }
    }

    /**
     * handle the "clear trade" message
     * @param mes  the message
     */
    protected void handleCLEARTRADEMSG(SOCClearTradeMsg mes) {}

    /**
     * handle the "development card count" message
     * @param mes  the message
     */
    protected void handleDEVCARDCOUNT(SOCDevCardCount mes)
    {
        CappedQueue brainQ = (CappedQueue) brainQs.get(mes.getGame());

        if (brainQ != null)
        {
            try
            {
                brainQ.put(mes);
            }
            catch (CutoffExceededException exc)
            {
                D.ebugPrintln("CutoffExceededException" + exc);
            }
        }
    }

    /**
     * handle the "development card action" message
     * @param mes  the message
     */
    protected void handleDEVCARD(SOCDevCard mes)
    {
        CappedQueue brainQ = (CappedQueue) brainQs.get(mes.getGame());

        if (brainQ != null)
        {
            try
            {
                brainQ.put(mes);
            }
            catch (CutoffExceededException exc)
            {
                D.ebugPrintln("CutoffExceededException" + exc);
            }
        }
    }

    /**
     * handle the "set played development card" message
     * @param mes  the message
     */
    protected void handleSETPLAYEDDEVCARD(SOCSetPlayedDevCard mes)
    {
        CappedQueue brainQ = (CappedQueue) brainQs.get(mes.getGame());

        if (brainQ != null)
        {
            try
            {
                brainQ.put(mes);
            }
            catch (CutoffExceededException exc)
            {
                D.ebugPrintln("CutoffExceededException" + exc);
            }
        }
    }

    /**
     * handle the "dismiss robot" message
     * @param mes  the message
     */
    protected void handleROBOTDISMISS(SOCRobotDismiss mes)
    {
        SOCGame ga = (SOCGame) games.get(mes.getGame());
        CappedQueue brainQ = (CappedQueue) brainQs.get(mes.getGame());

        if ((ga != null) && (brainQ != null))
        {
            try
            {
                brainQ.put(mes);
            }
            catch (CutoffExceededException exc)
            {
                D.ebugPrintln("CutoffExceededException" + exc);
            }

            /**
             * if the brain isn't alive, then we need to leave
             * the game
             */
            SOCRobotBrain brain = (SOCRobotBrain) robotBrains.get(mes.getGame());

            if ((brain == null) || (!brain.isAlive()))
            {
                leaveGame((SOCGame) games.get(mes.getGame()));
            }
        }
    }

    /**
     * handle the "potential settlements" message
     * @param mes  the message
     */
    protected void handlePOTENTIALSETTLEMENTS(SOCPotentialSettlements mes)
    {
        CappedQueue brainQ = (CappedQueue) brainQs.get(mes.getGame());

        if (brainQ != null)
        {
            try
            {
                brainQ.put(mes);
            }
            catch (CutoffExceededException exc)
            {
                D.ebugPrintln("CutoffExceededException" + exc);
            }
        }
    }

    /**
     * handle the "change face" message
     * @param mes  the message
     */
    protected void handleCHANGEFACE(SOCChangeFace mes)
    {
        SOCGame ga = (SOCGame) games.get(mes.getGame());

        if (ga != null)
        {
            SOCPlayer player = ga.getPlayer(mes.getPlayerNumber());
            player.setFaceId(mes.getFaceId());
        }
    }

    /**
     * handle the "longest road" message
     * @param mes  the message
     */
    protected void handleLONGESTROAD(SOCLongestRoad mes)
    {
        SOCGame ga = (SOCGame) games.get(mes.getGame());

        if (ga != null)
        {
            if (mes.getPlayerNumber() == -1)
            {
                ga.setPlayerWithLongestRoad((SOCPlayer) null);
            }
            else
            {
                ga.setPlayerWithLongestRoad(ga.getPlayer(mes.getPlayerNumber()));
            }
        }
    }

    /**
     * handle the "largest army" message
     * @param mes  the message
     */
    protected void handleLARGESTARMY(SOCLargestArmy mes)
    {
        SOCGame ga = (SOCGame) games.get(mes.getGame());

        if (ga != null)
        {
            if (mes.getPlayerNumber() == -1)
            {
                ga.setPlayerWithLargestArmy((SOCPlayer) null);
            }
            else
            {
                ga.setPlayerWithLargestArmy(ga.getPlayer(mes.getPlayerNumber()));
            }
        }
    }

    /**
     * the user leaves the given game
     *
     * @param ga   the game
     */
    public void leaveGame(SOCGame ga)
    {
        if (ga != null)
        {
            robotBrains.remove(ga.getName());
            brainQs.remove(ga.getName());
            games.remove(ga.getName());
            put(SOCLeaveGame.toCmd(nickname, host, ga.getName()));
        }
    }

    /**
     * add one the the number of clean brain kills
     */
    public void addCleanKill()
    {
        cleanBrainKills++;
    }

    /** destroy the applet */
    public void destroy()
    {
        SOCLeaveAll leaveAllMes = new SOCLeaveAll();
        put(leaveAllMes.toCmd());
        disconnectReconnect();
    }

    /**
     * for stand-alones
     */
    public static void main(String[] args)
    {
		if (args.length < 4)
		{
			System.err.println("usage: java soc.robot.SOCRobotClient host port_number userid password");

			return;
		}
    	
        SOCRobotClient ex1 = new SOCRobotClient(args[0], Integer.parseInt(args[1]), args[2], args[3]);
        ex1.init();
    }
}
