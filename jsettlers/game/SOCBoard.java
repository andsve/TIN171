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

import java.io.Serializable;

import java.util.Enumeration;
import java.util.Hashtable;
import java.util.Random;
import java.util.Vector;


/**
 * This is a representation of the board in Settlers of Catan.
 *
 * @author Robert S Thomas
 */
public class SOCBoard implements Serializable, Cloneable
{
    public static final int DESERT_HEX = 0;
    public static final int CLAY_HEX = 1;
    public static final int ORE_HEX = 2;
    public static final int SHEEP_HEX = 3;
    public static final int WHEAT_HEX = 4;
    public static final int WOOD_HEX = 5;
    public static final int WATER_HEX = 6;
    public static final int MISC_PORT_HEX = 7;
    public static final int CLAY_PORT_HEX = 8;
    public static final int ORE_PORT_HEX = 9;
    public static final int SHEEP_PORT_HEX = 10;
    public static final int WHEAT_PORT_HEX = 11;
    public static final int WOOD_PORT_HEX = 12;
    public static final int MISC_PORT = 0;
    public static final int CLAY_PORT = 1;
    public static final int ORE_PORT = 2;
    public static final int SHEEP_PORT = 3;
    public static final int WHEAT_PORT = 4;
    public static final int WOOD_PORT = 5;

    /**
     * largest value for a hex
     */
    public static final int MAXHEX = 0xDD;

    /**
     * smallest value for a hex
     */
    public static final int MINHEX = 0x11;

    /**
     * largest value for an edge
     */
    public static final int MAXEDGE = 0xCC;

    /**
     * smallest value for an edge
     */
    public static final int MINEDGE = 0x22;

    /**
     * largest value for a node
     */
    public static final int MAXNODE = 0xDC;

    /**
     * smallest value for a node
     */
    public static final int MINNODE = 0x23;

    /**
     * largest value for a node plus one
     */
    public static final int MAXNODEPLUSONE = MAXNODE + 1;

    /***************************************
       Key to the hexes[] :
       0 : desert
       1 : clay
       2 : ore
       3 : sheep
       4 : wheat
       5 : wood
       6 : water
       7 : misc port facing 1
       8 : misc port facing 2
       9 : misc port facing 3
       10 : misc port facing 4
       11 : misc port facing 5
       12 : misc port facing 6
        ports are represented in binary like this:
        (port facing)           (kind of port)
              \--> [0 0 0][0 0 0 0] <--/
        kind of port:
        1 : clay
        2 : ore
        3 : sheep
        4 : wheat
        5 : wood
        port facing:
        6___    ___1
            \/\/
            /  \
       5___|    |___2
           |    |
            \  /
        4___/\/\___3
     **************************************************/

    /*
       private int hexLayout[] = { 51, 6, 10, 6,
       6, 5, 3, 4, 68,
       8, 1, 2, 1, 3, 6,
       6, 0, 5, 4, 5, 4, 85,
       8, 1, 3, 3, 2, 6,
       6, 2, 4, 5, 12,
       18, 6, 97, 6 };
     */
    private int[] hexLayout = 
    {
        6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
        6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6
    };

    /**
     * Key to the numbers[] :
     *     0 : 2
     *     1 : 3
     *     2 : 4
     *     3 : 5
     *     4 : 6
     *     5 : 8
     *     6 : 9
     *     7 : 10
     *     8 : 11
     *     9 : 12
     */
    private int[] boardNum2Num = { -1, -1, 0, 1, 2, 3, 4, -1, 5, 6, 7, 8, 9 };
    private int[] num2BoardNum = { 2, 3, 4, 5, 6, 8, 9, 10, 11, 12 };

    /*
       private int numberLayout[] = { -1, -1, -1, -1,
       -1, 8, 9, 6, -1,
       -1, 2, 4, 3, 7, -1,
       -1, -1, 1, 8, 2, 5, -1,
       -1, 5, 7, 6, 1, -1,
       -1, 3, 0, 4, -1,
       -1, -1, -1, -1 };
     */
    private int[] numberLayout = 
    {
        -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
        -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
        -1
    };
    private int[] numToHexID = 
    {
        0x17, 0x39, 0x5B, 0x7D,
        
        0x15, 0x37, 0x59, 0x7B, 0x9D,
        
        0x13, 0x35, 0x57, 0x79, 0x9B, 0xBD,
        
        0x11, 0x33, 0x55, 0x77, 0x99, 0xBB, 0xDD,
        
        0x31, 0x53, 0x75, 0x97, 0xB9, 0xDB,
        
        0x51, 0x73, 0x95, 0xB7, 0xD9,
        
        0x71, 0x93, 0xB5, 0xD7
    };

    /**
     * translate hex ID to an array index
     */
    private int[] hexIDtoNum;

    /**
     * add to hex coord to get all node coords
     */
    private int[] hexNodes = { 0x01, 0x12, 0x21, 0x10, -0x01, -0x10 };

    /**
     *  all hexes adjacent to a node
     */
    private int[] nodeToHex = { -0x21, 0x01, -0x01, -0x10, 0x10, -0x12 };

    /**
     * the hex that the robber is in
     */
    private int robberHex;

    /**
     * where the ports are
     */
    private Vector[] ports;

    /**
     * pieces on the board
     */
    private Vector pieces;

    /**
     * roads on the board
     */
    private Vector roads;

    /**
     * settlements on the board
     */
    private Vector settlements;

    /**
     * cities on the board
     */
    private Vector cities;

    /**
     * random number generator
     */
    private Random rand = new Random();

    /**
     * a list of nodes on the board
     */
    protected Hashtable nodesOnBoard;

    /**
     * Create a new Settlers of Catan Board
     */
    public SOCBoard()
    {
        robberHex = -1;

        /**
         * generic counter
         */
        int i;

        /**
         * initialize the pieces vectors
         */
        pieces = new Vector(96);
        roads = new Vector(60);
        settlements = new Vector(20);
        cities = new Vector(16);

        /**
         * initialize the port vector
         */
        ports = new Vector[6];
        ports[MISC_PORT] = new Vector(8);

        for (i = CLAY_PORT; i <= WOOD_PORT; i++)
        {
            ports[i] = new Vector(2);
        }

        /**
         * initialize the hexIDtoNum array
         */
        hexIDtoNum = new int[0xEE];

        for (i = 0; i < 0xEE; i++)
        {
            hexIDtoNum[i] = 0;
        }

        initHexIDtoNumAux(0x17, 0x7D, 0);
        initHexIDtoNumAux(0x15, 0x9D, 4);
        initHexIDtoNumAux(0x13, 0xBD, 9);
        initHexIDtoNumAux(0x11, 0xDD, 15);
        initHexIDtoNumAux(0x31, 0xDB, 22);
        initHexIDtoNumAux(0x51, 0xD9, 28);
        initHexIDtoNumAux(0x71, 0xD7, 33);

        nodesOnBoard = new Hashtable();

        /**
         * initialize the list of nodes on the board
         */
        Boolean t = new Boolean(true);

        for (i = 0x27; i <= 0x8D; i += 0x11)
        {
            nodesOnBoard.put(new Integer(i), t);
        }

        for (i = 0x25; i <= 0xAD; i += 0x11)
        {
            nodesOnBoard.put(new Integer(i), t);
        }

        for (i = 0x23; i <= 0xCD; i += 0x11)
        {
            nodesOnBoard.put(new Integer(i), t);
        }

        for (i = 0x32; i <= 0xDC; i += 0x11)
        {
            nodesOnBoard.put(new Integer(i), t);
        }

        for (i = 0x52; i <= 0xDA; i += 0x11)
        {
            nodesOnBoard.put(new Integer(i), t);
        }

        for (i = 0x72; i <= 0xD8; i += 0x11)
        {
            nodesOnBoard.put(new Integer(i), t);
        }
    }

    /**
     * Auxillery method for initializing the hexIDtoNum array
     */
    private final void initHexIDtoNumAux(int begin, int end, int num)
    {
        int i;

        for (i = begin; i <= end; i += 0x22)
        {
            hexIDtoNum[i] = num;
            num++;
        }
    }

    /**
     * Shuffle the hex tiles and layout a board
     */
    public void makeNewBoard()
    {
        int[] landHex = { 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5 };
        int[] portHex = { 0, 0, 0, 0, 1, 2, 3, 4, 5 };
        int[] number = { 3, 0, 4, 1, 5, 7, 6, 9, 8, 2, 5, 7, 6, 2, 3, 4, 1, 8 };
        int[] numPath = { 29, 30, 31, 26, 20, 13, 7, 6, 5, 10, 16, 23, 24, 25, 19, 12, 11, 17, 18 };
        int i;
        int j;
        int idx;
        int tmp;

        // shuffle the land hexes
        for (j = 0; j < 10; j++)
        {
            for (i = 0; i < landHex.length; i++)
            {
                // Swap a random card below the ith card with the ith card
                idx = Math.abs(rand.nextInt() % (landHex.length - i));
                tmp = landHex[idx];
                landHex[idx] = landHex[i];
                landHex[i] = tmp;
            }
        }

        int cnt = 0;

        for (i = 0; i < landHex.length; i++)
        {
            // place the land hexes
            hexLayout[numPath[i]] = landHex[i];

            // place the robber
            if (landHex[i] == 0)
            {
                robberHex = numToHexID[numPath[i]];
                numberLayout[numPath[i]] = -1;
            }
            else
            {
                // place the numbers
                numberLayout[numPath[i]] = number[cnt];
                cnt++;
            }
        }

        // shuffle the ports
        for (j = 0; j < 10; j++)
        {
            for (i = 1; i < portHex.length; i++) // don't swap 0 with 0!
            {
                // Swap a random card below the ith card with the ith card
                idx = Math.abs(rand.nextInt() % (portHex.length - i));
                tmp = portHex[idx];
                portHex[idx] = portHex[i];
                portHex[i] = tmp;
            }
        }

        // place the ports
        placePort(portHex[0], 0, 3);
        placePort(portHex[1], 2, 4);
        placePort(portHex[2], 8, 4);
        placePort(portHex[3], 9, 2);
        placePort(portHex[4], 21, 5);
        placePort(portHex[5], 22, 2);
        placePort(portHex[6], 32, 6);
        placePort(portHex[7], 33, 1);
        placePort(portHex[8], 35, 6);

        // fill out the ports[] vectors
        ports[portHex[0]].addElement(new Integer(0x27));
        ports[portHex[0]].addElement(new Integer(0x38));

        ports[portHex[1]].addElement(new Integer(0x5A));
        ports[portHex[1]].addElement(new Integer(0x6B));

        ports[portHex[2]].addElement(new Integer(0x9C));
        ports[portHex[2]].addElement(new Integer(0xAD));

        ports[portHex[3]].addElement(new Integer(0x25));
        ports[portHex[3]].addElement(new Integer(0x34));

        ports[portHex[4]].addElement(new Integer(0xCD));
        ports[portHex[4]].addElement(new Integer(0xDC));

        ports[portHex[5]].addElement(new Integer(0x43));
        ports[portHex[5]].addElement(new Integer(0x52));

        ports[portHex[6]].addElement(new Integer(0xC9));
        ports[portHex[6]].addElement(new Integer(0xDA));

        ports[portHex[7]].addElement(new Integer(0x72));
        ports[portHex[7]].addElement(new Integer(0x83));

        ports[portHex[8]].addElement(new Integer(0xA5));
        ports[portHex[8]].addElement(new Integer(0xB6));
    }

    /**
     * Auxillary method for placing the port hexes
     */
    private final void placePort(int port, int hex, int face)
    {
        if (port == 0)
        {
            // generic port
            hexLayout[hex] = face + 6;
        }
        else
        {
            hexLayout[hex] = (face << 4) + port;
        }
    }

    /**
     * @return the hex layout
     */
    public int[] getHexLayout()
    {
        return hexLayout;
    }

    /**
     * @return the number layout
     */
    public int[] getNumberLayout()
    {
        return numberLayout;
    }

    /**
     * @return where the robber is
     */
    public int getRobberHex()
    {
        return robberHex;
    }

    /**
     * set the hexLayout
     *
     * @param hl  the hex layout
     */
    public void setHexLayout(int[] hl)
    {
        hexLayout = hl;

        if (hl[0] == 6)
        {
            /**
             * this is a blank board
             */
            return;
        }

        /**
         * fill in the port node information
         */
        ports[getPortTypeFromHex(hexLayout[0])].addElement(new Integer(0x27));
        ports[getPortTypeFromHex(hexLayout[0])].addElement(new Integer(0x38));

        ports[getPortTypeFromHex(hexLayout[2])].addElement(new Integer(0x5A));
        ports[getPortTypeFromHex(hexLayout[2])].addElement(new Integer(0x6B));

        ports[getPortTypeFromHex(hexLayout[8])].addElement(new Integer(0x9C));
        ports[getPortTypeFromHex(hexLayout[8])].addElement(new Integer(0xAD));

        ports[getPortTypeFromHex(hexLayout[9])].addElement(new Integer(0x25));
        ports[getPortTypeFromHex(hexLayout[9])].addElement(new Integer(0x34));

        ports[getPortTypeFromHex(hexLayout[21])].addElement(new Integer(0xCD));
        ports[getPortTypeFromHex(hexLayout[21])].addElement(new Integer(0xDC));

        ports[getPortTypeFromHex(hexLayout[22])].addElement(new Integer(0x43));
        ports[getPortTypeFromHex(hexLayout[22])].addElement(new Integer(0x52));

        ports[getPortTypeFromHex(hexLayout[32])].addElement(new Integer(0xC9));
        ports[getPortTypeFromHex(hexLayout[32])].addElement(new Integer(0xDA));

        ports[getPortTypeFromHex(hexLayout[33])].addElement(new Integer(0x72));
        ports[getPortTypeFromHex(hexLayout[33])].addElement(new Integer(0x83));

        ports[getPortTypeFromHex(hexLayout[35])].addElement(new Integer(0xA5));
        ports[getPortTypeFromHex(hexLayout[35])].addElement(new Integer(0xB6));
    }

    /**
     * @return the type of port given a hex type
     * @param hex  the hex type
     */
    public int getPortTypeFromHex(int hex)
    {
        int portType = 0;

        if ((hex >= 7) && (hex <= 12))
        {
            portType = 0;
        }
        else
        {
            portType = hex & 0xF;
        }

        return portType;
    }

    /**
     * set the number layout
     *
     * @param nl  the number layout
     */
    public void setNumberLayout(int[] nl)
    {
        numberLayout = nl;
    }

    /**
     * set where the robber is
     *
     * @param rh  the robber hex
     */
    public void setRobberHex(int rh)
    {
        robberHex = rh;
    }

    /**
     * @return the list of coordinates for a type of port
     *
     * @param portType  the type of port
     */
    public Vector getPortCoordinates(int portType)
    {
        return ports[portType];
    }

    /**
     * Given a hex coordinate, return the number on that hex
     *
     * @param hex  the coordinates for a hex
     *
     * @return the number on that hex
     */
    public int getNumberOnHexFromCoord(int hex)
    {
        return getNumberOnHexFromNumber(hexIDtoNum[hex]);
    }

    /**
     * Given a hex number, return the number on that hex
     *
     * @param hex  the number of a hex
     *
     * @return the number on that hex
     */
    public int getNumberOnHexFromNumber(int hex)
    {
        int num = numberLayout[hex];

        if (num < 0)
        {
            return 0;
        }
        else
        {
            return num2BoardNum[num];
        }
    }

    /**
     * Given a hex coordinate, return the type of hex
     *
     * @param hex  the coordinates for a hex
     *
     * @return the type of hex
     */
    public int getHexTypeFromCoord(int hex)
    {
        return getHexTypeFromNumber(hexIDtoNum[hex]);
    }

    /**
     * Given a hex number, return the type of hex
     *
     * @param hex  the number of a hex
     *
     * @return the type of hex
     */
    public int getHexTypeFromNumber(int hex)
    {
        int hexType = hexLayout[hex];

        if (hexType < 7)
        {
            return hexType;
        }
        else if ((hexType >= 7) && (hexType <= 12))
        {
            return MISC_PORT_HEX;
        }
        else
        {
            switch (hexType & 7)
            {
            case 1:
                return CLAY_PORT_HEX;

            case 2:
                return ORE_PORT_HEX;

            case 3:
                return SHEEP_PORT_HEX;

            case 4:
                return WHEAT_PORT_HEX;

            case 5:
                return WOOD_PORT_HEX;
            }
        }

        return -1;
    }

    /**
     * put a piece on the board
     */
    public void putPiece(SOCPlayingPiece pp)
    {
        pieces.addElement(pp);

        switch (pp.getType())
        {
        case SOCPlayingPiece.ROAD:
            roads.addElement(pp);

            break;

        case SOCPlayingPiece.SETTLEMENT:
            settlements.addElement(pp);

            break;

        case SOCPlayingPiece.CITY:
            cities.addElement(pp);

            break;
        }
    }

    /**
     * remove a piece from the board
     */
    public void removePiece(SOCPlayingPiece piece)
    {
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

                    break;

                case SOCPlayingPiece.SETTLEMENT:
                    settlements.removeElement(p);

                    break;

                case SOCPlayingPiece.CITY:
                    cities.removeElement(p);

                    break;
                }

                break;
            }
        }
    }

    /**
     * get the list of pieces on the board
     */
    public Vector getPieces()
    {
        return pieces;
    }

    /**
     * get the list of roads
     */
    public Vector getRoads()
    {
        return roads;
    }

    /**
     * get the list of settlements
     */
    public Vector getSettlements()
    {
        return settlements;
    }

    /**
     * get the list of cities
     */
    public Vector getCities()
    {
        return cities;
    }

    /**
     * @return the nodes that touch this edge
     */
    public static Vector getAdjacentNodesToEdge(int coord)
    {
        Vector nodes = new Vector(2);
        int tmp;

        /**
         * if the coords are (even, even), then
         * the road is '|'.
         */
        if ((((coord & 0x0F) + (coord >> 4)) % 2) == 0)
        {
            tmp = coord + 0x01;

            if ((tmp >= MINNODE) && (tmp <= MAXNODE))
            {
                nodes.addElement(new Integer(tmp));
            }

            tmp = coord + 0x10;

            if ((tmp >= MINNODE) && (tmp <= MAXNODE))
            {
                nodes.addElement(new Integer(tmp));
            }
        }
        else
        {
            /* otherwise the road is either '/' or '\' */
            tmp = coord;

            if ((tmp >= MINNODE) && (tmp <= MAXNODE))
            {
                nodes.addElement(new Integer(tmp));
            }

            tmp = coord + 0x11;

            if ((tmp >= MINNODE) && (tmp <= MAXNODE))
            {
                nodes.addElement(new Integer(tmp));
            }
        }

        return nodes;
    }

    /**
     * @return the adjacent edges to this edge
     */
    public static Vector getAdjacentEdgesToEdge(int coord)
    {
        Vector edges = new Vector(4);
        int tmp;

        /**
         * if the coords are (even, even), then
         * the road is '|'.
         */
        if ((((coord & 0x0F) + (coord >> 4)) % 2) == 0)
        {
            tmp = coord - 0x10;

            if ((tmp >= MINEDGE) && (tmp <= MAXEDGE))
            {
                edges.addElement(new Integer(tmp));
            }

            tmp = coord + 0x01;

            if ((tmp >= MINEDGE) && (tmp <= MAXEDGE))
            {
                edges.addElement(new Integer(tmp));
            }

            tmp = coord + 0x10;

            if ((tmp >= MINEDGE) && (tmp <= MAXEDGE))
            {
                edges.addElement(new Integer(tmp));
            }

            tmp = coord - 0x01;

            if ((tmp >= MINEDGE) && (tmp <= MAXEDGE))
            {
                edges.addElement(new Integer(tmp));
            }
        }

        /**
         * if the coords are (even, odd), then
         * the road is '/'.
         */
        else if (((coord >> 4) % 2) == 0)
        {
            tmp = coord - 0x11;

            if ((tmp >= MINEDGE) && (tmp <= MAXEDGE))
            {
                edges.addElement(new Integer(tmp));
            }

            tmp = coord + 0x01;

            if ((tmp >= MINEDGE) && (tmp <= MAXEDGE))
            {
                edges.addElement(new Integer(tmp));
            }

            tmp = coord + 0x11;

            if ((tmp >= MINEDGE) && (tmp <= MAXEDGE))
            {
                edges.addElement(new Integer(tmp));
            }

            tmp = coord - 0x01;

            if ((tmp >= MINEDGE) && (tmp <= MAXEDGE))
            {
                edges.addElement(new Integer(tmp));
            }
        }
        else
        {
            /**
             * otherwise the coords are (odd, even),
             * and the road is '\'
             */
            tmp = coord - 0x10;

            if ((tmp >= MINEDGE) && (tmp <= MAXEDGE))
            {
                edges.addElement(new Integer(tmp));
            }

            tmp = coord + 0x11;

            if ((tmp >= MINEDGE) && (tmp <= MAXEDGE))
            {
                edges.addElement(new Integer(tmp));
            }

            tmp = coord + 0x10;

            if ((tmp >= MINEDGE) && (tmp <= MAXEDGE))
            {
                edges.addElement(new Integer(tmp));
            }

            tmp = coord - 0x11;

            if ((tmp >= MINEDGE) && (tmp <= MAXEDGE))
            {
                edges.addElement(new Integer(tmp));
            }
        }

        return edges;
    }

    /**
     * @return the hexes touching this node
     */
    public static Vector getAdjacentHexesToNode(int coord)
    {
        Vector hexes = new Vector(3);
        int tmp;

        /**
         * if the coords are (even, odd), then
         * the node is 'Y'.
         */
        if (((coord >> 4) % 2) == 0)
        {
            tmp = coord - 0x10;

            if ((tmp >= MINHEX) && (tmp <= MAXHEX))
            {
                hexes.addElement(new Integer(tmp));
            }

            tmp = coord + 0x10;

            if ((tmp >= MINHEX) && (tmp <= MAXHEX))
            {
                hexes.addElement(new Integer(tmp));
            }

            tmp = coord - 0x12;

            if ((tmp >= MINHEX) && (tmp <= MAXHEX))
            {
                hexes.addElement(new Integer(tmp));
            }
        }
        else
        {
            /**
             * otherwise the coords are (odd, even),
             * and the node is 'upside down Y'.
             */
            tmp = coord - 0x21;

            if ((tmp >= MINHEX) && (tmp <= MAXHEX))
            {
                hexes.addElement(new Integer(tmp));
            }

            tmp = coord + 0x01;

            if ((tmp >= MINHEX) && (tmp <= MAXHEX))
            {
                hexes.addElement(new Integer(tmp));
            }

            tmp = coord - 0x01;

            if ((tmp >= MINHEX) && (tmp <= MAXHEX))
            {
                hexes.addElement(new Integer(coord - 0x01));
            }
        }

        return hexes;
    }

    /**
     * @return the edges touching this node
     */
    public static Vector getAdjacentEdgesToNode(int coord)
    {
        Vector edges = new Vector(3);
        int tmp;

        /**
         * if the coords are (even, odd), then
         * the node is 'Y'.
         */
        if (((coord >> 4) % 2) == 0)
        {
            tmp = coord - 0x11;

            if ((tmp >= MINEDGE) && (tmp <= MAXEDGE))
            {
                edges.addElement(new Integer(tmp));
            }

            tmp = coord;

            if ((tmp >= MINEDGE) && (tmp <= MAXEDGE))
            {
                edges.addElement(new Integer(tmp));
            }

            tmp = coord - 0x01;

            if ((tmp >= MINEDGE) && (tmp <= MAXEDGE))
            {
                edges.addElement(new Integer(tmp));
            }
        }
        else
        {
            /**
             * otherwise the coords are (odd, even),
             * and the EDGE is 'upside down Y'.
             */
            tmp = coord - 0x10;

            if ((tmp >= MINEDGE) && (tmp <= MAXEDGE))
            {
                edges.addElement(new Integer(tmp));
            }

            tmp = coord;

            if ((tmp >= MINEDGE) && (tmp <= MAXEDGE))
            {
                edges.addElement(new Integer(tmp));
            }

            tmp = coord - 0x11;

            if ((tmp >= MINEDGE) && (tmp <= MAXEDGE))
            {
                edges.addElement(new Integer(tmp));
            }
        }

        return edges;
    }

    /**
     * @return the EDGEs adjacent to this node
     */
    public static Vector getAdjacentNodesToNode(int coord)
    {
        Vector nodes = new Vector(3);
        int tmp;

        tmp = coord - 0x11;

        if ((tmp >= MINNODE) && (tmp <= MAXNODE))
        {
            nodes.addElement(new Integer(tmp));
        }

        tmp = coord + 0x11;

        if ((tmp >= MINNODE) && (tmp <= MAXNODE))
        {
            nodes.addElement(new Integer(tmp));
        }

        /**
         * if the coords are (even, odd), then
         * the node is 'Y'.
         */
        if (((coord >> 4) % 2) == 0)
        {
            tmp = (coord + 0x10) - 0x01;

            if ((tmp >= MINNODE) && (tmp <= MAXNODE))
            {
                nodes.addElement(new Integer((coord + 0x10) - 0x01));
            }
        }
        else
        {
            /**
             * otherwise the coords are (odd, even),
             * and the node is 'upside down Y'.
             */
            tmp = coord - 0x10 + 0x01;

            if ((tmp >= MINNODE) && (tmp <= MAXNODE))
            {
                nodes.addElement(new Integer(coord - 0x10 + 0x01));
            }
        }

        return nodes;
    }

    /**
     * @return true if the node is on the board
     */
    public boolean isNodeOnBoard(int node)
    {
        if (nodesOnBoard.containsKey(new Integer(node)))
        {
            return true;
        }
        else
        {
            return false;
        }
    }

    /**
     * @return a string representation of a node coordinate
     */
    public String nodeCoordToString(int node)
    {
        String str;
        Enumeration hexes = getAdjacentHexesToNode(node).elements();
        Integer hex = (Integer) hexes.nextElement();
        int number = getNumberOnHexFromCoord(hex.intValue());

        if (number == 0)
        {
            str = "-";
        }
        else
        {
            str = "" + number;
        }

        while (hexes.hasMoreElements())
        {
            hex = (Integer) hexes.nextElement();
            number = getNumberOnHexFromCoord(hex.intValue());

            if (number == 0)
            {
                str += "/-";
            }
            else
            {
                str += ("/" + number);
            }
        }

        return str;
    }

    /**
     * @return a string representation of an edge coordinate
     */
    public String edgeCoordToString(int edge)
    {
        String str;
        int number1;
        int number2;

        /**
         * if the coords are (even, even), then
         * the road is '|'.
         */
        if ((((edge & 0x0F) + (edge >> 4)) % 2) == 0)
        {
            number1 = getNumberOnHexFromCoord(edge - 0x11);
            number2 = getNumberOnHexFromCoord(edge + 0x11);
        }

        /**
         * if the coords are (even, odd), then
         * the road is '/'.
         */
        else if (((edge >> 4) % 2) == 0)
        {
            number1 = getNumberOnHexFromCoord(edge - 0x10);
            number2 = getNumberOnHexFromCoord(edge + 0x10);
        }
        else
        {
            /**
             * otherwise the coords are (odd, even),
             * and the road is '\'
             */
            number1 = getNumberOnHexFromCoord(edge - 0x01);
            number2 = getNumberOnHexFromCoord(edge + 0x01);
        }

        str = number1 + "/" + number2;

        return str;
    }
}
