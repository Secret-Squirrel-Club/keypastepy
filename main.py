#!/usr/bin/env  python3

import rumps
import getpass
import os
import pdb
import sys
from functools import partial
from PyQt5.QtWidgets import *
from keypaste.base import BaseKeyClass, KeyPasteException
from keypaste.sql_wrapper import (
    SQLChecker, Sqler,
)

UNICODE="\u2328"
ERR_MESSAGE="BAD INPUT"
class RunKeypaste(BaseKeyClass):

    def __init__(self, path):
        super().__init__()
        self.path = path
        self.config = {
            "app_name": "Keypaste",
            "add_mapping": "Add Mapping",
            "delete_mapping": "Delete Mapping"
        }
        self.app = rumps.App(self.config["app_name"])
    def check_table(self):
        pass

    def run(self):
        self.debug(f"Using path: {self.path}")
        if not os.path.isdir(self.path):
            self.info("Directory doesn't exist, creating...")
            os.makedirs(self.path)
        full_path = os.path.join(self.path, "keypaste.db")
        self.debug(f"Using {full_path} as database")
        if not os.path.isfile(full_path):
            self.info(f"Creating file {full_path}")
            open(f'{full_path}', 'a').close()
        sql = Sqler(full_path)
        conn = sql.connect_to_db()
        checker = SQLChecker(full_path)
        if checker.check_if_table_exists():
            sql.create_the_db()

if __name__ == "__main__":
    directory = f"/Users/{getpass.getuser()}/.keypaste/"
    run = RunKeypaste(directory)
    run.run()
