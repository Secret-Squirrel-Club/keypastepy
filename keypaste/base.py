#!/usr/bin/env python3

import logging
import getpass
import os
from keypaste.sql_wrapper import (
   Sqler,
)
formatter = logging.Formatter(
    "%(levelname)s:%(asctime)s:%(name)s: %(message)s"
)
sh = logging.StreamHandler()
sh.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(sh)
logger.setLevel(logging.DEBUG)


class KeyPasteException(Exception):
    pass


class BaseKeyClass(object):
    def __init__(self):
        self.logger = logger

    def set_level(self, log_level):
        return self.logger.setLevel(log_level)

    def debug(self, message: str):
        return self.logger.debug(message)

    def info(self, message: str):
        return self.logger.info(message)

    def error(self, message: str):
        return self.logger.error(message)

    def warn(self, message: str):
        return self.logger.warning(message)

    def critical(self, message: str):
        return self.logger.critical(message)

    def exception(self, message: str):
        return self.logger.exception(message)
    
    #def sql_client(self):
        full_path = self.checking_db_path()
        return Sqler(full_path)
    
    #def sql_conn(self, sql_client):
        return self.sql_client().connect_to_db()

    #def checking_db_path(self):
        path = f"/Users/{getpass.getuser()}/.keypaste/"
        self.debug(f"Using path: {path}")
        if not os.path.isdir(path):
            self.info("Directory doesn't exist, creating...")
            os.makedirs(path)
        full_path = os.path.join(path, "keypaste.db")
        self.debug(f"Using {full_path} as database")
        if not os.path.isfile(full_path):
            self.info(f"Creating file {full_path}")
            open(f'{self.full_path}', 'a').close()
        return full_path