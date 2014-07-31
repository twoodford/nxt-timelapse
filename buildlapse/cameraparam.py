from gi.repository import Gtk

from buildlapse.gui import ListBoxWindow, mkspin, TimeEntry
import buildlapse.gphoto2

class CameraParamWindow(ListBoxWindow):
    running = False

    def __init__(self):
        super().__init__("Camera Parameters")

        self.shutterentry = Gtk.Entry() # TODO show the list from gphoto
        self._make_row("Shutter Time", self.shutterentry)

    def action(self):
        class _camaction(object):
            def setup(slf):
                # Connect to camera
                slf.cam = buildlapse.gphoto2.GPTether()
                slf.cam.connect_camera()

            def __call__(slf):
                # This may be where we want to set parameters
                slf.cam.trigger_capture()

            def cleanup(slf):
                pass # Wish there was a way to hard-dealloc a camera
        return _camaction()
 
if __name__=="__main__":
    win = CameraParamWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
