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
package soc.message;

import java.util.StringTokenizer;


/**
 * This message says how many development cards are in the deck.
 *
 * @author Robert S. Thomas
 */
public class SOCDevCardCount extends SOCMessage
{
    /**
     * Name of game
     */
    private String game;

    /**
     * The number of dev cards
     */
    private int numDevCards;

    /**
     * Create a DevCardCount message.
     *
     * @param ga  the name of the game
     * @param nd  the number of dev cards
     */
    public SOCDevCardCount(String ga, int nd)
    {
        messageType = DEVCARDCOUNT;
        game = ga;
        numDevCards = nd;
    }

    /**
     * @return the name of the game
     */
    public String getGame()
    {
        return game;
    }

    /**
     * @return the number of dev cards
     */
    public int getNumDevCards()
    {
        return numDevCards;
    }

    /**
     * DEVCARDCOUNT sep game sep2 numDevCards
     *
     * @return the command string
     */
    public String toCmd()
    {
        return toCmd(game, numDevCards);
    }

    /**
     * DEVCARDCOUNT sep game sep2 numDevCards
     *
     * @param ga  the name of the game
     * @param nd  the number of dev cards
     * @return the command string
     */
    public static String toCmd(String ga, int nd)
    {
        return DEVCARDCOUNT + sep + ga + sep2 + nd;
    }

    /**
     * Parse the command String into a DevCardCount message
     *
     * @param s   the String to parse
     * @return    a DevCardCount message, or null of the data is garbled
     */
    public static SOCDevCardCount parseDataStr(String s)
    {
        String ga; // the game name
        int nd; // the number of dev cards 

        StringTokenizer st = new StringTokenizer(s, sep2);

        try
        {
            ga = st.nextToken();
            nd = Integer.parseInt(st.nextToken());
        }
        catch (Exception e)
        {
            return null;
        }

        return new SOCDevCardCount(ga, nd);
    }

    /**
     * @return a human readable form of the message
     */
    public String toString()
    {
        return "SOCDevCardCount:game=" + game + "|numDevCards=" + numDevCards;
    }
}
