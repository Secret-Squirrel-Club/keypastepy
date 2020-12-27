#!/usr/bin/env  python3

import multiprocessing
import rumps
import getpass
import os
import sys
import time
import threading
import sqlite3
import keyboard
from keypaste.keypaste import (
    BuildKeypaste
)
from keypaste.base import BaseKeyClass, KeyPasteException
from keypaste.basegui import (
    EntryGUI,
    DeleteEntryGUI,
    ViewEntriesGUI,
)
from keypaste.formulate_queries import (
    FormulateShowTables, FormulateTable, FormulateViewQuery
)
from keypaste.sql_wrapper import (
   Sqler,
)

UNICODE = "\u2328"
ADD_UNI = "\u2795"
REMOVE_UNI = "\u26D4"
VIEW_UNI = "\u1F4BE"
ERR_MESSAGE = "BAD INPUT"

class RunKeypasteGUI(BaseKeyClass):
    def __init__(self):
        super().__init__()
        self.config = {
            "app_name": "Keypaste",
            "add": f"{ADD_UNI} Add Entry",
            "delete": f"{REMOVE_UNI} Delete Entry",
            "view": "View All", 
        }
        self.app = rumps.App(self.config["app_name"])
        self.entry = rumps.MenuItem(title=self.config["add"], callback=self.run_entry)
        self.delete = rumps.MenuItem(title=self.config["delete"], callback=self.delete_entry)
        self.view = rumps.MenuItem(title=self.config["view"], callback=self.viewer)
        self.app.menu = [self.entry, self.delete, self.view]
        
    def run_entry(self, sender):
        EntryGUI(self.sql)
       
    def delete_entry(self, sender):
        DeleteEntryGUI(self.sql)

    def viewer(self, sender):
        ViewEntriesGUI(self.sql)
    
    def run(self):
        self.info("Starting app thread")
        return self.app
class RunKeypaste(BaseKeyClass):

    def __init__(self):
        super().__init__()
        self.config = {
            "app_name": "Keypaste",
            "add": f"{ADD_UNI} Add Entry",
            "delete": f"{REMOVE_UNI} Delete Entry",
            "view": "View All",
            
        }
        self.app = rumps.App(self.config["app_name"])

    def check_table_exists(self):
        show_table = FormulateShowTables().query()
        self.debug(f"Showing table with query: {show_table}")
        try:
            tables = self.sql.execute_sql(self.conn, show_table)
            if len(tables) == 0:
                self.debug("No tables, creating table Keypaste...")
                create_table = FormulateTable().query("keypaste")
                self.debug(f"Using Query to create table {create_table}")
                self.sql.execute_sql(self.conn, create_table)
            else:
                for table in tables:
                    if "keypaste" not in table:
                        self.debug("No Keypaste table, creating...")
                        create_table = FormulateTable().query("keypaste")
                        self.debug(f"Using Query to create table {create_table}")
                        self.sql.execute_sql(self.conn, create_table)
            self.debug("Table Keypaste exists")
            return True
        except sqlite3.OperationalError as sql3err:
            self.error(sql3err)
            return True

    def load_existing_keys(self):
        view_query = FormulateViewQuery().query("keypaste")
        try:
            keys = []
            data = self.sql.execute_sql(self.conn, view_query)
            if data != None:
                for key, paste in data:
                    keys.append(BuildKeypaste.construct_from_str(key, paste))
                return keys
            return []
        except sqlite3.OperationalError as sql3err:
            self.exception(sql3err)

    def keyboard_thread(self, keys):
        self.info("Starting Keyboard Thread...")
        keyboard.add_hotkey('command+x', lambda: keyboard.write('foobar'))
        keyboard.wait()
    
    def run(self):
        self.debug("Checking if user is root...")
        if getpass.os.getuid() != 0:
            self.error("User is not root, killing...")
            sys.exit(1)
        self.debug("User is root, continuing")
        if not self.check_table_exists():
            raise KeyPasteException("Could not create table")
        keys = self.load_existing_keys()
        #process = multiprocessing.Process(target=self.keyboard_thread, args=(keys))
        #process.start()
        thread = threading.Thread(target=self.keyboard_thread, args=(keys))
        return thread
if __name__ == "__main__":
    directory = f"/Users/{getpass.getuser()}/.keypaste/"
    keyboard_thread = RunKeypaste(directory).run()
    keyboard_thread.start()
    app = RunKeypasteGUI().run()
    app.run()
    # app_thread = threading.Thread(target=app.run)
    #app_thread.daemon = True
    #app_thread.start() 