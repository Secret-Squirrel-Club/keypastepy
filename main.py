#!/usr/bin/env  python3

import rumps
import getpass
import os
import time
import keyboard
import threading
import sqlite3
from keypaste.keypaste import (
    BuildKeypaste
)
from keypaste.base import BaseKeyClass, KeyPasteException
from keypaste.basegui import (
    CloneThread,
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
ERR_MESSAGE = "BAD INPUT"


class RunKeypaste(BaseKeyClass):

    def __init__(self, path):
        super().__init__()
        self.path = path
        self.full_path = os.path.join(self.path, "keypaste.db")
        self.config = {
            "app_name": "Keypaste",
            "add": "Add Entry",
            "delete": "Delete Entry",
            "view": "View All",
            
        }
        self.checking_db_path()
        self.sql = Sqler(self.full_path)
        self.conn = self.sql.connect_to_db()
        self.app = rumps.App(self.config["app_name"])
        self.entry = rumps.MenuItem(title=self.config["add"], callback=EntryGUI(self.sql))
        self.delete = rumps.MenuItem(title=self.config["delete"], callback=DeleteEntryGUI(self.sql))
        self.view = rumps.MenuItem(title=self.config["view"], callback=ViewEntriesGUI(self.sql))
        self.app.menu = [self.entry, self.delete, self.view]

    def checking_db_path(self):
        self.debug(f"Using path: {self.path}")
        if not os.path.isdir(self.path):
            self.info("Directory doesn't exist, creating...")
            os.makedirs(self.path)
        self.debug(f"Using {self.full_path} as database")
        if not os.path.isfile(self.full_path):
            self.info(f"Creating file {self.full_path}")
            open(f'{self.full_path}', 'a').close()

    def check_table_exists(self):
        show_table = FormulateShowTables().query()
        try:
            tables = self.sql.execute_sql(self.conn, show_table)
            for table in tables:
                if "keypaste" not in table:
                    self.debug("No Keypaste table, creating...")
                    create_table = FormulateTable().query("keypaste")
                    self.sql.execute_sql(self.conn, create_table)
                else:
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
            for key, paste in data:
                keys.append(BuildKeypaste.construct_from_str(key, paste))
            return keys
        except sqlite3.OperationalError as sql3err:
            self.exception(sql3err)

    def keyboard_thread(self, keys):
        for keypaste in keys:
            keyboard.add_hotkey(f"{keypaste.get_command()}", 
                                lambda: keyboard.write(f"{keypaste.get_paste()}"))
        keyboard.wait()
    def run(self):
        if not self.check_table_exists():
            raise KeyPasteException("Could not create table")
        keys = self.load_existing_keys()
        
        threading.Thread(target=self.keyboard_thread, args=[keys]).start()
        self.app.run()

if __name__ == "__main__":
    directory = f"/Users/{getpass.getuser()}/.keypaste/"
    run = RunKeypaste(directory)
    run.run()
