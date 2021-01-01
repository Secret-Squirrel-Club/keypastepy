#!/usr/bin/env  python3

import rumps
import pdb
import getpass
import os
import sys
import threading
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

UNICODE = "\u2328"
ADD_UNI = "\u2795"
REMOVE_UNI = "\u26D4"
VIEW_UNI = "\u1F4BE"
ERR_MESSAGE = "BAD INPUT"


class RunKeypaste(BaseKeyClass):

    def __init__(self):
        super().__init__()
        self.config = {
            "app_name": "Keypaste",
            "add": f"{ADD_UNI} Add Entry",
            "delete": f"{REMOVE_UNI} Delete Entry",
            "view": "View All",
            
        }
        self.checking_db_path()
        self.pickle = PickleWrap(self.storage_file)
        self.app = rumps.App(self.config["app_name"])
        self.entry = rumps.MenuItem(title=self.config["add"], callback=self.run_entry)
        self.delete = rumps.MenuItem(title=self.config["delete"], callback=self.delete_entry)
        self.view = rumps.MenuItem(title=self.config["view"], callback=self.viewer)
        self.app.menu = [self.entry, self.delete, self.view]

    def checking_db_path(self):
        self.debug(f"Using {self.storage_file} as storage file")
        if not os.path.isfile(self.storage_file):
            self.info(f"Creating file {self.storage_file}")
            open(self.storage_file, 'a').close()

    def create_hot_key_dict(self, keys):
        main_dict = {}
        for key in keys:
            main_dict[key.get_command()] = key.write
        return main_dict

    def keyboard_listener(self, key_dict):
        self.info("Creating Keyboard Listener")
        Listener =  keyboard.GlobalHotKeys(
            key_dict
        )
        return Listener
        
    def run_entry(self, sender):
        EntryGUI()

    def delete_entry(self, sender):
        DeleteEntryGUI()

    def viewer(self, sender):
        ViewEntriesGUI()
        
    def gui_worker(self):
        self.info("Starting app thread")
        self.app.run()
        
    def run(self):
        self.debug("Checking if user is root...")
        if getpass.os.getuid() != 0:
            self.error("User is not root, killing...")
            sys.exit(1)
        self.debug("User is root, continuing")
        keys = self.pickle.loadall()
        keys_dict = self.create_hot_key_dict(keys)
        listener = self.keyboard_listener(keys_dict)
        self.info("Starting Keyboard thread")
        if listener.is_alive():
            listener.stop()
        listener.start()
        import time
        #listener.join()
        self.gui_worker()
        #while True:
        #    print("stuff") 
        #    time.sleep(1) 
if __name__ == "__main__":
    run = RunKeypaste()
    run.run()
