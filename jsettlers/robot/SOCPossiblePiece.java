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

import java.util.Vector;


/**
 * Pieces that a player might build
 *
 * @author Robert S. Thomas
 */
public abstract class SOCPossiblePiece
{
    /**
     * Types of playing pieces
     */
    public static final int ROAD = 0;
    public static final int SETTLEMENT = 1;
    public static final int CITY = 2;
    public static final int CARD = 4;
    public static final int MIN = 0;
    public static final int MAXPLUSONE = 4;

    /**
     * The type of this playing piece
     */
    protected int pieceType;

    /**
     * The player who owns this piece
     */
    protected SOCPlayer player;

    /**
     * Where this piece is on the board
     */
    protected int coord;

    /**
     * this is how soon we estimate we can build
     * this piece measured in turns
     */
    protected int eta;

    /**
     * this is a flag used for updating
     */
    protected boolean updated;

    /**
     * this is a score used for deciding what to build next
     */
    protected float score;

    /**
     * this is the piece that we need to beat to build this one
     */
    protected Vector biggestThreats;

    /**
     * pieces that threaten this piece
     */
    protected Vector threats;

    /**
     * this flag is used for threat updating
     */
    protected boolean threatUpdatedFlag;

    /**
     * this flag is used for expansion
     */
    protected boolean hasBeenExpanded;

    /**
     * @return  the type of piece
     */
    public int getType()
    {
        return pieceType;
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

    /**
     * @return the eta for this piece
     */
    public int getETA()
    {
        return eta;
    }

    /**
     * update the eta for this piece
     *
     * @param e  the new eta
     */
    public void setETA(int e)
    {
        eta = e;
        updated = true;
    }

    /**
     * @return the value of the ETA update flag
     */
    public boolean isETAUpdated()
    {
        return updated;
    }

    /**
     * clear the update flag
     */
    public void clearUpdateFlag()
    {
        updated = false;
    }

    /**
     * reset the score
     */
    public void resetScore()
    {
        score = 0;
    }

    /**
     * add to score
     *
     * @param amt  the amount to add
     */
    public void addToScore(float amt)
    {
        score += amt;
    }

    /**
     * subtract from  score
     *
     * @param amt  the amount to subtract
     */
    public void subtractFromScore(float amt)
    {
        score -= amt;
    }

    /**
     * @return the score
     */
    public float getScore()
    {
        return score;
    }

    /**
     * reset the biggest threat
     */
    public void clearBiggestThreats()
    {
        biggestThreats.removeAllElements();
    }

    /**
     * set the biggest threat
     *
     * @param bt  the threat
     */
    public void addBiggestThreat(SOCPossiblePiece bt)
    {
        biggestThreats.addElement(bt);
    }

    /**
     * @return the biggest threat
     */
    public Vector getBiggestThreats()
    {
        return biggestThreats;
    }

    /**
     * @return the list of threats
     */
    public Vector getThreats()
    {
        return threats;
    }

    /**
     * add a threat to the list
     *
     * @param piece
     */
    public void addThreat(SOCPossiblePiece piece)
    {
        if (!threats.contains(piece))
        {
            threats.addElement(piece);
        }
    }

    /**
     * @return the status of the threatUpdatedFlag
     */
    public boolean isThreatUpdated()
    {
        return threatUpdatedFlag;
    }

    /**
     * clear the list of threats
     */
    public void clearThreats()
    {
        if (threatUpdatedFlag)
        {
            threats.removeAllElements();
            threatUpdatedFlag = false;
        }
    }

    /**
     * mark this piece as having been threat updated
     */
    public void threatUpdated()
    {
        threatUpdatedFlag = true;
    }

    /**
     * @return the status of the hasBeenExpanded flag
     */
    public boolean hasBeenExpanded()
    {
        return hasBeenExpanded;
    }

    /**
     * set hasBeenExpanded to false
     */
    public void resetExpandedFlag()
    {
        hasBeenExpanded = false;
    }

    /**
     * set hasBeenExpanded to true
     */
    public void setExpandedFlag()
    {
        hasBeenExpanded = true;
    }

    /**
     * @return a human readable form of this object
     */
    public String toString()
    {
        String s = "SOCPossiblePiece:type=" + pieceType + "|player=" + player + "|coord=" + Integer.toHexString(coord);

        return s;
    }
}
