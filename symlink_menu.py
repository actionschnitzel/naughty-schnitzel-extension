# Nautilus-Extension: Symlink-Quelle merken / Symlink hier erstellen
import os
import subprocess

import gi

gi.require_version('Nautilus', '4.1')

from gi.repository import GObject, Nautilus

source = None  # zuletzt gemerkter Pfad, lebt nur solange Nautilus läuft


def notify(text):
    try:
        subprocess.run(['notify-send', 'Symlink', text], check=False)
    except FileNotFoundError:
        print(text)


class SymlinkMenuProvider(GObject.GObject, Nautilus.MenuProvider):

    def get_file_items(self, files):
        if len(files) != 1:
            return []
        path = files[0].get_location().get_path()
        if path is None:
            return []
        item = Nautilus.MenuItem(name='SymlinkMerken', label='Symlink-Quelle merken', tip=path)
        item.connect('activate', self.merken, path)
        return [item]

    def get_background_items(self, current_folder):
        if source is None:
            return []
        item = Nautilus.MenuItem(name='SymlinkHier', label='Symlink hier erstellen', tip=source)
        item.connect('activate', self.erstellen, current_folder)
        return [item]

    def merken(self, _item, path):
        global source
        source = path
        notify(f'Gemerkt: {path}')

    def erstellen(self, _item, folder):
        dest_dir = folder.get_location().get_path()
        if dest_dir is None:
            notify('Zielordner ist kein lokaler Pfad')
            return
        target = os.path.join(dest_dir, os.path.basename(source))
        if os.path.lexists(target):
            notify(f'Existiert bereits: {target}')
            return
        try:
            os.symlink(source, target)
        except OSError as err:
            notify(f'Fehler: {err}')
            return
        notify(f'Symlink erstellt: {target}')
