#!/usr/bin/env python3

import sqlite3
class Sqler():

    def __init__(self, filename: str, timeout=300):
        self.filename = filename
        self.timeout = timeout
    
    def create_the_db(self):
        connection = None
        try: 
            connection = sqlite3.connect(self.filename)
            print(sqlite3.version)
        except Exception as err:
            print(err)
        if connection:
            connection.close()
    
    