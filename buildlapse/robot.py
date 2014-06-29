# robot.py
# An interface to the Java-based robot controller
import subprocess
import threading
import time

from gi.repository import Gtk
import buildlapse.gui

class RobotCtl(object):
    def __init__(self):
        self.sproc = subprocess.Popen(["nxjpc", "CameraComm"], stdin = subprocess.PIPE, stdout=subprocess.PIPE)
        self.sproc.stdout.readline() # Wait for startup
    
    def _write(self, msg):
        self.sproc.stdin.write(bytes(msg, "ascii"))
        self.sproc.stdin.flush()

    def forward(self, degrees):
        self._write("forward {0}\n".format(int(degrees)))

    def close(self):
        self._write("quit\n")
        #self.sproc.communicate()

class TimelapseMotionSettings(buildlapse.gui.ListBoxWindow):
    def __init__(self):
        super().__init__("Timelapse Motion")
        self.linear = buildlapse.gui.mkspin2(-3600, 3600)
        self._make_row("Linear Degrees Per Capture", self.linear)

if __name__=="__main__":
    win = RobotTestWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    rctl = RobotCtl()
    print("Connection started")
    thr = threading.Thread(target=runrobot, args=(rctl, win.mvctl.calib, win.mvctl.distance))
    thr.start()
    import atexit
    def cleanup():
        print("Closing")
        rctl.close()
    atexit.register(cleanup)
    Gtk.main()
    #rctl.calibfw(100, 300) 
