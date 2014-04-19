# main.py
# Tie everything together for maximum fun
import time
import threading
from gi.repository import Gtk

import buildlapse.robot
import buildlapse.cameraparam
import buildlapse.gphoto2

def runloop(camera, robot, campanel, movepanel):
    while campanel.running:
        camera.trigger_capture()
        time.sleep(0.5)
        cal = movepanel.calib.get_value()
        dist = movepanel.distance.get_value()
        robot.calibfw(dist-cal, dist+cal)
        # This is not exactly the right time, but it will do for now
        time.sleep(campanel.frame_entry.totalseconds)

class CameraParams(buildlapse.cameraparam.CameraParamWindow):
    def __init__(self):
        super().__init__()
        self.mvpanel = buildlapse.robot.MovementControls()
        self.timesettings.add(self.mvpanel)

    def startstop_cap(self, sender):
        if self.running:
            self.start_button.set_label("Start Capture")
            self.running = False
        else:
            self.start_button.set_label("Stop Capture")
            self.running = True
            framelen = int(self.frame_entry.get_value())
            numshots = int(self.total_shots_entry.get_value())
            camera = buildlapse.gphoto2.GPTether()
            camera.connect_camera()
            robot = buildlapse.robot.RobotCtl()
            thr = threading.Thread(target=runloop, args=(camera, robot, self, self.mvpanel))
            thr.start()

def run():
    camctl = CameraParams()
    camctl.connect("delete-event", Gtk.main_quit)
    camctl.show_all()
    Gtk.main()

if __name__=="__main__":
    run()
