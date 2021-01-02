#!/usr/bin/env  python3

import rumps
import pdb
import getpass
import os
import sys
import threading
import logging
import asyncio
import multiprocessing
import sqlite3
from pynput import keyboard
from keypaste.keypaste import (
    BuildKeypaste
)
from keypaste.base import (
    BaseKeyClass,
    KeyPasteException,
    PickleWrap
)
from keypaste.basegui import (
    CloneThread,
    EntryGUI,
    DeleteEntryGUI,
    ViewEntriesGUI,
)

UNICODE = "⌨️"
ADD_UNI = "\u2795"
REMOVE_UNI = "\u26D4"
VIEW_UNI = "\u1F4BE"
UPDATE_UNI = "🔄"
ERR_MESSAGE = "BAD INPUT"


class RunKeypaste(BaseKeyClass):

    def __init__(self):
        super().__init__()
        self.config = {
            "app_name": UNICODE,
            "add": f"{ADD_UNI} Add Entry",
            "delete": f"{REMOVE_UNI} Delete Entry",
            "update": f"{UPDATE_UNI} Update Entries",
            "view": "View All",
            
        }
        self.checking_db_path()
        self.pickle = PickleWrap(self.storage_file)
        self.app = rumps.App(self.config["app_name"])
        self.entry = rumps.MenuItem(title=self.config["add"], callback=self.run_entry)
        self.delete = rumps.MenuItem(title=self.config["delete"], callback=self.delete_entry)
        self.view = rumps.MenuItem(title=self.config["view"], callback=self.viewer)
        self.update = rumps.MenuItem(title=self.config["update"], callback=self.update_menu)
        if self.get_level() == logging.DEBUG:
            rumps.debug_mode(True)

    def checking_db_path(self):
        self.debug(f"Using {self.storage_file} as storage file")
        if not os.path.isfile(self.storage_file):
            self.info(f"Creating file {self.storage_file}")
            open(self.storage_file, 'a').close()
        
    def run_entry(self, _):
        EntryGUI()

    def delete_entry(self, _):
        DeleteEntryGUI()

    def viewer(self, _):
        ViewEntriesGUI()

    def update_menu(self, _):
        self.debug("Updating app with new Entries")
        os.execl(sys.executable, sys.executable, * sys.argv) 

    def create_menu(self, keys):
        self.debug("Creating Menus")
        menu_list = [self.update, self.entry, self.delete, self.view]
        sub_list = []
        for keypaste in keys:
            self.debug(f"Added {keypaste.get_command()} to menu")
            sub_list.append(rumps.MenuItem(
                title=keypaste.get_command(),
                callback=keypaste.write
            ))
        menu_list.append(("Pastes", [item for item in sub_list]))
        self.app.menu = menu_list

    def run(self):
        self.debug("Checking if user is root...")
        if getpass.os.getuid() != 0:
            self.error("User is not root, killing...")
            sys.exit(1)
        self.debug("User is root, continuing")
        keys = self.pickle.loadall()
        self.create_menu(keys)
        self.app.run()

if __name__ == "__main__":
    run = RunKeypaste()
    run.run()
