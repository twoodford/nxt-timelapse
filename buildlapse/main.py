# main.py
# Tie everything together for maximum fun
import threading
import time
from gi.repository import Gtk, GLib

import buildlapse.robot
import buildlapse.cameraparam
import buildlapse.gphoto2
import buildlapse.gui

def runloop(camera, robot, settings, progress):
    i = 0
    while settings.running:
        st_time = time.monotonic()
        if settings.cam_check.checked:
            if settings.cam_param.total_shots < i:
                settings.running = False
                break
            camera.trigger_capture()
        if settings.move_check.checked:
            time.sleep(0.5)
            # Can't call this outside of main thread because GTK isn't thread-safe
            #settings.move_param.linear.doupdate()
            dist = settings.move_param.linear.position
            robot.forward(dist)
        if settings.cam_check.checked:
            progress.fraction = i/settings.cam_param.total_shots
            # Triggering the capture and moving the robot takes time (although, 
            # bizarrely, trigger_capture() doesn't necessarily wait until the 
            # shutter is closed).  Take this time into account to improve both 
            # accuracy (fixed time delays) and precision (variable latency in 
            # USB communication).
            elapsed_time = time.monotonic() - st_time
            time.sleep(settings.cam_param.frame_entry.get_value() - elapsed_time)
        i+=1
    if settings.move_check.checked:
        print("Closing robot connection")
        robot.close()
    settings.start_button.set_label("Start Capture")
    progress.hide()

def gui_update(settings):
    settings.move_param.linear.doupdate()
    if settings.running:
        if settings.cam_check.checked:
            GLib.timeout_add(settings.cam_param.frame_entry.get_value() * 1000, settings)
        else:
            GLib.timeout_add(1000, gui_update, settings)
    return False

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

        self.progress = ProgressWindow()
        self.progress.set_no_show_all(True)
        self.listbox.add(self.progress)

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
            self.running = False
        else:
            self.start_button.set_label("Stop Capture")
            self.running = True
            self.numshots = 0
            if self.cam_check.checked:
                camera = buildlapse.gphoto2.GPTether()
                camera.connect_camera()
            else:
                camera = None
            if self.move_check.checked:
                robot = buildlapse.robot.RobotCtl()
            else:
                robot = None
            self.progress.set_no_show_all(False)
            self.progress.show_all()
            thr = threading.Thread(target=runloop, args=(camera, robot, self, self.progress))
            thr.start()
            gui_update(self)

class ProgressWindow(Gtk.Box):
    def __init__(self):
        super().__init__()
        self.progress = Gtk.ProgressBar()
        self.add(self.progress)

    @property
    def fraction(self):
        return self.progress.fraction

    @fraction.setter
    def fraction(self, value):
        self.progress.set_fraction(value)

def run():
    ctl = MainSettings()
    ctl.connect("delete-event", Gtk.main_quit)
    ctl.show_all()
    Gtk.main()

if __name__=="__main__":
    run()
