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
 * This message contains a text message for everyone connected
 *
 * @author Robert S Thomas
 */
public class SOCBCastTextMsg extends SOCMessage
{
    /**
     * Text message
     */
    private String text;

    /**
     * Create a BCastTextMsg message.
     *
     * @param tm  text message
     */
    public SOCBCastTextMsg(String tm)
    {
        messageType = BCASTTEXTMSG;
        text = tm;
    }

    /**
     * @return the text message
     */
    public String getText()
    {
        return text;
    }

    /**
     * BCASTTEXTMSG sep text
     *
     * @return the command String
     */
    public String toCmd()
    {
        return toCmd(text);
    }

    /**
     * BCASTTEXTMSG sep text
     *
     * @param tm  the text message
     * @return    the command string
     */
    public static String toCmd(String tm)
    {
        return BCASTTEXTMSG + sep + tm;
    }

    /**
     * Parse the command String into a BCastTextMsg message
     *
     * @param s   the String to parse
     * @return    a BCastTextMsg message, or null of the data is garbled
     */
    public static SOCBCastTextMsg parseDataStr(String s)
    {
        return new SOCBCastTextMsg(s);
    }

    /**
     * @return a human readable form of the message
     */
    public String toString()
    {
        String s = "SOCBCastTextMsg:text=" + text;

        return s;
    }
}
