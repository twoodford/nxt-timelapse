from gi.repository import Gtk
import multiprocessing

import buildlapse.gui

def _mkspin(maxval):
        adj = Gtk.Adjustment(0, 0, maxval, 1, 10, 0)
        spin = Gtk.SpinButton()
        spin.set_adjustment(adj)
        return spin

class TimeEntry(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self, spacing=2)
        self.hoursf = _mkspin(48)
        self.minutesf = _mkspin(59)
        self.secondsf = _mkspin(59)
        self.pack_start(self.hoursf, False, True, 0)
        self.pack_start(self.minutesf, False, True, 0)
        self.pack_start(self.secondsf, False, True, 0)

    def connect(self, event, func):
        self.hoursf.connect(event, func)
        self.minutesf.connect(event, func)
        self.secondsf.connect(event, func)

    @property
    def totalseconds(self):
        return ((self.hoursf.get_value()*60 + self.minutesf.get_value())*60 + self.secondsf.get_value())

    @totalseconds.setter
    def totalseconds(self, value):
        self.hoursf.set_value(value//60//60)
        self.minutesf.set_value((value//60)%60)
        self.secondsf.set_value((value%60)%60)

class CameraParamWindow(buildlapse.gui.ListBoxWindow):
    running = False

    def __init__(self):
        super().__init__("Camera Parameters")

        self.shutterentry = Gtk.Entry() # TODO show the list from gphoto
        self._make_row("Shutter Time", self.shutterentry)

        self.frame_entry = _mkspin(90)
        self.frame_entry.connect("value-changed", self.update_times)
        self._make_row("Length of Frame", self.frame_entry) 

        self.total_shots_entry = _mkspin(6000) # TODO adjust based on mem card space
        self.total_shots_entry.connect("value-changed", self.update_times)
        self._make_row("Total Shots", self.total_shots_entry)

        self.play_time_entry = TimeEntry()
        self.play_time_entry.connect("value-changed", self.update_numshots)
        self._make_row("Playback Time", self.play_time_entry)

        self.shooting_time_entry = TimeEntry()
        self._make_row("Shooting Time", self.shooting_time_entry)

        #self.start_button = Gtk.Button("Start Capture")
        #self.start_button.connect("clicked", self.startstop_cap)
        #self._make_row("Capture", self.start_button)
 
    def update_times(self, sender):
        framelen = self.frame_entry.get_value()
        total_shots = self.total_shots_entry.get_value()
        self.shooting_time_entry.totalseconds = framelen*total_shots
        self.play_time_entry.totalseconds = total_shots/24 # TODO specify FPS of video

    def update_numshots(self, sender):
        playtime = self.play_time_entry.totalseconds
        self.total_shots_entry.set_value(playtime*24)
        self.update_times(self) 

if __name__=="__main__":
    win = CameraParamWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
