
"""
.. module:: ui
   :synopsis: user interface

"""

# Released under AGPLv3+ license, see LICENSE.txt

import pygtk
pygtk.require('2.0')
import gtk

class UI(object):

    def hide_check_tab(self, button):
        page = self._notebook.get_current_page()
        self._notebook.remove_page(page)
        # Need to refresh the widget --
        # This forces the widget to redraw itself.
        self._notebook.queue_draw_area(0,0,-1,-1)

    def delete(self, widget, event=None):
        gtk.main_quit()
        return False

    def __init__(self):
        self._cnt = 0
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.connect("delete_event", self.delete)
        window.set_border_width(10)
        window.set_position(gtk.WIN_POS_CENTER)
        window.set_title("Security assistant")
        window.set_icon_from_file("cat.png")

        table = gtk.Table(3,6,False)
        window.add(table)

        # Create a new notebook, place the position of the tabs
        notebook = gtk.Notebook()
        notebook.show()
        notebook.set_tab_pos(gtk.POS_TOP)
        table.attach(notebook, 0,6,0,1)
        notebook.set_tab_pos(4)
        notebook.set_current_page(0)
        self._notebook = notebook

        # Create a bunch of buttons
        button = gtk.Button("close")
        button.show()
        button.connect("clicked", self.delete)
        button.set_size_request(10, 20)
        table.attach(button, 0,1,1,2)

        table.show()
        window.show()

    @staticmethod
    def add_label(vbox, text):
        """Add label"""
        label = gtk.Label(text)
        label.set_use_markup(True)
        label.set_alignment(0, 0.5)
        label.show()
        vbox.pack_start(label, False, False, 0)

    @staticmethod
    def add_rating(vbox, desc, n):
        """Add rating"""
        if n is None:
            return

        hbox = gtk.HBox(homogeneous=False, spacing=0)
        hbox.show()
        vbox.pack_start(hbox, False, False, 0)

        label = gtk.Label("%s: " % desc)
        label.set_use_markup(True)
        label.set_alignment(0, 0.5)
        label.show()
        hbox.pack_start(label, False, False, 0)

        for _ in xrange(int(n)):
            i = gtk.Image()
            i.show()
            i.set_alignment(0, 0.5)
            i.set_from_file('rating.png')
            hbox.pack_start(i, expand=False, fill=False, padding=0)



    def add_check_tab(self, check):
        """Add a tab with the output of a check"""

        frame = gtk.Frame(check.name)
        frame.show()
        frame.set_border_width(10)
        frame.set_size_request(150, 15)

        vbox = gtk.VBox(homogeneous=False, spacing=5)
        vbox.show()
        frame.add(vbox)

        self.add_label(vbox, "%s" % check.desc)
        self.add_label(vbox, "URL: %s" % check.url)
        self.add_rating(vbox, "risk", check.risk)
        self.add_rating(vbox, "difficulty", check.difficulty)

        # hide button
        hidebutton = gtk.Button("Hide")
        hidebutton.show()
        hidebutton.set_size_request(10, 20)
        hidebutton.connect('clicked', self.hide_check_tab)
        vbox.pack_start(hidebutton, False, False, 0)


        #self._notebook.append_page(vbox, gtk.Label(check.name))
        self._notebook.append_page(frame, gtk.Label(check.name))
        return



        frame = gtk.Frame(check.name)
        frame.set_border_width(10)
        frame.set_size_request(150, 15)
        frame.show()

        table1 = gtk.Table(rows=6, columns=1)
        table1.show()
        frame.add(table1)

        label = gtk.Label(check.desc)
        label.show()
        table1.attach(label,0,1,0,1)

        #entry=gtk.Entry()
        #table1.attach(entry,1,3,0,1)
        #entry.show()

        label = gtk.Label("URL: %s" % check.url)
        label.show()
        table1.attach(label,0,1,2,3)

        # hide button
        hidebutton = gtk.Button("Hide")
        hidebutton.set_size_request(10, 7)
        hidebutton.connect('clicked', self.hide_check_tab)
        hidebutton.show()

        table1.attach(hidebutton, 0, 1, 4, 6)

        table1.show()
        namelabel = gtk.Label(check.name)
        self._notebook.append_page(frame, namelabel)

        return



        frame = gtk.Frame(check.name)
        frame.set_border_width(10)
        frame.set_size_request(100, 75)
        frame.show()

        # desc
        desclabel = gtk.Label(check.desc)
        desclabel.show()
        #frame.add(desclabel)

        namelabel = gtk.Label(check.name)

        # hide button
        hidebutton = gtk.Button("Hide")
        hidebutton.set_size_request(10, 7)
        hidebutton.connect('clicked', self.hide_check_tab)
        hidebutton.show()

        frame.add(hidebutton)

        self._notebook.append_page(frame, namelabel)







    def main(self):
        gtk.main()


