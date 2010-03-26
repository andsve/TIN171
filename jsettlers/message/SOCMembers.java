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

import soc.server.genericServer.Connection;

import java.util.Enumeration;
import java.util.StringTokenizer;
import java.util.Vector;


/**
 * This message lists all the members of a chat channel
 *
 * @author Robert S Thomas
 */
public class SOCMembers extends SOCMessage
{
    /**
     * List of members
     */
    private Vector members;

    /**
     * Name of channel
     */
    private String channel;

    /**
     * Create a Members message.
     *
     * @param ch  name of chat channel
     * @param ml  list of members
     */
    public SOCMembers(String ch, Vector ml)
    {
        messageType = MEMBERS;
        members = ml;
        channel = ch;
    }

    /**
     * @return the list of members
     */
    public Vector getMembers()
    {
        return members;
    }

    /**
     * @return the channel name
     */
    public String getChannel()
    {
        return channel;
    }

    /**
     * MEMBERS sep channel sep2 members
     *
     * @return the command String
     */
    public String toCmd()
    {
        return toCmd(channel, members);
    }

    /**
     * MEMBERS sep channel sep2 members
     *
     * @param ch  the new channel name
     * @param ml  the list of members
     * @return    the command string
     */
    public static String toCmd(String ch, Vector ml)
    {
        String cmd = MEMBERS + sep + ch;

        try
        {
            Enumeration mlEnum = ml.elements();

            while (mlEnum.hasMoreElements())
            {
                Connection con = (Connection) mlEnum.nextElement();
                cmd += (sep2 + (String) con.data);
            }
        }
        catch (Exception e) {}

        return cmd;
    }

    /**
     * Parse the command String into a Members message
     *
     * @param s   the String to parse
     * @return    a Members message, or null of the data is garbled
     */
    public static SOCMembers parseDataStr(String s)
    {
        String ch;
        Vector ml = new Vector();
        StringTokenizer st = new StringTokenizer(s, sep2);

        try
        {
            ch = st.nextToken();

            while (st.hasMoreTokens())
            {
                ml.addElement(st.nextToken());
            }
        }
        catch (Exception e)
        {
            return null;
        }

        return new SOCMembers(ch, ml);
    }

    /**
     * @return a human readable form of the message
     */
    public String toString()
    {
        String s = "SOCMembers:channel=" + channel + "|members=";

        try
        {
            Enumeration mlEnum = members.elements();
            s += (String) mlEnum.nextElement();

            while (mlEnum.hasMoreElements())
            {
                s += ("," + (String) mlEnum.nextElement());
            }
        }
        catch (Exception e) {}

        return s;
    }
}
