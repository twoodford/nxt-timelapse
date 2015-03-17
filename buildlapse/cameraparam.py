from gi.repository import Gtk

from buildlapse.gui import ListBoxWindow, mkspin, TimeEntry
import buildlapse.gphoto2
import subprocess

class CameraParamWindow(ListBoxWindow):
    running = False

    def __init__(self):
        super().__init__("Camera Parameters")

        self.shutterentry = Gtk.Entry() # TODO show the list from gphoto
        # cam.root_widget.child_by_name("main").child_by_name("capturesettings").child_by_name("shutterspeed2").choices
        self._make_row("Shutter Time", self.shutterentry)

    def action(self):
        class _camaction(object):
            def setup(slf):
                # Connect to camera
                slf.cam = buildlapse.gphoto2.GPTether()
                slf.cam.connect_camera()
                print("connected camera")

            def __call__(slf):
                # This may be where we want to set parameters
                print("triggering capture")
                slf.cam.trigger_capture()
                print("end")

            def cleanup(slf):
                pass # Wish there was a way to hard-dealloc a camera
        return _camaction()
 
class CLICallCamParam(CameraParamWindow):
    def action(self):
        class _camaction(object):
            def setup(slf):
                pass
            def __call__(slf):
                subprocess.call(["gphoto2", "--trigger-capture"])
            def cleanup(slf):
                pass
        return _camaction()

if __name__=="__main__":
    #win = CameraParamWindow()
    win=CLICallCamParam()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
