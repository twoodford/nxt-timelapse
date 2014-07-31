import threading
import time

from gi.repository import Gtk, GLib

from buildlapse.gui import ListBoxWindow, mkspin, TimeEntry, ProgressWindow

class _testaction(object):
    def setup(self):
        print("testaction setup")

    def cleanup(self):
        print("testaction cleanup")

    def __call__(self):
        print("testaction call")

class TimingParamWindow(ListBoxWindow):
    running = False
    actions = [_testaction()]

    def __init__(self, mset):
        super().__init__("Timing")

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

        self.start_button = Gtk.Button("Start Capture")
        self.start_button.connect("clicked", self.startstop_cap)
        self._make_row("Capture", self.start_button)

        self.progress = ProgressWindow()
        self.progress.set_no_show_all(True)
        self.listbox.add(self.progress) 

        self.mset = mset
 
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

    def startstop_cap(self, sender):
        if self.running:
            self.running = False
        else:
            self.start_button.set_label("Stop Capture")
            self.running = True
            self.numshots = 0
            # TODO: do setup here somewhere?
            self.progress.set_no_show_all(False)
            self.progress.show_all()
            thr = threading.Thread(target=self.runloop)
            thr.start()

            # Don't ask why, this is just what works
            # This is an unfortunate piece of ugliness I couldn't remove
            def gui_update(settings):
                settings.move_param.linear.doupdate()
                if settings.running:
                   GLib.timeout_add(settings.time_param.frame_entry.get_value() * 1000, gui_update, settings)
                return False
            gui_update(self.mset)

    def runloop(self):
        for action in self.actions:
            action.setup()
        i = 0
        while self.running:
            if self.total_shots < i:
                self.running = False
                break
            st_time = time.monotonic()
            for action in self.actions:
                action()
            self.progress.fraction = i / self.total_shots
            # Triggering the capture and moving the robot takes time (although, 
            # bizarrely, trigger_capture() doesn't necessarily wait until the 
            # shutter is closed).  Take this time into account to improve both 
            # accuracy (fixed time delays) and precision (variable latency in 
            # USB communication).
            elapsed_time = time.monotonic() - st_time
            time.sleep(self.frame_entry.get_value() - elapsed_time)
            i+=1
        for action in self.actions:
            action.cleanup()
        self.start_button.set_label("Start Capture")
        self.progress.hide()



if __name__=="__main__":
    win = CameraParamWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
