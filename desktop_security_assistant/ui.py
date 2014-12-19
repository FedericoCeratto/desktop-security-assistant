
"""
.. module:: desktop_security_assistant.ui
   :synopsis: user interface

"""

# Released under AGPLv3+ license, see LICENSE

from gi.repository import Gtk
from logging import getLogger
from utils import get_resource
import re

log = getLogger(__name__)

class UI(object):
    def __init__(self):

        fn = get_resource('data', 'security-assistant.ui')
        builder = Gtk.Builder()
        builder.add_from_file(fn)
        window = builder.get_object("ui")
        window.show_all()
        window.connect("destroy", Gtk.main_quit)
        self._notebook = window.get_child()
        self._notebook.remove_page(self._notebook.get_current_page())
        self._add_intro_tab()

    @staticmethod
    def _replace_pts_links(text):
        """Replace links to the Debian PTS"""
        return re.sub(
            r'pts:([\w-]+)',
            r'<a href="https://packages.debian.org/sid/\1">\1</a>',
            text
        )

    def add_label(self, vbox, text):
        """Add label"""
        label = Gtk.Label()
        label.set_markup(self._replace_pts_links(text))
        label.set_alignment(0, 0.5)
        label.show()
        vbox.pack_start(label, False, False, 0)

    @staticmethod
    def add_url(vbox, url):
        """Add URL"""
        if url is None:
            return

        label = Gtk.LinkButton(url, label='Documentation')
        label.set_alignment(0, 0.5)
        label.show()
        vbox.pack_start(label, False, False, 0)

    @staticmethod
    def add_rating(vbox, desc, n):
        """Add rating"""
        if n is None:
            return

        hbox = Gtk.HBox(homogeneous=False, spacing=0)
        hbox.show()
        vbox.pack_start(hbox, False, False, 0)

        label = Gtk.Label("%s: " % desc)
        label.set_use_markup(True)
        label.set_alignment(0, 0.5)
        label.show()
        hbox.pack_start(label, False, False, 0)

        fn = get_resource('data', 'rating.png')
        for _ in xrange(int(n)):
            i = Gtk.Image()
            i.show()
            i.set_alignment(0, 0.5)
            i.set_from_file(fn)
            hbox.pack_start(i, expand=False, fill=False, padding=0)

    def _add_intro_tab(self):
        """Add intro tab"""

        vbox = Gtk.VBox(homogeneous=False, spacing=5)
        vbox.show()
        vbox.set_border_width(10)
        self._notebook.append_page(vbox, Gtk.Label('introduction'))
        self.add_label(vbox, """Welcome to the desktop security assistant.

This application provides you with a set of suggestions to improve the overall security of your system and protect your privacy.
Click through the tabs on the left to explore the suggestions.
Some of the tabs are displayed or not based on the current configuration of your system.

Some very rough estimates are displayed for:
risk: how serious a threat could be
difficulty: the level of skill and work required to follow the suggestion

""")

    def add_check_tab(self, check):
        """Add a tab with the output of a check"""

        vbox = Gtk.VBox(homogeneous=False, spacing=5)
        vbox.show()
        vbox.set_border_width(10)
        self._notebook.append_page(vbox, Gtk.Label(check.name))

        self.add_label(vbox, "%s" % check.desc)
        self.add_rating(vbox, "risk", check.risk)
        self.add_rating(vbox, "difficulty", check.difficulty)
        self.add_url(vbox, check.url)

        # hide button
        hidebutton = Gtk.Button("Hide")
        hidebutton.show()
        hidebutton.set_size_request(10, 20)
        hidebutton.connect('clicked', self.hide_check_tab)
        vbox.pack_start(hidebutton, False, False, 0)

    def hide_check_tab(self, button):
        page = self._notebook.get_current_page()
        self._notebook.remove_page(page)
        # This forces the widget to redraw itself.
        self._notebook.queue_draw_area(0, 0, -1, -1)

    def main(self):
        Gtk.main()
