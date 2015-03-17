# main.py
# Tie everything together for maximum fun
from gi.repository import Gtk

import buildlapse.robot
import buildlapse.cameraparam
import buildlapse.gui
import buildlapse.timing

class MainSettings(buildlapse.gui.ListBoxWindow):
    def __init__(self):
        super().__init__("BuildLapse Settings")
        
        self.cam_check = buildlapse.gui.CheckEntry("Camera Capture", self.camtoggle)
        self.listbox.add(self.cam_check)
        # Pick one.  CameraParam doesn't work for me now, possibly because 
        # I need to pull pictures off the camera for some reason.
        self.cam_param = buildlapse.cameraparam.CLICallCamParam()
        #self.cam_param = buildlapse.cameraparam.CameraParamWindow()

        # Why pass self?  Because thread safety. Ugliness can't always
        # go away :(
        self.time_param = buildlapse.timing.TimingParamWindow(self)
        self.time_param.show_all()

        self.move_check = buildlapse.gui.CheckEntry("Motion Control", self.movetoggle)
        #self.move_check.set_sensitive(False)
        self.listbox.add(self.move_check)
        self.move_param = buildlapse.robot.TimelapseMotionSettings()
   
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
        self.update_timer_actions()

    def movetoggle(self, button, name):
        if self.move_check.checked:
            self.move_param.show_all()
        else:
            self.move_param.hide()
        self.update_timer_actions()

    def update_timer_actions(self):
        actions = [buildlapse.timing._testaction()]
        if self.cam_check.checked:
            actions.append(self.cam_param.action())
        if self.move_check.checked:
            actions.append(self.move_param.action())
        self.time_param.actions = actions

def run():
    ctl = MainSettings()
    ctl.connect("delete-event", Gtk.main_quit)
    ctl.show_all()
    Gtk.main()

if __name__=="__main__":
    run()
