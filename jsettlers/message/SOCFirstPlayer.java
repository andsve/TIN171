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
 * This message says who the first player is
 *
 * @author Robert S. Thomas
 */
public class SOCFirstPlayer extends SOCMessage
{
    /**
     * Name of game
     */
    private String game;

    /**
     * The seat number
     */
    private int playerNumber;

    /**
     * Create a FirstPlayer message.
     *
     * @param ga  the name of the game
     * @param pn  the seat number
     */
    public SOCFirstPlayer(String ga, int pn)
    {
        messageType = FIRSTPLAYER;
        game = ga;
        playerNumber = pn;
    }

    /**
     * @return the name of the game
     */
    public String getGame()
    {
        return game;
    }

    /**
     * @return the seat number
     */
    public int getPlayerNumber()
    {
        return playerNumber;
    }

    /**
     * FIRSTPLAYER sep game sep2 playerNumber
     *
     * @return the command string
     */
    public String toCmd()
    {
        return toCmd(game, playerNumber);
    }

    /**
     * FIRSTPLAYER sep game sep2 playerNumber
     *
     * @param ga  the name of the game
     * @param pn  the seat number
     * @return the command string
     */
    public static String toCmd(String ga, int pn)
    {
        return FIRSTPLAYER + sep + ga + sep2 + pn;
    }

    /**
     * Parse the command String into a StartGame message
     *
     * @param s   the String to parse
     * @return    a StartGame message, or null of the data is garbled
     */
    public static SOCFirstPlayer parseDataStr(String s)
    {
        String ga; // the game name
        int pn; // the seat number

        StringTokenizer st = new StringTokenizer(s, sep2);

        try
        {
            ga = st.nextToken();
            pn = Integer.parseInt(st.nextToken());
        }
        catch (Exception e)
        {
            return null;
        }

        return new SOCFirstPlayer(ga, pn);
    }

    /**
     * @return a human readable form of the message
     */
    public String toString()
    {
        return "SOCFirstPlayer:game=" + game + "|playerNumber=" + playerNumber;
    }
}
