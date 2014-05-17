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


