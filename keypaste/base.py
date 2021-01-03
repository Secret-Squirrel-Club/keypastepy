#!/usr/bin/env python3


import logging
import pickle
import os
import json
from pathlib import Path
from keypaste.keypaste import Keypaste

formatter = logging.Formatter(
    "%(levelname)s:%(asctime)s:%(name)s: %(message)s"
)
sh = logging.StreamHandler()
sh.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(sh)
logger.setLevel(logging.DEBUG)
USER_HOME = str(Path.home())

class KeyPasteException(Exception):
    pass


class BaseKeyClass(object):

    def __init__(self):
        self.logger = logger
        self.config_file = f"{USER_HOME}/.keypaste/keypaste.json"
        self.config_json = self.load_config_json()
        self.storage_file = self.config_json.get("stored_file")
        self.pickle = PickleWrap(self.storage_file)

    def set_level(self, log_level):
        return self.logger.setLevel(log_level)

    def get_level(self):
        return self.logger.level

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

    def create_json_file(self):
        config_dir = os.path.dirname(self.config_file)
        if not os.path.isdir(config_dir):
            os.mkdir(config_dir)
        json_dict = {"stored_file": f"{USER_HOME}/.keypaste/keypaste.dat"}
        with open(self.config_file, "w") as config_file:
            json.dump(json_dict, config_file)

    def load_config_json(self):
        if not os.path.isfile(self.config_file):
            self.create_json_file()
        with open(self.config_file) as config:
            return json.load(config)


class PickleWrap(object):

    def __init__(self, full_path_file):
        super().__init__()
        self.logger = logger
        self.full_path_file = full_path_file

    def write_to_file(self, obj: Keypaste):
        self.logger.info("Writing to file")
        with open(self.full_path_file, 'wb') as file_stream:
            pickle.dump(obj, file_stream)

    def loadall(self):
        keypaste_data = []
        try:
            with open(self.full_path_file, 'rb') as file_stream:
                while True:
                    keypaste_data.extend(pickle.load(file_stream))
        except EOFError:
            return keypaste_data

    def append_and_reload(self, obj: Keypaste):
        """
        Input: Keypaste
        Output: reload a list of keypaste

        Grabs Current list, matches
        if not, it will append new object to file
        if yes raise exception
        """
        original = self.loadall()
        for keypaste in original:
            if obj.get_command() == keypaste.get_command():
                self.logger.debug("Object already in pickle")
                return original
        self.logger.debug(f"Adding {obj.get_command()} to file")
        original.append(obj)
        self.write_to_file(original)
        return self.loadall()

    def delete_and_reload(self, command):
        original = self.loadall()
        for keypaste in original:
            if keypaste.get_command() == command:
                self.logger.debug(f"Found {keypaste.get_command()}, deleting")
                original.remove(keypaste)
        self.write_to_file(original)
        return self.loadall()

    def view_all(self):
        original = self.loadall()
        key_list = []
        for keypaste in original:
            key_list.append((keypaste.get_command(), keypaste.get_paste()))
        return key_list

    def delete_all_entries(self):
        self.logger.info("Clearing out all Entries")
        self.write_to_file([])
        return self.loadall()

    def get_last_keypaste(self):
        all_keys = self.loadall()
        last_key = all_keys[-1]
        return last_key

    def checking_db_path(self):
        self.logger.debug(f"Using {self.full_path_file} as storage file")
        if not os.path.isfile(self.full_path_file):
            self.logger.info(f"Creating file {self.full_path_file}")
            open(self.full_path_file, 'a').close()
