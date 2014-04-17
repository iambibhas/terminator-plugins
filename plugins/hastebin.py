import gtk
import urllib
import terminatorlib.plugin as plugin
import re
import requests
import json

# Written by Bibhas Debnath http://bibhas.in

# AVAILABLE must contain a list of all the classes that you want exposed
AVAILABLE = ['HastebinPlugin']

_spaces = re.compile(" +")

class HastebinPlugin(plugin.Plugin):
    capabilities = ['terminal_menu']

    def do_upload(self, searchMenu):
        """Launch Hastebin with the url"""
        if not self.searchstring:
            return
        base_uri = "http://hastebin.com"
        resp = requests.post(base_uri + "/documents", data=self.searchstring)
        rdict = json.loads(resp.text)
        gtk.show_uri(None, base_uri + "/" + rdict['key'], gtk.gdk.CURRENT_TIME)

    def callback(self, menuitems, menu, terminal):
        """Add our menu item to the menu"""
        self.terminal = terminal
        item = gtk.ImageMenuItem(gtk.STOCK_FIND)
        item.connect('activate', self.do_upload)
        if terminal.vte.get_has_selection():
            clip = gtk.clipboard_get(gtk.gdk.SELECTION_PRIMARY)
            self.searchstring = clip.wait_for_text().strip()
        else:
            self.searchstring = None
        if self.searchstring:
            if len(self.searchstring) > 40:
                displaystring = self.searchstring[:37] + "..."
            else:
                displaystring = self.searchstring
            item.set_label("Upload to Hastebin")
            item.set_sensitive(True)
        else:
            item.set_label("Upload to Hastebin")
            item.set_sensitive(False)
        # Avoid turning any underscores in selection into menu accelerators
        item.set_use_underline(False)
        menuitems.append(item)
