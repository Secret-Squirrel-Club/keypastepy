#!/usr/bin/env  python3

import rumps
import logging
from keypaste.base import (
    BaseKeyClass,
    PickleWrap
)
from keypaste.basegui import (
    EntryGUI,
    DeleteEntryGUI,
    ViewEntriesGUI,
)

UNICODE = "⌨️"
ADD_UNI = "\u2795"
REMOVE_UNI = "\u26D4"
VIEW_UNI = "👓"
ERR_MESSAGE = "BAD INPUT"


class RunKeypaste(BaseKeyClass):

    def __init__(self):
        super().__init__()
        self.config = {
            "app_name": UNICODE,
            "add": f"{ADD_UNI} Add Entry",
            "delete": f"{REMOVE_UNI} Delete Entry",
            "view": f"{VIEW_UNI} View All",
        }
        self.pickle = PickleWrap(self.storage_file)
        self.pickle.checking_db_path()
        self.app = rumps.App(self.config["app_name"])
        self.entry = rumps.MenuItem(
            title=self.config["add"],
            callback=self.run_entry)
        self.delete = rumps.MenuItem(
            title=self.config["delete"],
            callback=self.delete_entry)
        self.view = rumps.MenuItem(
            title=self.config["view"],
            callback=self.viewer)
        if self.get_level() == logging.DEBUG:
            rumps.debug_mode(True)

    def run_entry(self, _):
        EntryGUI(self.app.menu)

    def delete_entry(self, _):
        DeleteEntryGUI(self.app.menu)

    def viewer(self, _):
        ViewEntriesGUI()

    def create_menu(self, keys):
        self.debug("Creating Menus")
        menu_list = [self.entry, self.delete, self.view]
        sub_list = []
        for keypaste in keys:
            self.debug(f"Added {keypaste.get_command()} to menu")
            if not self.copy_clipboard:
                self.debug("Config says to write it to screen")
                sub_list.append(rumps.MenuItem(
                    title=keypaste.get_command(),
                    callback=keypaste.write
                ))
            else:
                self.debug("Config says to copy to buffer")
                sub_list.append(rumps.MenuItem(
                    title=keypaste.get_command(),
                    callback=keypaste.copy_to_clipboard
                ))
        menu_list.append(("Pastes", [item for item in sub_list]))
        self.app.menu = menu_list

    def run(self):
        self.debug("Loading Keys")
        keys = self.pickle.loadall()
        self.create_menu(keys)
        rumps.notification(title="Keypaste",
                           subtitle="App Running",
                           message="",
                           icon="keyboard.icns")
        self.app.run()


if __name__ == "__main__":
    run = RunKeypaste()
    run.run()
