from gi.repository import Gtk
import multiprocessing

from buildlapse.gui import ListBoxWindow, mkspin, TimeEntry

class CameraParamWindow(ListBoxWindow):
    running = False

    def __init__(self):
        super().__init__("Camera Parameters")

        self.shutterentry = Gtk.Entry() # TODO show the list from gphoto
        self._make_row("Shutter Time", self.shutterentry)
 
if __name__=="__main__":
    win = CameraParamWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
