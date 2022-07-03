import os
import cairo
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

from lib_vars import *
from lib_elements import *
from lib_commands import *
from lib_expressions import *

from construction import *

#--------------------------------------------------------------------------

class DisplayWindow(Gtk.Window):

    def __init__(self, width, height, construction):
        super(DisplayWindow, self).__init__()

        self.construction = construction
        self.construction.rebuild()

        self.oxy = [width / 2, height / 2]
        self.scale = min(width / 8, height / 8)
        self.size = [width, height]

        #далее внутренние аттрибуты Gtk.Window

        self.darea = Gtk.DrawingArea()
        self.darea.connect("draw", self.on_draw)
        self.darea.set_events(Gdk.EventMask.KEY_PRESS_MASK)
        self.add(self.darea)

        self.connect("key-press-event", self.on_key_press)

        self.set_title("Display")
        self.resize(width, height)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()
    
    def X(self, value):
        return value * self.scale + self.oxy[0]
    def Y(self, value):
        return value * self.scale + self.oxy[1]

    def on_draw(self, w, cr):
        for element in self.construction.elements:
            if type(element.data) == Point:
                x = self.X(element.data.a[0])
                y = self.Y(element.data.a[1])
                cr.arc(x, y, 3, 0, 2 * np.pi)
                cr.fill()

    def on_key_press(self, w, e):
        keyval_name = Gdk.keyval_name(e.keyval)
        print(keyval_name)

        if  keyval_name == "space":
            rebuild = True
        elif keyval_name == "Escape":
            Gtk.main_quit()
        else:
            return False

        if rebuild:
            self.construction.rebuild()
            self.darea.queue_draw()
