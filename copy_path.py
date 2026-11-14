import subprocess
import gi

gi.require_version('Nautilus', '4.1')

from gi.repository import GObject, Nautilus


def notify(text):
    try:
        subprocess.run(['notify-send', 'Kopiert', text], check=False)
    except FileNotFoundError:
        print(text)


class CopyPathMenuProvider(GObject.GObject, Nautilus.MenuProvider):

    def get_file_items(self, files):
        if len(files) != 1:
            return []
        path = files[0].get_location().get_path()
        if path is None:
            return []
        item = Nautilus.MenuItem(
            name='CopyPath::file',
            label='Pfad kopieren',
            tip=path
        )
        item.connect('activate', self.copy_path, path)
        return [item]

    def get_background_items(self, current_folder):
        path = current_folder.get_location().get_path()
        if path is None:
            return []
        item = Nautilus.MenuItem(
            name='CopyPath::folder',
            label='Ordnerpfad kopieren',
            tip=path
        )
        item.connect('activate', self.copy_path, path)
        return [item]

    def copy_path(self, _item, path):
        try:
            subprocess.run(['xclip', '-selection', 'clipboard'], 
                         input=path.encode(), check=True)
            notify(path)
        except FileNotFoundError:
            try:
                subprocess.run(['xsel', '--clipboard', '--input'],
                             input=path.encode(), check=True)
                notify(path)
            except FileNotFoundError:
                notify(f'Fehler: weder xclip noch xsel gefunden. Pfad: {path}')
