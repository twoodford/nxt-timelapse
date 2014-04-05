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

def runrobot(rconn, calsc, distsc):
    print("runrobot() started")
    time.sleep(5)
    while True:
        cal = calsc.get_value()
        dist = distsc.get_value()
        print("move")
        rconn.calibfw(dist-cal, dist+cal)
        time.sleep(2)

class MovementControls(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self, spacing=2)
        calibadj = Gtk.Adjustment(0, -20, 20, 1, 10)
        self.settings = Gtk.ListBox()
        self.calib = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=calibadj)
        self.calib.set_hexpand(True)
        self.calib.set_digits(0)
        self._make_row(self.settings, "Direction Calibration", self.calib)

        distadj = Gtk.Adjustment(100, 0, 5000, 1, 10)
        self.distance = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=distadj)
        self.distance.add_mark(100, Gtk.PositionType.TOP, "")
        self.distance.set_hexpand(True)
        self.distance.set_digits(0)
        self._make_row(self.settings, "Distance Moved", self.distance)
        self.pack_start(self.settings, True, True, 0)

    def _make_row(self, lbox, labeltxt, entry):
        label = Gtk.Label(labeltxt, xalign=0)
        hbox = Gtk.Box(spacing=6)
        row = Gtk.ListBoxRow()
        hbox.pack_start(label, True, True, 0)
        hbox.pack_start(entry, True, True, 0)
        row.add(hbox)
        lbox.add(row)

class RobotTestWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Test Window")
        self.mvctl = MovementControls()
        self.add(self.mvctl)

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
