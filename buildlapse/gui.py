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

