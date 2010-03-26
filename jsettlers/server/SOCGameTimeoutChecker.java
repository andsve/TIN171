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
package soc.server;


/**
 * Wakes up to check for games that have expired
 *
 * @author Robert S Thomas
 */
public class SOCGameTimeoutChecker extends Thread
{
    SOCServer server;
    boolean alive;

    /**
     * Create a game timeout checker
     *
     * @param srv  the game server
     */
    public SOCGameTimeoutChecker(SOCServer srv)
    {
        server = srv;
        alive = true;
    }

    /**
     * DOCUMENT ME!
     */
    public void run()
    {
        while (alive)
        {
            server.checkForExpiredGames();
            yield();

            try
            {
                // check every 5 minutes
                sleep(300000);
            }
            catch (InterruptedException exc) {}
        }

        server = null;
    }

    /**
     * DOCUMENT ME!
     */
    public void stopChecking()
    {
        alive = false;
    }
}
