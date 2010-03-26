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
package soc.game;

import soc.disableDebug.D;

import soc.util.IntPair;
import soc.util.NodeLenVis;

import java.io.Serializable;

import java.util.Enumeration;
import java.util.Stack;
import java.util.Vector;


/**
 * A class for holding and manipulating player data
 *
 * @author Robert S Thomas
 */
public class SOCPlayer implements SOCResourceConstants, SOCDevCardConstants, Serializable, Cloneable
{
    /**
     * the name of the player
     */
    private String name;

    /**
     * the integer id for this player
     */
    private int playerNumber;

    /**
     * the game that this player is in
     */
    private SOCGame game;

    /**
     * the number of pieces not in play
     */
    private int[] numPieces;

    /**
     * a list of this player's pieces in play
     */
    private Vector pieces;

    /**
     * a list of this player's roads in play
     */
    private Vector roads;

    /**
     * a list of this player's settlements in play
     */
    private Vector settlements;

    /**
     * a list of this player's cities in play
     */
    private Vector cities;

    /**
     * The coordinates of our most recent settlement
     */
    protected int lastSettlementCoord;

    /**
     * The coordinates of our most recent road
     */
    protected int lastRoadCoord;

    /**
     * length of the longest road for this player
     */
    private int longestRoadLength;

    /**
     * list of longest paths
     */
    private Vector lrPaths;

    /**
     * how many of each resource this player has
     */
    private SOCResourceSet resources;

    /**
     * how many of each type of development card this player has
     */
    private SOCDevCardSet devCards;

    /**
     * how many knights this player has in play
     */
    private int numKnights;

    /**
     * the number of victory points for settlements and cities
     */
    private int buildingVP;

    /**
     * the number of development card victory points
     */
    private int devCardVP;

    /**
     * this flag is true if the player needs to discard
     */
    private boolean needToDiscard;

    /**
     * all of the nodes that this player's roads touch
     * this is used to calculate longest road
     */
    private Vector roadNodes;

    /**
     * a graph of what nodes are connected by this
     * player's roads
     */
    private boolean[][] roadNodeGraph;

    /**
     * a list of edges where it is legal to place a road.
     * an edge is legal if a road could eventually be
     * placed there.
     */
    private boolean[] legalRoads;

    /**
     * a list of nodes where it is legal to place a
     * settlement.        a node is legal if a settlement
     * could eventually be placed there.
     */
    private boolean[] legalSettlements;

    /**
     * a list of edges where a road could be placed
     * on the next turn.
     */
    private boolean[] potentialRoads;

    /**
     * a list of nodes where a settlement could be
     * placed on the next turn.
     */
    private boolean[] potentialSettlements;

    /**
     * a list of nodes where a city could be
     * placed on the next turn.
     */
    private boolean[] potentialCities;

    /**
     * a boolean array stating wheather this player is touching a
     * particular kind of port
     */
    private boolean[] ports;

    /**
     * this is the current trade offer that this player is making
     */
    private SOCTradeOffer currentOffer;

    /**
     * this is true if the player played a development card this turn
     */
    private boolean playedDevCard;

    /**
     * this is true if this player is a robot
     */
    private boolean robotFlag;

    /**
     * which face image this player is using
     */
    private int faceId;

    /**
     * the numbers that our settlements are touching
     */
    private SOCPlayerNumbers ourNumbers;

    /**
     * a guess at how many turns it takes to build
     */

    // private SOCBuildingSpeedEstimate buildingSpeed;

    /**
     * create a copy of the player
     *
     * @param player        the player to copy
     */
    public SOCPlayer(SOCPlayer player)
    {
        int i;
        int j;
        game = player.game;
        playerNumber = player.playerNumber;
        numPieces = new int[SOCPlayingPiece.MAXPLUSONE];
        numPieces[SOCPlayingPiece.ROAD] = player.numPieces[SOCPlayingPiece.ROAD];
        numPieces[SOCPlayingPiece.SETTLEMENT] = player.numPieces[SOCPlayingPiece.SETTLEMENT];
        numPieces[SOCPlayingPiece.CITY] = player.numPieces[SOCPlayingPiece.CITY];
        pieces = (Vector) player.pieces.clone();
        roads = (Vector) player.roads.clone();
        settlements = (Vector) player.settlements.clone();
        cities = (Vector) player.cities.clone();
        longestRoadLength = player.longestRoadLength;
        lrPaths = (Vector) player.lrPaths.clone();
        resources = player.resources.copy();
        devCards = new SOCDevCardSet(player.devCards);
        numKnights = player.numKnights;
        buildingVP = player.buildingVP;
        devCardVP = player.devCardVP;
        playedDevCard = player.playedDevCard;
        needToDiscard = player.needToDiscard;
        robotFlag = player.robotFlag;
        faceId = player.faceId;
        ourNumbers = new SOCPlayerNumbers(player.ourNumbers);
        ports = new boolean[SOCBoard.WOOD_PORT + 1];

        for (i = SOCBoard.MISC_PORT; i <= SOCBoard.WOOD_PORT; i++)
        {
            ports[i] = player.ports[i];
        }

        roadNodes = (Vector) player.roadNodes.clone();
        roadNodeGraph = new boolean[SOCBoard.MAXNODEPLUSONE][SOCBoard.MAXNODEPLUSONE];

        for (i = SOCBoard.MINNODE; i < SOCBoard.MAXNODEPLUSONE; i++)
        {
            for (j = SOCBoard.MINNODE; j < SOCBoard.MAXNODEPLUSONE; j++)
            {
                roadNodeGraph[i][j] = player.roadNodeGraph[i][j];
            }
        }

        /**
         * init legal and potential arrays
         */
        legalRoads = new boolean[0xEF];
        legalSettlements = new boolean[0xFF];
        potentialRoads = new boolean[0xEF];
        potentialSettlements = new boolean[0xFF];
        potentialCities = new boolean[0xFF];

        for (i = 0; i < 0xEF; i++)
        {
            legalRoads[i] = player.legalRoads[i];
            potentialRoads[i] = player.potentialRoads[i];
        }

        for (i = 0; i < 0xFF; i++)
        {
            legalSettlements[i] = player.legalSettlements[i];
            potentialSettlements[i] = player.potentialSettlements[i];
            potentialCities[i] = player.potentialCities[i];
        }

        if (player.currentOffer != null)
        {
            currentOffer = new SOCTradeOffer(player.currentOffer);
        }
        else
        {
            currentOffer = null;
        }
    }

    /**
     * create a new player
     *
     * @param pn the player number
     * @param ga the game that the player is in
     */
    public SOCPlayer(int pn, SOCGame ga)
    {
        int i;
        int j;

        game = ga;
        playerNumber = pn;
        numPieces = new int[SOCPlayingPiece.MAXPLUSONE];
        numPieces[SOCPlayingPiece.ROAD] = 15;
        numPieces[SOCPlayingPiece.SETTLEMENT] = 5;
        numPieces[SOCPlayingPiece.CITY] = 4;
        pieces = new Vector(24);
        roads = new Vector(15);
        settlements = new Vector(5);
        cities = new Vector(4);
        longestRoadLength = 0;
        lrPaths = new Vector();
        resources = new SOCResourceSet();
        devCards = new SOCDevCardSet();
        numKnights = 0;
        buildingVP = 0;
        devCardVP = 0;
        playedDevCard = false;
        needToDiscard = false;
        robotFlag = false;
        faceId = 1;
        ourNumbers = new SOCPlayerNumbers();

        // buildingSpeed = new SOCBuildingSpeedEstimate(this);
        ports = new boolean[SOCBoard.WOOD_PORT + 1];

        for (i = SOCBoard.MISC_PORT; i <= SOCBoard.WOOD_PORT; i++)
        {
            ports[i] = false;
        }

        roadNodes = new Vector(20);
        roadNodeGraph = new boolean[SOCBoard.MAXNODEPLUSONE][SOCBoard.MAXNODEPLUSONE];

        for (i = SOCBoard.MINNODE; i < SOCBoard.MAXNODEPLUSONE; i++)
        {
            for (j = SOCBoard.MINNODE; j < SOCBoard.MAXNODEPLUSONE; j++)
            {
                roadNodeGraph[i][j] = false;
            }
        }

        /**
         * init legal and potential arrays
         */
        legalRoads = new boolean[0xEF];
        legalSettlements = new boolean[0xFF];
        potentialRoads = new boolean[0xEF];
        potentialSettlements = new boolean[0xFF];
        potentialCities = new boolean[0xFF];

        for (i = 0; i < 0xEF; i++)
        {
            legalRoads[i] = false;
            potentialRoads[i] = false;
        }

        for (i = 0; i < 0xFF; i++)
        {
            legalSettlements[i] = false;
            potentialSettlements[i] = false;
            potentialCities[i] = false;
        }

        initLegalRoads();
        initLegalAndPotentialSettlements();
        currentOffer = null;
    }

    /**
     * initialize the legalRoads array
     */
    private final void initLegalRoads()
    {
        int i;

        for (i = 0x27; i <= 0x7C; i += 0x11)
        {
            legalRoads[i] = true;
        }

        for (i = 0x26; i <= 0x8C; i += 0x22)
        {
            legalRoads[i] = true;
        }

        for (i = 0x25; i <= 0x9C; i += 0x11)
        {
            legalRoads[i] = true;
        }

        for (i = 0x24; i <= 0xAC; i += 0x22)
        {
            legalRoads[i] = true;
        }

        for (i = 0x23; i <= 0xBC; i += 0x11)
        {
            legalRoads[i] = true;
        }

        for (i = 0x22; i <= 0xCC; i += 0x22)
        {
            legalRoads[i] = true;
        }

        for (i = 0x32; i <= 0xCB; i += 0x11)
        {
            legalRoads[i] = true;
        }

        for (i = 0x42; i <= 0xCA; i += 0x22)
        {
            legalRoads[i] = true;
        }

        for (i = 0x52; i <= 0xC9; i += 0x11)
        {
            legalRoads[i] = true;
        }

        for (i = 0x62; i <= 0xC8; i += 0x22)
        {
            legalRoads[i] = true;
        }

        for (i = 0x72; i <= 0xC7; i += 0x11)
        {
            legalRoads[i] = true;
        }
    }

    /**
     * initialize the legal settlements array
     */
    private final void initLegalAndPotentialSettlements()
    {
        int i;

        for (i = 0x27; i <= 0x8D; i += 0x11)
        {
            potentialSettlements[i] = true;
            legalSettlements[i] = true;
        }

        for (i = 0x25; i <= 0xAD; i += 0x11)
        {
            potentialSettlements[i] = true;
            legalSettlements[i] = true;
        }

        for (i = 0x23; i <= 0xCD; i += 0x11)
        {
            potentialSettlements[i] = true;
            legalSettlements[i] = true;
        }

        for (i = 0x32; i <= 0xDC; i += 0x11)
        {
            potentialSettlements[i] = true;
            legalSettlements[i] = true;
        }

        for (i = 0x52; i <= 0xDA; i += 0x11)
        {
            potentialSettlements[i] = true;
            legalSettlements[i] = true;
        }

        for (i = 0x72; i <= 0xD8; i += 0x11)
        {
            potentialSettlements[i] = true;
            legalSettlements[i] = true;
        }
    }

    /**
     * Set all nodes to not be potential settlements
     */
    public void clearPotentialSettlements()
    {
        int i;

        for (i = 0; i < 0xFF; i++)
        {
            potentialSettlements[i] = false;
        }
    }

    /**
     * set the name of the player
     *
     * @param na        the name
     */
    public void setName(String na)
    {
        name = na;
    }

    /**
     * @return the name of the player
     */
    public String getName()
    {
        return name;
    }

    /**
     * @return the player id
     */
    public int getPlayerNumber()
    {
        return playerNumber;
    }

    /**
     * @return the game that this player is in
     */
    public SOCGame getGame()
    {
        return game;
    }

    /**
     * @return true if the player played a dev card this turn
     */
    public boolean hasPlayedDevCard()
    {
        return playedDevCard;
    }

    /**
     * set the playedDevCard flag
     *
     * @param value         the value of the flag
     */
    public void setPlayedDevCard(boolean value)
    {
        playedDevCard = value;
    }

    /**
     * set the "need to discard" flag
     *
     * @param value         the value of the flag
     */
    public void setNeedToDiscard(boolean value)
    {
        needToDiscard = value;
    }

    /**
     * @return true if this player needs to discard
     */
    public boolean getNeedToDiscard()
    {
        return needToDiscard;
    }

    /**
     * set the robot flag
     *
     * @param value
     */
    public void setRobotFlag(boolean value)
    {
        robotFlag = value;
    }

    /**
     * @return the value of the robot flag
     */
    public boolean isRobot()
    {
        return robotFlag;
    }

    /**
     * set the face image id
     *
     * @param id        the image id
     */
    public void setFaceId(int id)
    {
        faceId = id;
    }

    /**
     * get the face image id
     */
    public int getFaceId()
    {
        return faceId;
    }

    /**
     * @return the numbers that this player's settlements are touching
     */
    public SOCPlayerNumbers getNumbers()
    {
        return ourNumbers;
    }

    /**
     * @return the number of pieces not in play for a particualr type of piece
     *
     * @param ptype the type of piece
     */
    public int getNumPieces(int ptype)
    {
        return numPieces[ptype];
    }

    /**
     * set the amount of pieces not in play
     * for a particular type of piece
     *
     * @param ptype         the type of piece
     * @param amt                 the amount
     */
    public void setNumPieces(int ptype, int amt)
    {
        numPieces[ptype] = amt;
    }

    /**
     * @return the list of pieces in play
     */
    public Vector getPieces()
    {
        return pieces;
    }

    /**
     * @return the list of roads in play
     */
    public Vector getRoads()
    {
        return roads;
    }

    /**
     * @return the list of settlements in play
     */
    public Vector getSettlements()
    {
        return settlements;
    }

    /**
     * @return the list of cities in play
     */
    public Vector getCities()
    {
        return cities;
    }

    /**
     * @return the coordinates of the last settlement
     * played by this player
     */
    public int getLastSettlementCoord()
    {
        return lastSettlementCoord;
    }

    /**
     * @return the coordinates of the last road
     * played by this player
     */
    public int getLastRoadCoord()
    {
        return lastRoadCoord;
    }

    /**
     * @return the longest road length
     */
    public int getLongestRoadLength()
    {
        return longestRoadLength;
    }

    /**
     * @return longest road paths
     */
    public Vector getLRPaths()
    {
        return lrPaths;
    }

    /**
     * set the longest paths vector
     * @param vec  the vector
     */
    public void setLRPaths(Vector vec)
    {
        lrPaths.removeAllElements();

        Enumeration enum = vec.elements();

        while (enum.hasMoreElements())
        {
            SOCLRPathData pd = (SOCLRPathData) enum.nextElement();
            D.ebugPrintln("restoring pd for player " + playerNumber + " :" + pd);
            lrPaths.addElement(pd);
        }
    }

    /**
     * set the longest road length
     *
     * @param len         the length
     */
    public void setLongestRoadLength(int len)
    {
        longestRoadLength = len;
    }

    /**
     * @return the resource set
     */
    public SOCResourceSet getResources()
    {
        return resources;
    }

    /**
     * @return the development card set
     */
    public SOCDevCardSet getDevCards()
    {
        return devCards;
    }

    /**
     * @return the number of knights in play
     */
    public int getNumKnights()
    {
        return numKnights;
    }

    /**
     * set the number of knights in play
     *
     * @param nk        the number of knights
     */
    public void setNumKnights(int nk)
    {
        numKnights = nk;
    }

    /**
     * increment the number of knights in play
     */
    public void incrementNumKnights()
    {
        numKnights++;
    }

    /**
     * @return true if this player has the longest road
     */
    public boolean hasLongestRoad()
    {
        if (game.getPlayerWithLongestRoad() == null)
        {
            return false;
        }
        else
        {
            return (game.getPlayerWithLongestRoad().getPlayerNumber() == this.getPlayerNumber());
        }
    }

    /**
     * @return true if this player has the largest army
     */
    public boolean hasLargestArmy()
    {
        if (game.getPlayerWithLargestArmy() == null)
        {
            return false;
        }
        else
        {
            return (game.getPlayerWithLargestArmy().getPlayerNumber() == this.getPlayerNumber());
        }
    }

    /**
     * @return the number of publicly known victory points
     */
    public int getPublicVP()
    {
        int vp = buildingVP;

        /**
         * if we have longest road, then add 2 VP
         */
        if (hasLongestRoad())
        {
            vp += 2;
        }

        /**
         * if we have largest army, then add 2 VP
         */
        if (hasLargestArmy())
        {
            vp += 2;
        }

        return vp;
    }

    /**
     * @return the actual number of victory points
     */
    public int getTotalVP()
    {
        int vp = getPublicVP();
        vp += devCards.getNumVPCards();

        return vp;
    }

    /**
     * @return the list of nodes that touch the roads in play
     */
    public Vector getRoadNodes()
    {
        return roadNodes;
    }

    /**
     * @return this player's latest offer
     */
    public SOCTradeOffer getCurrentOffer()
    {
        return currentOffer;
    }

    /**
     * set the current offer for this player
     *
     * @param of        the offer
     */
    public void setCurrentOffer(SOCTradeOffer of)
    {
        currentOffer = of;
    }

    /**
     * @return true if one of this player's roads connects
     *                                 the two nodes.
     *
     * @param node1         coordinates of first node
     * @param node2         coordinates of second node
     */
    public boolean isConnectedByRoad(int node1, int node2)
    {
        //D.ebugPrintln("isConnectedByRoad "+Integer.toHexString(node1)+", "+Integer.toHexString(node2)+" = "+roadNodeGraph[node1][node2]);
        return roadNodeGraph[node1][node2];
    }

    /**
     * put a piece into play
     * note: placing a city automatically removes the settlement there
     *
     * @param piece         the piece to be put into play
     */
    public void putPiece(SOCPlayingPiece piece)
    {
        /**
         * only do this stuff if it's our piece
         */
        if (piece.getPlayer().getPlayerNumber() == this.getPlayerNumber())
        {
            pieces.addElement(piece);

            switch (piece.getType())
            {
            /**
             * placing a road
             */
            case SOCPlayingPiece.ROAD:
                numPieces[SOCPlayingPiece.ROAD]--;
                roads.addElement(piece);
                lastRoadCoord = piece.getCoordinates();

                /**
                 * add the nodes this road touches to the roadNodes list
                 */
                Enumeration nodes = SOCBoard.getAdjacentNodesToEdge(piece.getCoordinates()).elements();
                int[] nodeCoords = new int[2];
                int i = 0;

                while (nodes.hasMoreElements())
                {
                    Integer node = (Integer) nodes.nextElement();

                    //D.ebugPrintln("^^^ node = "+Integer.toHexString(node.intValue()));
                    nodeCoords[i] = node.intValue();
                    i++;

                    /**
                     * only add nodes that aren't in the list
                     */

                    //D.ebugPrintln("(roadNodes.contains(node)) = "+(roadNodes.contains(node)));
                    if (!(roadNodes.contains(node)))
                    {
                        roadNodes.addElement(node);
                    }
                }

                /**
                 * update the graph of nodes connected by roads
                 */
                roadNodeGraph[nodeCoords[0]][nodeCoords[1]] = true;
                roadNodeGraph[nodeCoords[1]][nodeCoords[0]] = true;

                //D.ebugPrintln("^^ roadNodeGraph["+Integer.toHexString(nodeCoords[0])+"]["+Integer.toHexString(nodeCoords[1])+"] = true");
                //D.ebugPrintln("^^ roadNodeGraph["+Integer.toHexString(nodeCoords[1])+"]["+Integer.toHexString(nodeCoords[0])+"] = true");
                break;

            /**
             * placing a settlement
             */
            case SOCPlayingPiece.SETTLEMENT:
                numPieces[SOCPlayingPiece.SETTLEMENT]--;
                settlements.addElement(piece);
                lastSettlementCoord = piece.getCoordinates();
                buildingVP++;

                /**
                 * update what numbers we're touching
                 */
                ourNumbers.updateNumbers(piece, game.getBoard());

                /**
                 * update our port flags
                 */
                Integer coordInteger = new Integer(piece.getCoordinates());

                for (int portType = SOCBoard.MISC_PORT;
                        portType <= SOCBoard.WOOD_PORT; portType++)
                {
                    if (game.getBoard().getPortCoordinates(portType).contains(coordInteger))
                    {
                        setPortFlag(portType, true);

                        break;
                    }
                }

                break;

            /**
             * placing a city
             */
            case SOCPlayingPiece.CITY:

                /**
                 * place the city
                 */
                numPieces[SOCPlayingPiece.CITY]--;
                cities.addElement(piece);
                buildingVP += 2;

                /**
                 * update what numbers we're touching
                 * a city counts as touching a number twice
                 */
                ourNumbers.updateNumbers(piece, game.getBoard());

                break;
            }
        }

        updatePotentials(piece);
    }

    /**
     * undo the putting of a piece
     *
     * @param piece         the piece to be put into play
     */
    public void undoPutPiece(SOCPlayingPiece piece)
    {
        boolean ours = (piece.getPlayer().getPlayerNumber() == this.getPlayerNumber());

        switch (piece.getType())
        {
        //
        // undo a played road
        //
        case SOCPlayingPiece.ROAD:

            if (ours)
            {
                //
                // update the potential places to build roads
                // 
                removePiece(piece);
            }
            else
            {
                //
                // not our road
                //
                // make it a legal space again
                //
                legalRoads[piece.getCoordinates()] = true;

                //
                // call updatePotentials
                // on our roads that are adjacent to 
                // this edge
                //
                Vector adjEdges = SOCBoard.getAdjacentEdgesToEdge(piece.getCoordinates());
                Enumeration roadEnum = roads.elements();

                while (roadEnum.hasMoreElements())
                {
                    SOCRoad road = (SOCRoad) roadEnum.nextElement();
                    Enumeration edgeEnum = adjEdges.elements();

                    while (edgeEnum.hasMoreElements())
                    {
                        Integer edge = (Integer) edgeEnum.nextElement();

                        if (road.getCoordinates() == edge.intValue())
                        {
                            updatePotentials(road);
                        }
                    }
                }
            }

            break;

        //
        // undo a played settlement
        //
        case SOCPlayingPiece.SETTLEMENT:

            if (ours)
            {
                removePiece(piece);
                ourNumbers.undoUpdateNumbers(piece, game.getBoard());

                //
                // update our port flags
                //
                Integer coordInteger = new Integer(piece.getCoordinates());

                for (int portType = SOCBoard.MISC_PORT;
                        portType <= SOCBoard.WOOD_PORT; portType++)
                {
                    if (game.getBoard().getPortCoordinates(portType).contains(coordInteger))
                    {
                        //
                        // since only one settlement can be on a 2:1 port
                        // we can just set the port flag to false
                        //
                        if (portType != SOCBoard.MISC_PORT)
                        {
                            setPortFlag(portType, false);
                        }
                        else
                        {
                            //
                            // there are muliple 3:1 ports, so we need to check all the settlements
                            //
                            boolean haveMiscPort = false;
                            Enumeration settlementEnum = settlements.elements();

                            while (settlementEnum.hasMoreElements())
                            {
                                SOCSettlement settlement = (SOCSettlement) settlementEnum.nextElement();

                                if (game.getBoard().getPortCoordinates(SOCBoard.MISC_PORT).contains(new Integer(settlement.getCoordinates())))
                                {
                                    haveMiscPort = true;

                                    break;
                                }
                            }

                            if (!haveMiscPort)
                            {
                                Enumeration cityEnum = cities.elements();

                                while (cityEnum.hasMoreElements())
                                {
                                    SOCCity city = (SOCCity) cityEnum.nextElement();

                                    if (game.getBoard().getPortCoordinates(SOCBoard.MISC_PORT).contains(new Integer(city.getCoordinates())))
                                    {
                                        haveMiscPort = true;

                                        break;
                                    }
                                }
                            }

                            setPortFlag(SOCBoard.MISC_PORT, haveMiscPort);
                        }
                    }
                }
            }

            //
            // update settlement potentials 
            //
            undoPutPieceAuxSettlement(piece.getCoordinates());

            //
            // check adjacent nodes
            //
            Enumeration adjNodesEnum = SOCBoard.getAdjacentNodesToNode(piece.getCoordinates()).elements();

            while (adjNodesEnum.hasMoreElements())
            {
                Integer adjNode = (Integer) adjNodesEnum.nextElement();
                undoPutPieceAuxSettlement(adjNode.intValue());
            }

            break;

        //
        // undo a played city
        //
        case SOCPlayingPiece.CITY:

            if (ours)
            {
                removePiece(piece);
                potentialCities[piece.getCoordinates()] = true;

                /**
                 * update what numbers we're touching
                 * a city counts as touching a number twice
                 */
                ourNumbers.undoUpdateNumbers(piece, game.getBoard());
                ourNumbers.undoUpdateNumbers(piece, game.getBoard());
            }

            break;
        }
    }

    /**
     * Auxiliary function for undoing settlement placement
     *
     * @param settlementNode  the node we want to consider
     */
    protected void undoPutPieceAuxSettlement(int settlementNode)
    {
        //D.ebugPrintln("))))) undoPutPieceAuxSettlement : node = "+Integer.toHexString(settlementNode));
        //
        // if this node doesn't have any neighboring settlements or cities, make it legal
        //
        boolean haveNeighbor = false;
        Vector adjNodes = SOCBoard.getAdjacentNodesToNode(settlementNode);
        Enumeration settlementsEnum = game.getBoard().getSettlements().elements();

        while (settlementsEnum.hasMoreElements())
        {
            SOCSettlement settlement = (SOCSettlement) settlementsEnum.nextElement();
            Enumeration adjNodesEnum = adjNodes.elements();

            while (adjNodesEnum.hasMoreElements())
            {
                Integer adjNode = (Integer) adjNodesEnum.nextElement();

                if (adjNode.intValue() == settlement.getCoordinates())
                {
                    haveNeighbor = true;

                    //D.ebugPrintln(")))) haveNeighbor = true : node = "+Integer.toHexString(adjNode.intValue()));
                    break;
                }
            }

            if (haveNeighbor == true)
            {
                break;
            }
        }

        if (!haveNeighbor)
        {
            Enumeration citiesEnum = game.getBoard().getCities().elements();

            while (citiesEnum.hasMoreElements())
            {
                SOCCity city = (SOCCity) citiesEnum.nextElement();
                Enumeration adjNodesEnum = adjNodes.elements();

                while (adjNodesEnum.hasMoreElements())
                {
                    Integer adjNode = (Integer) adjNodesEnum.nextElement();

                    if (adjNode.intValue() == city.getCoordinates())
                    {
                        haveNeighbor = true;

                        //D.ebugPrintln(")))) haveNeighbor = true : node = "+Integer.toHexString(adjNode.intValue()));
                        break;
                    }
                }

                if (haveNeighbor == true)
                {
                    break;
                }
            }

            if (!haveNeighbor)
            {
                //D.ebugPrintln(")))) haveNeighbor = false");
                //
                // check to see if this node is on the board
                //
                if (game.getBoard().isNodeOnBoard(settlementNode))
                {
                    legalSettlements[settlementNode] = true;

                    //D.ebugPrintln(")))) legalSettlements["+Integer.toHexString(settlementNode)+"] = true");
                    //
                    // if it's the beginning of the game, make it potental
                    //
                    if (game.getGameState() < SOCGame.PLAY)
                    {
                        potentialSettlements[settlementNode] = true;

                        //D.ebugPrintln(")))) potentialSettlements["+Integer.toHexString(settlementNode)+"] = true");
                    }
                    else
                    {
                        //
                        // if it's legal and we have an adjacent road, make it potential
                        //
                        //D.ebugPrintln(")))) checking for adjacent roads");
                        boolean adjRoad = false;
                        Vector adjEdges = SOCBoard.getAdjacentEdgesToNode(settlementNode);
                        Enumeration roadsEnum = roads.elements();

                        while (roadsEnum.hasMoreElements())
                        {
                            SOCRoad road = (SOCRoad) roadsEnum.nextElement();
                            Enumeration adjEdgesEnum = adjEdges.elements();

                            while (adjEdgesEnum.hasMoreElements())
                            {
                                Integer adjEdge = (Integer) adjEdgesEnum.nextElement();

                                if (road.getCoordinates() == adjEdge.intValue())
                                {
                                    //D.ebugPrintln("))) found adj road at "+Integer.toHexString(adjEdge.intValue()));
                                    adjRoad = true;

                                    break;
                                }
                            }

                            if (adjRoad == true)
                            {
                                break;
                            }
                        }

                        if (adjRoad)
                        {
                            potentialSettlements[settlementNode] = true;

                            //D.ebugPrintln(")))) potentialSettlements["+Integer.toHexString(settlementNode)+"] = true");
                        }
                    }
                }
            }
        }
    }

    /**
     * remove a player's piece from the board2
     * and put it back in the player's hand
     *
     * NOTE: Does NOT update the potential building lists
     *           for removing settlements or cities.
     *       DOES update potential road lists.
     *
     */
    public void removePiece(SOCPlayingPiece piece)
    {
        D.ebugPrintln("--- SOCPlayer.removePiece(" + piece + ")");

        Enumeration pEnum = pieces.elements();

        while (pEnum.hasMoreElements())
        {
            SOCPlayingPiece p = (SOCPlayingPiece) pEnum.nextElement();

            if ((piece.getType() == p.getType()) && (piece.getCoordinates() == p.getCoordinates()))
            {
                pieces.removeElement(p);

                switch (piece.getType())
                {
                case SOCPlayingPiece.ROAD:
                    roads.removeElement(p);
                    numPieces[SOCPlayingPiece.ROAD]++;

                    /**
                     * remove the nodes this road touches from the roadNodes list
                     */
                    Enumeration nodes = SOCBoard.getAdjacentNodesToEdge(piece.getCoordinates()).elements();
                    int[] nodeCoords = new int[2];
                    int i = 0;

                    while (nodes.hasMoreElements())
                    {
                        Integer node = (Integer) nodes.nextElement();
                        nodeCoords[i] = node.intValue();
                        i++;

                        /**
                         * only remove nodes if none of our roads are touching it
                         */
                        Enumeration roadsEnum = roads.elements();
                        Vector adjEdges = SOCBoard.getAdjacentEdgesToNode(node.intValue());
                        boolean match = false;

                        while (roadsEnum.hasMoreElements())
                        {
                            SOCRoad rd = (SOCRoad) roadsEnum.nextElement();
                            Enumeration adjEdgesEnum = adjEdges.elements();

                            while (adjEdgesEnum.hasMoreElements())
                            {
                                Integer adjEdge = (Integer) adjEdgesEnum.nextElement();

                                if (adjEdge.intValue() == rd.getCoordinates())
                                {
                                    match = true;

                                    break;
                                }
                            }

                            if (match)
                            {
                                break;
                            }
                        }

                        if (!match)
                        {
                            roadNodes.removeElement(node);
                            potentialSettlements[node.intValue()] = false;
                        }
                    }

                    /**
                     * update the graph of nodes connected by roads
                     */
                    roadNodeGraph[nodeCoords[0]][nodeCoords[1]] = false;
                    roadNodeGraph[nodeCoords[1]][nodeCoords[0]] = false;

                    /**
                     * update the potential places to build roads
                     *
                     * NOTE: we're assuming that we could build a road here
                     * before, so we can make it a legal spot again
                     */
                    potentialRoads[piece.getCoordinates()] = true;
                    legalRoads[piece.getCoordinates()] = true;

                    /**
                     * check each adjacent legal edge, if there are
                     * no roads touching it, then it's no longer a
                     * potential road
                     */
                    Vector allPieces = game.getBoard().getPieces();
                    Enumeration adjEdgesEnum = SOCBoard.getAdjacentEdgesToEdge(piece.getCoordinates()).elements();

                    while (adjEdgesEnum.hasMoreElements())
                    {
                        Integer adjEdge = (Integer) adjEdgesEnum.nextElement();

                        if (potentialRoads[adjEdge.intValue()])
                        {
                            boolean isPotentialRoad = false;

                            /**
                             * check each adjacent node for blocking
                             * settlements or cities
                             */
                            Enumeration adjNodesEnum = SOCBoard.getAdjacentNodesToEdge(adjEdge.intValue()).elements();

                            while ((adjNodesEnum.hasMoreElements()) && (isPotentialRoad == false))
                            {
                                boolean blocked = false;
                                Integer adjNode = (Integer) adjNodesEnum.nextElement();
                                Enumeration allPiecesEnum = allPieces.elements();

                                while (allPiecesEnum.hasMoreElements())
                                {
                                    SOCPlayingPiece aPiece = (SOCPlayingPiece) allPiecesEnum.nextElement();

                                    if ((aPiece.getPlayer().getPlayerNumber() != this.getPlayerNumber()) && ((aPiece.getType() == SOCPlayingPiece.SETTLEMENT) || (aPiece.getType() == SOCPlayingPiece.CITY)) && (aPiece.getCoordinates() == (adjNode.intValue())))
                                    {
                                        /**
                                         * we're blocked, don't bother checking adjacent edges
                                         */
                                        blocked = true;

                                        break;
                                    }
                                }

                                if (!blocked)
                                {
                                    Enumeration adjAdjEdgesEnum = SOCBoard.getAdjacentEdgesToNode(adjNode.intValue()).elements();

                                    while ((adjAdjEdgesEnum.hasMoreElements()) && (isPotentialRoad == false))
                                    {
                                        Integer adjAdjEdge = (Integer) adjAdjEdgesEnum.nextElement();

                                        if (adjAdjEdge.intValue() != adjEdge.intValue())
                                        {
                                            Enumeration ourRoadsEnum = roads.elements();

                                            while (ourRoadsEnum.hasMoreElements())
                                            {
                                                SOCRoad ourRoad = (SOCRoad) ourRoadsEnum.nextElement();

                                                if (ourRoad.getCoordinates() == adjAdjEdge.intValue())
                                                {
                                                    /**
                                                     * we're still connected
                                                     */
                                                    isPotentialRoad = true;

                                                    break;
                                                }
                                            }
                                        }
                                    }
                                }
                            }

                            potentialRoads[adjEdge.intValue()] = isPotentialRoad;
                        }
                    }

                    break;

                case SOCPlayingPiece.SETTLEMENT:
                    settlements.removeElement(p);
                    numPieces[SOCPlayingPiece.SETTLEMENT]++;
                    buildingVP--;

                    break;

                case SOCPlayingPiece.CITY:
                    cities.removeElement(p);
                    numPieces[SOCPlayingPiece.CITY]++;
                    buildingVP -= 2;

                    break;
                }

                break;
            }
        }
    }

    /**
     * update the arrays that keep track of where
     * this player can play a piece
     *
     * @param piece         a piece that has just been played
     */
    public void updatePotentials(SOCPlayingPiece piece)
    {
        //D.ebugPrintln("&&& UPDATING POTENTIALS FOR "+piece);
        int tmp;
        boolean ours;
        boolean blocked;
        int i;
        Integer coord;
        int id = piece.getCoordinates();
        Vector allPieces = game.getBoard().getPieces();

        /**
         * check if this piece is ours
         */
        if (piece.getPlayer().getPlayerNumber() == this.getPlayerNumber())
        {
            ours = true;
        }
        else
        {
            ours = false;
        }

        switch (piece.getType())
        {
        /**
         * a road was played
         */
        case SOCPlayingPiece.ROAD:

            // remove non-potentials
            potentialRoads[id] = false;
            legalRoads[id] = false;

            if (ours)
            {
                // only add potentials if it's our piece
                // add new potentials
                Enumeration nodes = (SOCBoard.getAdjacentNodesToEdge(id)).elements();

                while (nodes.hasMoreElements())
                {
                    Integer node = (Integer) nodes.nextElement();

                    /**
                     * check for a foreign settlement or city
                     */
                    blocked = false;

                    Enumeration pEnum = allPieces.elements();

                    while (pEnum.hasMoreElements())
                    {
                        SOCPlayingPiece p = (SOCPlayingPiece) pEnum.nextElement();

                        if ((p.getPlayer().getPlayerNumber() != this.getPlayerNumber()) && ((p.getType() == SOCPlayingPiece.SETTLEMENT) || (p.getType() == SOCPlayingPiece.CITY)) && (p.getCoordinates() == (node.intValue())))
                        {
                            blocked = true;

                            break;
                        }
                    }

                    if (!blocked)
                    {
                        Enumeration edges = SOCBoard.getAdjacentEdgesToNode(node.intValue()).elements();

                        while (edges.hasMoreElements())
                        {
                            Integer edge = (Integer) edges.nextElement();

                            if (legalRoads[edge.intValue()])
                            {
                                potentialRoads[edge.intValue()] = true;
                            }
                        }

                        if (legalSettlements[node.intValue()])
                        {
                            potentialSettlements[node.intValue()] = true;
                        }
                    }
                }
            }

            break;

        /**
         * a settlement was placed
         */
        case SOCPlayingPiece.SETTLEMENT:

            // remove non-potentials
            potentialSettlements[id] = false;
            potentialSettlements[id - 0x11] = false;
            potentialSettlements[id + 0x11] = false;
            legalSettlements[id] = false;
            legalSettlements[id - 0x11] = false;
            legalSettlements[id + 0x11] = false;

            if (((id >> 4) % 2) == 0)
            { // If first digit is even,
                potentialSettlements[(id + 0x10) - 0x01] = false;
                legalSettlements[(id + 0x10) - 0x01] = false;

                if (ours)
                { // only add potentials if it's our piece

                    // add new potentials
                    tmp = id - 0x11; // upper left '\' edge

                    if (legalRoads[tmp]) // make sure the potential road is legal
                    {
                        potentialRoads[tmp] = true;
                    }

                    // upper right '/' edge
                    if (legalRoads[id]) // make sure the potential road is legal
                    {
                        potentialRoads[id] = true;
                    }

                    tmp = id - 0x01; // lower middle '|' edge

                    if (legalRoads[tmp]) // make sure the potential road is legal
                    {
                        potentialRoads[tmp] = true;
                    }
                }
                else
                {
                    // see if a road has been cut off
                    Vector ourRoads = new Vector();
                    Enumeration pEnum = (this.pieces).elements();

                    while (pEnum.hasMoreElements())
                    {
                        SOCPlayingPiece p = (SOCPlayingPiece) pEnum.nextElement();

                        if (p.getType() == SOCPlayingPiece.ROAD)
                        {
                            ourRoads.addElement(new Integer(p.getCoordinates()));
                        }
                    }

                    tmp = id - 0x11; // upper left '\' edge

                    if ((potentialRoads[tmp]) && // make sure the pot. road is still connected
                            !(ourRoads.contains(new Integer(tmp - 0x10)) || ourRoads.contains(new Integer(tmp - 0x11))))
                    {
                        potentialRoads[tmp] = false;
                    }

                    tmp = id; // upper right '/' edge

                    if ((potentialRoads[tmp]) && // make sure the pot. road is still connected
                            !(ourRoads.contains(new Integer(tmp + 0x01)) || ourRoads.contains(new Integer(tmp + 0x11))))
                    {
                        potentialRoads[tmp] = false;
                    }

                    tmp = id - 0x01; // lower middle '|' edge

                    if ((potentialRoads[tmp]) && // make sure the pot. road is still connected
                            !(ourRoads.contains(new Integer(tmp - 0x01)) || ourRoads.contains(new Integer(tmp + 0x10))))
                    {
                        potentialRoads[tmp] = false;
                    }
                }
            }
            else
            {
                // we have an A node.
                // continue removing non-potentials
                potentialSettlements[id - 0x10 + 0x01] = false;
                legalSettlements[id - 0x10 + 0x01] = false;

                if (ours)
                { // only add potentials if it's our piece

                    // add new potentials
                    tmp = id - 0x11; // lower left '/' edge

                    if (legalRoads[tmp]) // make sure the potential road is legal
                    {
                        potentialRoads[tmp] = true;
                    }

                    // lower right '\' edge
                    if (legalRoads[id]) // make sure the potential road is legal
                    {
                        potentialRoads[id] = true;
                    }

                    tmp = id - 0x10; // upper middle '|' edge

                    if (legalRoads[tmp]) // make sure the potential road is legal
                    {
                        potentialRoads[tmp] = true;
                    }
                }
                else
                {
                    // see if a road has been cut off
                    Vector ourRoads = new Vector();
                    Enumeration pEnum = (this.pieces).elements();

                    while (pEnum.hasMoreElements())
                    {
                        SOCPlayingPiece p = (SOCPlayingPiece) pEnum.nextElement();

                        if (p.getType() == SOCPlayingPiece.ROAD)
                        {
                            ourRoads.addElement(new Integer(p.getCoordinates()));
                        }
                    }

                    tmp = id - 0x11; // lower left '/' edge

                    if ((potentialRoads[tmp]) && // make sure the pot. road is still connected
                            !(ourRoads.contains(new Integer(tmp - 0x11)) || ourRoads.contains(new Integer(tmp - 0x01))))
                    {
                        potentialRoads[tmp] = false;
                    }

                    tmp = id; // lower right '\' edge

                    if ((potentialRoads[tmp]) && // make sure the pot. road is still connected
                            !(ourRoads.contains(new Integer(tmp + 0x11)) || ourRoads.contains(new Integer(tmp + 0x10))))
                    {
                        potentialRoads[tmp] = false;
                    }

                    tmp = id - 0x10; // upper middle '|' edge

                    if ((potentialRoads[tmp]) && // make sure the pot. road is still connected
                            !(ourRoads.contains(new Integer(tmp - 0x10)) || ourRoads.contains(new Integer(tmp + 0x01))))
                    {
                        potentialRoads[tmp] = false;
                    }
                }
            }

            if (ours)
            { // only add potentials if it's our piece

                // continue adding new potentials
                potentialCities[id] = true;
            }

            break;

        /**
         * a city was placed
         */
        case SOCPlayingPiece.CITY:

            // remove non-potentials
            potentialCities[id] = false;

            break;
        }
    }

    /**
     * set which nodes are potential settlements
     *
     * @param psList        the list of potential settlements
     */
    public void setPotentialSettlements(Vector psList)
    {
        clearPotentialSettlements();

        Enumeration enum = psList.elements();

        while (enum.hasMoreElements())
        {
            Integer number = (Integer) enum.nextElement();
            potentialSettlements[number.intValue()] = true;
        }
    }

    /**
     * @return true if this node is a potential settlement
     * @param node        the coordinates of a node on the board
     */
    public boolean isPotentialSettlement(int node)
    {
        return potentialSettlements[node];
    }

    /**
     * @return true if this node is a potential city
     * @param node        the coordinates of a node on the board
     */
    public boolean isPotentialCity(int node)
    {
        return potentialCities[node];
    }

    /**
     * @return true if this edge is a potential road
     * @param edge        the coordinates of an edge on the board
     */
    public boolean isPotentialRoad(int edge)
    {
        return potentialRoads[edge];
    }

    /**
     * @return true if this edge is a legal road
     * @param edge        the coordinates of an edge on the board
     */
    public boolean isLegalRoad(int edge)
    {
        return legalRoads[edge];
    }

    /**
     * @return true if there is at least one potential road
     */
    public boolean hasPotentialRoad()
    {
        for (int i = 0x22; i <= 0xCC; i++)
        {
            if (potentialRoads[i])
            {
                return true;
            }
        }

        return false;
    }

    /**
     * @return true if there is at least one potential settlement
     */
    public boolean hasPotentialSettlement()
    {
        for (int i = 0x23; i <= 0xDC; i++)
        {
            if (potentialSettlements[i])
            {
                return true;
            }
        }

        return false;
    }

    /**
     * @return true if there is at least one potential city
     */
    public boolean hasPotentialCity()
    {
        for (int i = 0x23; i <= 0xDC; i++)
        {
            if (potentialCities[i])
            {
                return true;
            }
        }

        return false;
    }

    /**
     * Calculates the longest road for a player
     *
     * @return                         the length of the longest road for that player
     */
    public int calcLongestRoad2()
    {
        //Date startTime = new Date();
        //
        // clear the lr paths vector so that we have an accurate
        // representation.  if someone cut our longest path in two
        // we won't catch it unless we clear the vector
        //
        D.ebugPrintln("CLEARING PATH DATA");
        lrPaths.removeAllElements();

        /**
         * we're doing a depth first search of all possible road paths
         */
        Stack pending = new Stack();
        int longest = 0;

        for (Enumeration e = roadNodes.elements(); e.hasMoreElements();)
        {
            Integer roadNode = (Integer) e.nextElement();
            int pathStartCoord = roadNode.intValue();
            int pathEndCoord;
            int pathLength = 0;
            pending.push(new NodeLenVis(pathStartCoord, 0, new Vector()));

            while (!pending.isEmpty())
            {
                NodeLenVis curNode = (NodeLenVis) pending.pop();
                int coord = curNode.node;
                int len = curNode.len;
                Vector visited = curNode.vis;
                boolean pathEnd = false;

                /**
                 * check for road blocks
                 */
                Enumeration pEnum = game.getBoard().getPieces().elements();

                while (pEnum.hasMoreElements())
                {
                    SOCPlayingPiece p = (SOCPlayingPiece) pEnum.nextElement();

                    if ((len > 0) && (p.getPlayer().getPlayerNumber() != this.getPlayerNumber()) && ((p.getType() == SOCPlayingPiece.SETTLEMENT) || (p.getType() == SOCPlayingPiece.CITY)) && (p.getCoordinates() == coord))
                    {
                        pathEnd = true;

                        //D.ebugPrintln("^^^ path end at "+Integer.toHexString(coord));
                        break;
                    }
                }

                if (!pathEnd)
                {
                    pathEnd = true;

                    int j;
                    IntPair pair;
                    boolean match;

                    j = coord - 0x11;
                    pair = new IntPair(coord, j);
                    match = false;

                    if ((j >= SOCBoard.MINNODE) && (j < SOCBoard.MAXNODEPLUSONE) && (isConnectedByRoad(coord, j)))
                    {
                        for (Enumeration ev = visited.elements();
                                ev.hasMoreElements();)
                        {
                            IntPair vis = (IntPair) ev.nextElement();

                            if (vis.equals(pair))
                            {
                                match = true;

                                break;
                            }
                        }

                        if (!match)
                        {
                            Vector newVis = (Vector) visited.clone();
                            newVis.addElement(pair);
                            pending.push(new NodeLenVis(j, len + 1, newVis));
                            pathEnd = false;
                        }
                    }

                    j = coord + 0x11;
                    pair = new IntPair(coord, j);
                    match = false;

                    if ((j >= SOCBoard.MINNODE) && (j < SOCBoard.MAXNODEPLUSONE) && (isConnectedByRoad(coord, j)))
                    {
                        for (Enumeration ev = visited.elements();
                                ev.hasMoreElements();)
                        {
                            IntPair vis = (IntPair) ev.nextElement();

                            if (vis.equals(pair))
                            {
                                match = true;

                                break;
                            }
                        }

                        if (!match)
                        {
                            Vector newVis = (Vector) visited.clone();
                            newVis.addElement(pair);
                            pending.push(new NodeLenVis(j, len + 1, newVis));
                            pathEnd = false;
                        }
                    }

                    j = (coord + 0x10) - 0x01;
                    pair = new IntPair(coord, j);
                    match = false;

                    if ((j >= SOCBoard.MINNODE) && (j < SOCBoard.MAXNODEPLUSONE) && (isConnectedByRoad(coord, j)))
                    {
                        for (Enumeration ev = visited.elements();
                                ev.hasMoreElements();)
                        {
                            IntPair vis = (IntPair) ev.nextElement();

                            if (vis.equals(pair))
                            {
                                match = true;

                                break;
                            }
                        }

                        if (!match)
                        {
                            Vector newVis = (Vector) visited.clone();
                            newVis.addElement(pair);
                            pending.push(new NodeLenVis(j, len + 1, newVis));
                            pathEnd = false;
                        }
                    }

                    j = coord - 0x10 + 0x01;
                    pair = new IntPair(coord, j);
                    match = false;

                    if ((j >= SOCBoard.MINNODE) && (j < SOCBoard.MAXNODEPLUSONE) && (isConnectedByRoad(coord, j)))
                    {
                        for (Enumeration ev = visited.elements();
                                ev.hasMoreElements();)
                        {
                            IntPair vis = (IntPair) ev.nextElement();

                            if (vis.equals(pair))
                            {
                                match = true;

                                break;
                            }
                        }

                        if (!match)
                        {
                            Vector newVis = (Vector) visited.clone();
                            newVis.addElement(pair);
                            pending.push(new NodeLenVis(j, len + 1, newVis));
                            pathEnd = false;
                        }
                    }
                }

                if (pathEnd)
                {
                    if (len > longest)
                    {
                        longest = len;
                    }

                    //
                    // we want to store the longest path for a single set of nodes
                    // check to make sure that we don't save two paths that share a node
                    //
                    boolean intersection;
                    boolean addNewPath = true;
                    Vector trash = new Vector();

                    for (Enumeration pdEnum = lrPaths.elements();
                            pdEnum.hasMoreElements();)
                    {
                        SOCLRPathData oldPathData = (SOCLRPathData) pdEnum.nextElement();
                        D.ebugPrintln("oldPathData = " + oldPathData);

                        Vector nodePairs = oldPathData.getNodePairs();
                        intersection = false;

                        for (Enumeration ev = visited.elements();
                                ev.hasMoreElements();)
                        {
                            IntPair vis = (IntPair) ev.nextElement();
                            D.ebugPrintln("vis = " + vis);

                            for (Enumeration npev = nodePairs.elements();
                                    npev.hasMoreElements();)
                            {
                                IntPair np = (IntPair) npev.nextElement();
                                D.ebugPrintln("np = " + np);

                                if (np.equals(vis))
                                {
                                    D.ebugPrintln("oldPathData.nodePairs.contains(vis)");
                                    intersection = true;

                                    break;
                                }
                            }

                            if (intersection)
                            {
                                break;
                            }
                        }

                        if (intersection)
                        {
                            //
                            // only keep the longer of the two paths
                            //
                            if (oldPathData.getLength() < len)
                            {
                                D.ebugPrintln("REMOVING OLDPATHDATA");
                                trash.addElement(oldPathData);
                            }
                            else
                            {
                                addNewPath = false;
                                D.ebugPrintln("NOT ADDING NEW PATH");
                            }
                        }
                    }

                    if (!trash.isEmpty())
                    {
                        for (Enumeration trashEnum = trash.elements();
                                trashEnum.hasMoreElements();)
                        {
                            SOCLRPathData oldPathData = (SOCLRPathData) trashEnum.nextElement();
                            lrPaths.removeElement(oldPathData);
                        }
                    }

                    if (addNewPath)
                    {
                        SOCLRPathData newPathData = new SOCLRPathData(pathStartCoord, coord, len, visited);
                        D.ebugPrintln("ADDING PATH: " + newPathData);
                        lrPaths.addElement(newPathData);
                    }
                }
            }
        }

        longestRoadLength = longest;

        //Date stopTime = new Date();
        //long elapsed = stopTime.getTime() - startTime.getTime();
        //System.out.println("LONGEST FOR "+name+" IS "+longest+" TIME = "+elapsed+"ms");
        return longest;
    }

    /**
     * set a port flag
     *
     * @param portType        the type of port, see SOCBoard
     * @param value                        true or false
     */
    public void setPortFlag(int portType, boolean value)
    {
        ports[portType] = value;
    }

    /**
     * @return the port flag for a type of port
     *
     * @param portType        the type of port, see SOCBoard
     */
    public boolean getPortFlag(int portType)
    {
        return ports[portType];
    }

    /**
     * @return the ports array
     */
    public boolean[] getPortFlags()
    {
        return ports;
    }

    /**
     * @return a copy of this player
     */
    public SOCPlayer copy()
    {
        SOCPlayer copy = new SOCPlayer(this.getPlayerNumber(), game);

        if (game.getGameState() >= SOCGame.START2B)
        {
            copy.clearPotentialSettlements();
        }

        /**
         * copy all of the pieces that have been played by all players
         * we need to get all pieces so that we have an accurate potential
         * building map
         */
        for (int pnum = 0; pnum < SOCGame.MAXPLAYERS; pnum++)
        {
            if (pnum != this.getPlayerNumber())
            {
                Enumeration piecesEnum = game.getPlayer(pnum).getPieces().elements();

                while (piecesEnum.hasMoreElements())
                {
                    SOCPlayingPiece piece = (SOCPlayingPiece) piecesEnum.nextElement();
                    SOCPlayer owner = game.getPlayer(pnum);

                    switch (piece.getType())
                    {
                    case SOCPlayingPiece.ROAD:
                        copy.putPiece(new SOCRoad(owner, piece.getCoordinates()));

                        break;

                    case SOCPlayingPiece.SETTLEMENT:
                        copy.putPiece(new SOCSettlement(owner, piece.getCoordinates()));

                        break;

                    case SOCPlayingPiece.CITY:

                        /**
                         * if it's a city, put down a settlement first in order to
                         * get the proper potential settlement list and number list
                         */
                        if (piece.getType() == SOCPlayingPiece.CITY)
                        {
                            SOCSettlement temp = new SOCSettlement(owner, piece.getCoordinates());
                            copy.putPiece(temp);
                            copy.removePiece(temp);
                        }

                        copy.putPiece(new SOCCity(owner, piece.getCoordinates()));

                        break;
                    }
                }
            }
            else
            {
                Enumeration piecesEnum = this.getPieces().elements();

                while (piecesEnum.hasMoreElements())
                {
                    SOCPlayingPiece piece = (SOCPlayingPiece) piecesEnum.nextElement();
                    SOCPlayer owner = copy;

                    switch (piece.getType())
                    {
                    case SOCPlayingPiece.ROAD:
                        copy.putPiece(new SOCRoad(owner, piece.getCoordinates()));

                        break;

                    case SOCPlayingPiece.SETTLEMENT:
                        copy.putPiece(new SOCSettlement(owner, piece.getCoordinates()));

                        break;

                    case SOCPlayingPiece.CITY:

                        /**
                         * if it's a city, put down a settlement first in order to
                         * get the proper potential settlement list and number list
                         */
                        if (piece.getType() == SOCPlayingPiece.CITY)
                        {
                            SOCSettlement temp = new SOCSettlement(owner, piece.getCoordinates());
                            copy.putPiece(temp);
                            copy.removePiece(temp);
                        }

                        copy.putPiece(new SOCCity(owner, piece.getCoordinates()));

                        break;
                    }
                }
            }
        }

        /**
         * copy the resources
         */
        SOCResourceSet copyResources = copy.getResources();

        for (int rType = SOCResourceConstants.CLAY;
                rType <= SOCResourceConstants.UNKNOWN; rType++)
        {
            copyResources.setAmount(resources.getAmount(rType), rType);
        }

        /**
         * copy the dev cards
         */
        SOCDevCardSet copyDevCards = getDevCards();

        for (int dcType = SOCDevCardConstants.KNIGHT;
                dcType <= SOCDevCardConstants.UNKNOWN; dcType++)
        {
            copyDevCards.setAmount(devCards.getAmount(SOCDevCardSet.OLD, dcType), SOCDevCardSet.OLD, dcType);
            copyDevCards.setAmount(devCards.getAmount(SOCDevCardSet.NEW, dcType), SOCDevCardSet.NEW, dcType);
        }

        /**
         * copy the army
         */
        copy.setNumKnights(numKnights);

        /**
         * copy port flags
         */
        for (int port = SOCBoard.MISC_PORT; port <= SOCBoard.WOOD_PORT;
                port++)
        {
            copy.setPortFlag(port, ports[port]);
        }

        /**
         * NEED TO COPY :
         *        currentOffer
         *        playedDevCard flag
         *        robotFlag
         *        faceId
         */
        return copy;
    }

    /**
     * set vars to null so gc can clean up
     */
    public void destroyPlayer()
    {
        game = null;
        numPieces = null;
        pieces.removeAllElements();
        pieces = null;
        roads.removeAllElements();
        roads = null;
        settlements.removeAllElements();
        settlements = null;
        cities.removeAllElements();
        cities = null;
        resources = null;
        devCards = null;
        ourNumbers = null;
        ports = null;
        roadNodes.removeAllElements();
        roadNodes = null;
        roadNodeGraph = null;
        legalRoads = null;
        legalSettlements = null;
        potentialRoads = null;
        potentialSettlements = null;
        potentialCities = null;
        currentOffer = null;
    }
}
