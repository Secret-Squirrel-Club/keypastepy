#!/usr/bin/env  python3

from keypaste.base import BaseKeyClass
import getpass
import os
from keypaste.sql_wrapper import (
    Sqler,
    SQLChecker
)

class RunKeypaste(BaseKeyClass):

    def __init__(self, path):
        super().__init__()
        self.path = path

    def run(self):
        self.debug(f"Using path: {self.path}")
        if not os.path.isdir(self.path):
            self.info(f"Directory doesn't exist, creating...")
            os.makedirs(self.path)
        full_path = os.path.join(self.path, "keypaste.db")
        self.debug(f"Using {full_path} as database")
        if not os.path.isfile(full_path):
            self.info(f"Creating file {full_path}")
            open(f'{full_path}', 'a').close()
        sql = Sqler(full_path)
        conn = sql.connect_to_db()
if __name__ == "__main__":
    directory = f"/Users/{getpass.getuser()}/.keypaste/"
    run = RunKeypaste(directory)
    run.run()

