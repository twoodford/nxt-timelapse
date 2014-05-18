# main.py
# Tie everything together for maximum fun
import time
from gi.repository import Gtk

import buildlapse.robot
import buildlapse.cameraparam
import buildlapse.gphoto2
import buildlapse.gui

def runloop(camera, robot, campanel, movepanel):
    while campanel.running:
        camera.trigger_capture()
        time.sleep(0.5)
        cal = movepanel.calib.get_value()
        dist = movepanel.distance.get_value()
        robot.calibfw(dist-cal, dist+cal)
        # This is not exactly the right time, but it will do for now
        time.sleep(campanel.totalseconds)

class MainSettings(buildlapse.gui.ListBoxWindow):
    def __init__(self):
        super().__init__("BuildLapse Settings")
        
        self.cam_check = buildlapse.gui.CheckEntry("Timelapse Capture", self.camtoggle)
        self.listbox.add(self.cam_check)
        self.cam_param = buildlapse.cameraparam.CameraParamWindow()

        self.move_check = buildlapse.gui.CheckEntry("Timelapse Motion Control", self.movetoggle)
        self.listbox.add(self.move_check)
        self.move_param = buildlapse.robot.TimelapseMotionSettings()

        self.start_button = Gtk.Button("Start Capture")
        self.start_button.connect("clicked", self.startstop_cap)
        self._make_row("Capture", self.start_button)
    
    def _add_row(self, box):
        row = Gtk.ListBoxRow()
        row.add(box)
        self.listbox.add(row)

    def camtoggle(self, button, name):
        if self.cam_check.checked:
            self.cam_param.show_all()
        else:
            self.cam_param.hide()

    def movetoggle(self, button, name):
        if self.move_check.checked:
            self.move_param.show_all()
        else:
            self.move_param.hide()

    def startstop_cap(self, sender):
        if self.running:
            self.start_button.set_label("Start Capture")
            self.running = False
            self.subproc.terminate()
        else:
            self.start_button.set_label("Stop Capture")
            self.running = True
            framelen = int(self.frame_entry.get_value())
            numshots = int(self.total_shots_entry.get_value())
            robot = buildlapse.robot.RobotCtl()
            thr = threading.Thread(target=runloop, args=(camera, robot, self, self.mvpanel))
            thr.start()

def run():
    ctl = MainSettings()
    ctl.connect("delete-event", Gtk.main_quit)
    ctl.show_all()
    Gtk.main()

if __name__=="__main__":
    run()
