try:
    import wx
    from wx import glcanvas
except ImportError:
    raise ImportError, "Required dependency wx.glcanvas not present"

try:
    from OpenGL.GL import *
    from OpenGL.GLUT import *
except ImportError:
    raise ImportError, "Required dependency OpenGL not present"

import client
import logging
from jsettlers_utils import hex_grid, roads_around_hex2


#class PApp(wx.PySimpleApp):
#    def OnIdle(self, evt):
#        print("SEPPPPPPPPPPPPPE")

class GLFrame(wx.Frame):
    """A simple class for using OpenGL with wxPython."""

    def __init__(self, parent, id, title, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE,
                 name='frame'):
        
        self.w = size[0]
        self.h = size[1]
        self.score = None
        
        # Setup bot client
        self.client = client.Client()
        if not self.client.connect(("doff.csbnet.se", int(8880))):
            print("Could not connect to: {0}".format("doff.csbnet.se"))
            exit(-1)
        
        self.client.setup(None, True, 1, None)
        self.render = True
        
        # Resource history
        self.res_history = []
        self.last_r = [0, 0, 0, 0, 0]
        
        #
        # Forcing a specific style on the window.
        #   Should this include styles passed?
        style = wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE

        super(GLFrame, self).__init__(parent, id, title, pos, size, style, name)

        self.GLinitialized = False
        attribList = (glcanvas.WX_GL_RGBA, # RGBA
                      glcanvas.WX_GL_DOUBLEBUFFER, # Double Buffered
                      glcanvas.WX_GL_DEPTH_SIZE, 24) # 24 bit

        #
        # Create the canvas
        self.canvas = glcanvas.GLCanvas(self, attribList=attribList)

        #
        # Set the event handlers.
        self.canvas.Bind(wx.EVT_ERASE_BACKGROUND, self.processEraseBackgroundEvent)
        self.canvas.Bind(wx.EVT_SIZE, self.processSizeEvent)
        self.canvas.Bind(wx.EVT_PAINT, self.processPaintEvent)
        self.Bind(wx.EVT_IDLE, self.OnIdle)
        #app.Bind(wx.EVT_INTERNAL_IDLE, self.processPaintEvent)
        
        # Start client thread
        #t = ThreadClient("testnick", "doff.csbnet.se", 8880, self.OnDraw)
        #t.start()
        wx.CallAfter(self.OnDraw, None, None)
        

    #
    # Canvas Proxy Methods

    def GetGLExtents(self):
        """Get the extents of the OpenGL canvas."""
        return self.canvas.GetClientSize()

    def SwapBuffers(self):
        """Swap the OpenGL buffers."""
        self.canvas.SwapBuffers()

    #
    # wxPython Window Handlers

    def processEraseBackgroundEvent(self, event):
        """Process the erase background event."""
        pass # Do nothing, to avoid flashing on MSWin

    def processSizeEvent(self, event):
        """Process the resize event."""
        if self.canvas.GetContext():
            # Make sure the frame is shown before calling SetCurrent.
            self.Show()
            self.canvas.SetCurrent()

            size = self.GetGLExtents()
            self.OnReshape(size.width, size.height)
            self.canvas.Refresh(False)
        event.Skip()

    def processPaintEvent(self, event):
        """Process the drawing event."""
        self.canvas.SetCurrent()

        # This is a 'perfect' time to initialize OpenGL ... only if we need to
        if not self.GLinitialized:
            self.OnInitGL()
            self.GLinitialized = True

        self.OnDraw()
        event.Skip()

    #
    # GLFrame OpenGL Event Handlers

    def OnInitGL(self):
        """Initialize OpenGL for use in the window."""
        glClearColor(1, 1, 1, 1)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_GEQUAL)
        glClearDepth(-1.0)
        glLineWidth(6.0)

    def OnReshape(self, width, height):
        """Reshape the OpenGL viewport based on the dimensions of the window."""
        self.w = width
        self.h = height
        glViewport(0, 0, width, height)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-0.1, 1.6, 1.2, -0.1, 1.0, -1.0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
    def OnIdle(self, evt):
        # Update client, and draw if needed
        if self.render:
            self.score = self.client.run_update()
            if self.score != None:
                self.render = False
        self.OnDraw()
        evt.RequestMore()
    
    def DrawText(self, x, y, txt, color=(0.0, 0.0, 0.0)):
        glColor(color)
        glRasterPos(x,y,1)
        for c in txt:
            glutBitmapCharacter(GLUT_BITMAP_8_BY_13, ord(c))
        
    def OnDraw(self, *args, **kwargs):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Drawing an example triangle in the middle of the screen
        
        i = 0
        sized = 1.0/7.0
        size2 = sized / 2.0
        size4 = size2 / 2.0
        for y in range(7):
            w = y
            if y > 3:
                w = 6 - y
            for x in range(4+w):
                id = hex_grid[i]
                res = -1
                if (y == 0 or y == 6) or (x == 0 or x == 3+w):
                    res = 6 # Water
                else:
                    if self.client.game and self.client.game.boardLayout:
                        res = int(self.client.game.boardLayout.tiles[id].resource)
                    
                self.DrawTile(0.5 - sized - size2 +
                              x*sized + -w*size2,
                              size2 + (size2 + size4)*y,
                              res, id)
                i += 1
        
        # Calculate bonus
        bonus_lst = [0, 0, 0, 0]
        for i in range(4):
            if self.client.game:
                bonus = 2 if i == self.client.game.longest_road else 0
                bonus += 2 if i == self.client.game.largest_army else 0
                bonus_lst[i] += bonus
            
        
        # Display player info
        self.DrawText(0.01, -0.05, "Player: {0}, Game: {1}, Seat: {2}".format(self.client.nickname, self.client.gamename, self.client.seat_num))
        if self.client.agent:
            self.DrawText(1.2, -0.05, "Agent score: {0}".format(bonus_lst[self.client.seat_num] + self.client.agent.resources["VICTORY_CARDS"] + self.client.game.vp[int(self.client.seat_num)]))
            
            self.DrawText(1.2, 0.3, "'Public' scores:")
            for i in range(4):
                prefix = "-> " if self.client.stats["ACTIVE_PLAYER"] == i else "   "
                self.DrawText(1.20, 0.35+i*0.04, prefix + "Player {0}: {1}".format(i, self.client.game.vp[i] + bonus_lst[i]))
        
        # Resources
        res_lut = ["Clay", "Ore", "Sheep", "Wheat", "Wood"]
        rposx = 1.2
        rposy = 0.0
        rsize = 0.04
        round_res = [0, 0, 0, 0, 0]
        for i in range(5):
            glColor(self.TileToColor(i+1))
            glBegin(GL_QUADS)
            glVertex(rposx, rposy, 1.0)
            glVertex(rposx+rsize, rposy, 1.0)
            glVertex(rposx+rsize, rposy+rsize, 1.0)
            glVertex(rposx, rposy+rsize, 1.0)
            glEnd()
            
            if self.client.game and self.client.game.resources:
                round_res[i] = (self.client.game.resources[res_lut[i].upper()])
                self.DrawText(rposx + rsize * 1.2, rposy + rsize / 1.5, "{0}: {1}".format(res_lut[i], self.client.game.resources[res_lut[i].upper()]))
            
            rposy += rsize * 1.1
        
        if len(self.res_history) > 0:
            self.last_r = self.res_history[-1]
            
        if self.last_r != round_res:
            self.res_history.append(round_res)
        
        # Resource histogram
        num_history = 50
        rposx = 0.0
        rposy = 1.1
        rh = 0.2
        rsize = 1.5
        rstep = rsize / num_history
        
        glColor((0, 0, 0))
        glBegin(GL_LINES)
        glVertex(rposx, rposy, 1.0)
        glVertex(rposx+rsize, rposy, 1.0)
        glEnd()
        
        if len(self.res_history) > 0:
            last_r = self.res_history[-num_history:][0]
            for r in self.res_history[-num_history:]:
                for i in range(5):
                    glColor(self.TileToColor(i+1))
                    glBegin(GL_LINES)
                    glVertex(rposx, rposy-last_r[i]/20.0, 1.0)
                    glVertex(rposx+rstep, rposy-r[i]/20.0, 1.0)
                    glEnd()
                last_r = r
                rposx += rstep
                
        
        
        self.SwapBuffers()
    
    def TileToColor(self, id):
        if id == 0:
            return (0.1, 0.1, 0.1) # Desert
        elif id == 1:
            return (219.0/256.0, 122.0/256.0, 7.0/256.0) # Clay
        elif id == 2:
            return (115.0/256.0, 155.0/256.0, 155.0/256.0) # Ore
        elif id == 3:
            return (224.0/256.0, 224.0/256.0, 224.0/256.0) # Sheep
        elif id == 4:
            return (197.0/256.0, 173.0/256.0, 11.0/256.0) # Grain
        elif id == 5:
            return (153.0/256.0, 110.0/256.0, 55.0/256.0) # Lumber
        elif id == 6:
            return (2.0/256.0, 20.0/256.0, 110.0/256.0) # Sea
        
        return (1.0, 1.0, 0.0)
    
    def DrawTile(self, x, y, res, id):
        glColor(self.TileToColor(res))
        sized = 1.0/7.0
        size2 = sized / 2.0
        size4 = size2 / 2.0
        d = 0.0
        if res == 6:
            d = -1.0
        
        glBegin(GL_TRIANGLE_FAN)
        glVertex(x, y, d)
        glVertex(x-size2, y-size4, d)
        glVertex(x, y-size2, d)
        glVertex(x+size2, y-size4, d)
        glVertex(x+size2, y+size4, d)
        glVertex(x, y+size2, d)
        glVertex(x-size2, y+size4, d)
        glVertex(x-size2, y-size4, d)
        glEnd()
        
        # Draw number
        if res != -1 and res != 6 and self.client.game.boardLayout.tiles[id]:
            self.DrawText(x - size4/4.0, y + size4/4.0,
                          str(self.client.game.boardLayout.tiles[id].number))
        
        # Draw nodes
        n1 = None
        n2 = None
        n3 = None
        n4 = None
        n5 = None
        n6 = None
        if res != -1 and res != 6:
            if self.client.game and self.client.game.boardLayout:
                n1 = self.client.game.boardLayout.tiles[id].n1
                n2 = self.client.game.boardLayout.tiles[id].n2
                n3 = self.client.game.boardLayout.tiles[id].n3
                n4 = self.client.game.boardLayout.tiles[id].n4
                n5 = self.client.game.boardLayout.tiles[id].n5
                n6 = self.client.game.boardLayout.tiles[id].n6
            self.DrawNode(x, y-size2, n1)             # n1
            self.DrawNode(x+size2, y-size4, n2)       # n2
            self.DrawNode(x+size2, y+size4, n3)       # n3
            self.DrawNode(x, y+size2, n4)             # n4
            self.DrawNode(x-size2, y+size4, n5)       # n5
            self.DrawNode(x-size2, y-size4, n6)       # n6
        
        # Draw roads
        if res != -1 and res != 6:
            roads = roads_around_hex2(id)
            
            self.DrawRoad(x-size2, y+size4, x-size2, y-size4, roads[0])      # r0
            self.DrawRoad(x-size2, y-size4, x, y-size2, roads[1])            # r1
            self.DrawRoad(x, y-size2, x+size2, y-size4, roads[2])            # r2
            self.DrawRoad(x+size2, y-size4, x+size2, y+size4, roads[3])      # r3
            self.DrawRoad(x+size2, y+size4, x, y+size2, roads[4])            # r4
            self.DrawRoad(x, y+size2, x-size2, y+size4, roads[5])            # r5
            
    def DrawRoad(self, x1, y1, x2, y2, road_id):
        owner = self.client.game.boardLayout.roads[road_id].owner
        
        if owner != None:
            glColor(player_colors[owner])
            glBegin(GL_LINES)
            glVertex(x1, y1, 1.0)
            glVertex(x2, y2, 1.0)
            glEnd()
        
    def DrawNode(self, x, y, node):
        
        sized = (1.0/7.0) / 5
        size2 = sized / 2.0
        
        if node != None:
            node = self.client.game.boardLayout.nodes[node]
        
        if node != None and node.owner != None:
            glColor(player_colors[node.owner])
            glBegin(GL_TRIANGLE_FAN)
            
            if node.type == 1:
                glVertex(x, y, 1.0)
                glVertex(x+size2, y, 1.0)
                glVertex(x+size2, y+sized, 1.0)
                glVertex(x-size2, y+sized, 1.0)
                glVertex(x-size2, y, 1.0)
                glVertex(x, y-size2, 1.0)
                glVertex(x+size2, y, 1.0)
            else:
                glVertex(x, y, 1.0)
                glVertex(x+sized, y, 1.0)
                glVertex(x+sized, y+sized, 1.0)
                glVertex(x-sized, y+sized, 1.0)
                glVertex(x-sized, y, 1.0)
                glVertex(x-size2, y-sized, 1.0)
            
            glEnd()
    

# color lookup for player ids
player_colors = [(0.0, 0.0, 1.0),
                 (1.0, 0.0, 0.0),
                 (1.0, 1.0, 1.0),
                 (1.0, 1.0, 0.0)]

if __name__ == '__main__':
    import sys
    import os
    import time

    if os.name == 'nt':
        os.system("mode 80,60")
        os.system("mode con: cols=80 lines=900")
    
    #logging.disable(logging.INFO)
    js_logger = logging.getLogger("")
    logging.basicConfig(filename="robot-output.{0}.log".format(time.strftime("%H%M%S")),filemode="w",level=logging.DEBUG,format="%(module)s:%(levelname)s: %(message)s")
    js_logger.addHandler(client.logconsole)
    
    try:
        app = wx.PySimpleApp(redirect=False)
        frame = GLFrame(None, -1, 'Settlers of Awesome', size = (800,700))
        frame.Show()

        app.MainLoop()
        app.Destroy()
            
            
    except:
        import pdb
        import traceback
        traceback.print_exc(file=sys.stdout)
        pdb.set_trace()