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

import soc.game.SOCPlayer;


/**
 * DOCUMENT ME!
 *
 * @author $author$
 * @version $Revision: 1.1 $
 */
public class SOCPlayerAction
{
    /**
     * possible actions
     */
    public static final int PLACE_ROAD = 0;
    public static final int PLACE_SETTLEMENT = 1;
    public static final int PLACE_CITY = 2;
    public static final int PLAY_KNIGHT = 3;
    public static final int DRAW_VP = 4;
    public static final int REMOVE_KNIGHT = 5;
    public static final int REMOVE_VP = 6;

    /**
     * The type of action
     */
    protected int actionType;

    /**
     * The player who owns this piece
     */
    protected SOCPlayer player;

    /**
     * Where this piece is on the board
     */
    protected int coord;

    /**
     * constructor
     */
    public SOCPlayerAction(int type, SOCPlayer pl, int co)
    {
        actionType = type;
        player = pl;
        coord = co;
    }

    /**
     * @return  the type of piece
     */
    public int getType()
    {
        return actionType;
    }

    /**
     * @return the owner of the piece
     */
    public SOCPlayer getPlayer()
    {
        return player;
    }

    /**
     * @return the coordinates for this piece
     */
    public int getCoordinates()
    {
        return coord;
    }
}
