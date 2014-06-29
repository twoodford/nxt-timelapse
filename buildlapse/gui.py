# gui.py
# Generic GUI crap
from gi.repository import Gtk

class CheckEntry(Gtk.Box):
    def __init__(self, labeltxt, togglef = None):
        Gtk.Box.__init__(self, spacing=2)
        self.label = Gtk.Label(labeltxt, valign=0)
        self.check = Gtk.CheckButton()
        self.pack_start(self.check, True, True, 0)
        self.pack_start(self.label, False, True, 0)
        def _toggle(x, y):
            if togglef != None:
                togglef(x, y)
        self.check.connect("toggled", _toggle, labeltxt)

    @property
    def checked(self):
        return self.check.get_active()

    @checked.setter
    def checked(self, value):
        self.check.set_active(value)

class ListBoxWindow(Gtk.Window):
    def __init__(self, title):
        Gtk.Window.__init__(self, title=title)
        self.set_border_width(10)
        self.listbox = Gtk.ListBox()
        self.listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.add(self.listbox)

    def _make_row(self, labeltxt, entry):
        label = Gtk.Label(labeltxt, xalign=0)
        hbox = Gtk.Box(spacing=6)
        row = Gtk.ListBoxRow()
        hbox.pack_start(label, True, True, 0)
        hbox.pack_start(entry, False, True, 0)
        row.add(hbox)
        self.listbox.add(row)

def mkspin(maxval):
    return mkspin2(0, maxval)
    
def mkspin2(minval, maxval):
    adj = Gtk.Adjustment(0, minval, maxval, 1, 10, 0)
    spin = Gtk.SpinButton()
    spin.set_adjustment(adj)
    return spin

class TimeEntry(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self, spacing=2)
        self.hoursf = mkspin(48)
        self.minutesf = mkspin(59)
        self.secondsf = mkspin(59)
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


