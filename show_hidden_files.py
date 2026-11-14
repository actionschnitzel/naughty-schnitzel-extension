import gi

gi.require_version('Nautilus', '4.1')
from gi.repository import GObject, Gio, Nautilus

SCHEMA = 'org.gtk.gtk4.Settings.FileChooser'
KEY = 'show-hidden'


class ShowHiddenFilesExtension(GObject.GObject, Nautilus.MenuProvider):
    def __init__(self):
        self.settings = Gio.Settings.new(SCHEMA)

    def _toggle(self, _item):
        self.settings.set_boolean(KEY, not self.settings.get_boolean(KEY))

    def get_background_items(self, current_folder):
        if self.settings.get_boolean(KEY):
            label = 'Versteckte Dateien ausblenden'
        else:
            label = 'Versteckte Dateien anzeigen'

        item = Nautilus.MenuItem(
            name='ShowHiddenFiles::toggle',
            label=label,
            tip='Versteckte Dateien ein- oder ausschalten',
        )
        item.connect('activate', self._toggle)
        return [item]
