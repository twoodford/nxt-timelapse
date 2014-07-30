from gi.repository import Gtk
import multiprocessing

from buildlapse.gui import ListBoxWindow, mkspin, TimeEntry

class CameraParamWindow(ListBoxWindow):
    running = False

    def __init__(self):
        super().__init__("Camera Parameters")

        self.shutterentry = Gtk.Entry() # TODO show the list from gphoto
        self._make_row("Shutter Time", self.shutterentry)

        self.frame_entry = mkspin(360)
        self.frame_entry.connect("value-changed", self.update_times)
        self._make_row("Length of Frame", self.frame_entry) 

        self.total_shots_entry = mkspin(6000) # TODO adjust based on mem card space
        self.total_shots_entry.connect("value-changed", self.update_times)
        self._make_row("Total Shots", self.total_shots_entry)

        self.play_time_entry = TimeEntry()
        self.play_time_entry.connect("value-changed", self.update_numshots)
        self._make_row("Playback Time", self.play_time_entry)

        self.shooting_time_entry = TimeEntry()
        self._make_row("Shooting Time", self.shooting_time_entry)

 
    def update_times(self, sender):
        framelen = self.frame_entry.get_value()
        total_shots = self.total_shots_entry.get_value()
        self.shooting_time_entry.totalseconds = framelen*total_shots
        self.play_time_entry.totalseconds = total_shots/24 # TODO specify FPS of video

    def update_numshots(self, sender):
        playtime = self.play_time_entry.totalseconds
        self.total_shots_entry.set_value(playtime*24)
        self.update_times(self)

    @property
    def total_shots(self):
        return self.total_shots_entry.get_value()

if __name__=="__main__":
    win = CameraParamWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
