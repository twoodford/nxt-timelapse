# robot.py
# An interface to the Java-based robot controller
import subprocess
import threading
import time
from gi.repository import Gtk

class RobotCtl(object):
    def __init__(self):
        self.sproc = subprocess.Popen(["nxjpc", "CameraComm"], stdin = subprocess.PIPE, stdout=subprocess.PIPE)
        self.sproc.stdout.readline() # Wait for startup
    
    def _write(self, msg):
        self.sproc.stdin.write(bytes(msg, "ascii"))
        self.sproc.stdin.flush()

    def calibfw(self, left, right):
        self._write("calibfw {0} {1}\n".format(int(left), int(right)))

    def close(self):
        self._write("quit\n")
        #self.sproc.communicate()

class TimelapseMotionSettings(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Timelapse Motion")

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
