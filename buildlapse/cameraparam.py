from gi.repository import Gtk

class CameraParamWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Camera Parameters")
        self.timesettings = Gtk.Table()
        self.timesettings.set_row_spacings(5)
        self.timesettings.set_col_spacings(5)
        self.add(self.timesettings)

        self.shutterentry = Gtk.Entry()
        shutterlabel = Gtk.Label()
        shutterlabel.set_text("Shutter Speed")
        self.timesettings.attach(self.shutterentry, 1, 2, 0, 1)
        self.timesettings.attach(shutterlabel, 0, 1, 0, 1)

        self.frame_entry = Gtk.Entry()
        frame_label = Gtk.Label()
        frame_label.set_text("Length of a Frame")
        self.timesettings.attach(self.frame_entry, 1, 2, 1, 2)
        self.timesettings.attach(frame_label, 0, 1, 1, 2)

        self.total_shots_entry = Gtk.Entry()
        total_shots_label = Gtk.Label()
        total_shots_label.set_text("Total Number of Shots")
        self.timesettings.attach(self.total_shots_entry, 1, 2, 2, 3)
        self.timesettings.attach(total_shots_label, 0, 1, 2, 3)

        self.play_time_entry = Gtk.Entry()
        play_time_label = Gtk.Label()
        play_time_label.set_text("Playback Time")
        self.timesettings.attach(self.play_time_entry, 3, 4, 0, 1)
        self.timesettings.attach(play_time_label, 2, 3, 0, 1)

        self.shooting_time_entry = Gtk.Entry()
        shooting_time_label = Gtk.Label()
        shooting_time_label.set_text("Time to shoot sequence")
        self.timesettings.attach(self.shooting_time_entry, 3, 4, 1, 2)
        self.timesettings.attach(shooting_time_label, 2, 3, 1, 2)


if __name__=="__main__":
    win = CameraParamWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
