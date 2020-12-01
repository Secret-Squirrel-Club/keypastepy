#!/usr/bin/env python3
import sqlite3
import logging
from sqlite3.dbapi2 import Error
from keypaste.command import Command
from keypaste.paste import Paste

class Keypaste():
    def __init__(self, command: Command, paste: Paste):
        self.command = command
        self.paste = paste
    