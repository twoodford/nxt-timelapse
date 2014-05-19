# main.py
# Tie everything together for maximum fun
import threading
import time
from gi.repository import Gtk

import buildlapse.robot
import buildlapse.cameraparam
import buildlapse.gphoto2
import buildlapse.gui

def runloop(camera, robot, settings):
    while settings.running:
        if settings.cam_check.checked:
            camera.trigger_capture()
        if settings.move_check.checked:
            time.sleep(0.5)
            dist = settings.move_param.linear.get_value()
            robot.forward(dist)
        if settings.cam_check.checked:
            # This is not exactly the right time, but it will do for now
            time.sleep(settings.cam_param.frame_entry.get_value())
    if settings.move_check:
        print("Closing robot connection")
        robot.close()

class MainSettings(buildlapse.gui.ListBoxWindow):
    def __init__(self):
        super().__init__("BuildLapse Settings")
        
        self.cam_check = buildlapse.gui.CheckEntry("Timelapse Camera Capture", self.camtoggle)
        self.listbox.add(self.cam_check)
        self.cam_param = buildlapse.cameraparam.CameraParamWindow()

        self.move_check = buildlapse.gui.CheckEntry("Timelapse Motion Control", self.movetoggle)
        #self.move_check.set_sensitive(False)
        self.listbox.add(self.move_check)
        self.move_param = buildlapse.robot.TimelapseMotionSettings()

        self.start_button = Gtk.Button("Start Capture")
        self.start_button.connect("clicked", self.startstop_cap)
        self._make_row("Capture", self.start_button)

        self.running = False
    
    def _add_row(self, box):
        row = Gtk.ListBoxRow()
        row.add(box)
        self.listbox.add(row)

    def camtoggle(self, button, name):
        if self.cam_check.checked:
            self.move_check.set_sensitive(True)
            self.cam_param.show_all()
        else:
            self.move_check.set_sensitive(False)
            self.move_check.checked = False
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
        else:
            self.start_button.set_label("Stop Capture")
            self.running = True
            if self.cam_check.checked:
                camera = buildlapse.gphoto2.GPTether()
                camera.connect_camera()
            else:
                camera = None
            if self.move_check.checked:
                robot = buildlapse.robot.RobotCtl()
            else:
                robot = None
            thr = threading.Thread(target=runloop, args=(camera, robot, self))
            thr.start()

def run():
    ctl = MainSettings()
    ctl.connect("delete-event", Gtk.main_quit)
    ctl.show_all()
    Gtk.main()

if __name__=="__main__":
    run()
