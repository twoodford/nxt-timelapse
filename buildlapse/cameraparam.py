from gi.repository import Gtk
import multiprocessing

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

def photocap(framelen, numshots):
    import time
    import buildlapse.gphoto2
    camera = buildlapse.gphoto2.GPTether()
    camera.connect_camera()
    for i in range(numshots):
        print(i)
        camera.trigger_capture()
        time.sleep(framelen)

class CameraParamWindow(Gtk.Window):
    running = False

    def __init__(self):
        Gtk.Window.__init__(self, title="Camera Parameters")
        self.set_border_width(10)
        
        self.timesettings = Gtk.ListBox()
        self.timesettings.set_selection_mode(Gtk.SelectionMode.NONE)
        self.add(self.timesettings)

        self.shutterentry = Gtk.Entry() # TODO show the list from gphoto
        self._make_row(self.timesettings, "Shutter Time", self.shutterentry)

        self.frame_entry = _mkspin(90)
        self.frame_entry.connect("value-changed", self.update_times)
        self._make_row(self.timesettings, "Length of Frame", self.frame_entry) 

        self.total_shots_entry = _mkspin(6000) # TODO adjust based on mem card space
        self.total_shots_entry.connect("value-changed", self.update_times)
        self._make_row(self.timesettings, "Total Shots", self.total_shots_entry)

        self.play_time_entry = TimeEntry()
        self.play_time_entry.connect("value-changed", self.update_numshots)
        self._make_row(self.timesettings, "Playback Time", self.play_time_entry)

        self.shooting_time_entry = TimeEntry()
        self._make_row(self.timesettings, "Shooting Time", self.shooting_time_entry)

        self.start_button = Gtk.Button("Start Capture")
        self.start_button.connect("clicked", self.startstop_cap)
        self._make_row(self.timesettings, "Capture", self.start_button)


    def _make_row(self, lbox, labeltxt, entry):
        label = Gtk.Label(labeltxt, xalign=0)
        hbox = Gtk.Box(spacing=6)
        row = Gtk.ListBoxRow()
        hbox.pack_start(label, True, True, 0)
        hbox.pack_start(entry, False, True, 0)
        row.add(hbox)
        self.timesettings.add(row)

    def update_times(self, sender):
        framelen = self.frame_entry.get_value()
        total_shots = self.total_shots_entry.get_value()
        self.shooting_time_entry.totalseconds = framelen*total_shots
        self.play_time_entry.totalseconds = total_shots/24 # TODO specify FPS of video

    def update_numshots(self, sender):
        playtime = self.play_time_entry.totalseconds
        self.total_shots_entry.set_value(playtime*24)
        self.update_times(self)

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
            self.subproc = multiprocessing.Process(target=photocap, args=(framelen, numshots))
            self.subproc.start()

if __name__=="__main__":
    win = CameraParamWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
