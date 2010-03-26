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


/**
 * This message means that a new game has been created.
 *
 * @author Robert S Thomas
 */
public class SOCNewGame extends SOCMessage
{
    /**
     * Name of the new game.
     */
    private String game;

    /**
     * Create a NewGame message.
     *
     * @param ga  name of new game
     */
    public SOCNewGame(String ga)
    {
        messageType = NEWGAME;
        game = ga;
    }

    /**
     * @return the name of the game
     */
    public String getGame()
    {
        return game;
    }

    /**
     * NEWGAME sep game
     *
     * @return the command String
     */
    public String toCmd()
    {
        return toCmd(game);
    }

    /**
     * NEWGAME sep game
     *
     * @param ga  the new game name
     * @return    the command string
     */
    public static String toCmd(String ga)
    {
        return NEWGAME + sep + ga;
    }

    /**
     * Parse the command String into a NewGame message
     *
     * @param s   the String to parse
     * @return    a NewGame message
     */
    public static SOCNewGame parseDataStr(String s)
    {
        return new SOCNewGame(s);
    }

    /**
     * @return a human readable form of the message
     */
    public String toString()
    {
        return "SOCNewGame:game=" + game;
    }
}
