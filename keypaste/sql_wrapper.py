#!/usr/bin/env python3

import sqlite3
class Sqler():

    def __init__(self, database: str, timeout=300):
        self.database = database
        self.timeout = timeout
    
    def create_the_db(self):
        connection = None
        try: 
            connection = sqlite3.connect(self.database)
            print(sqlite3.version)
        except Exception as err:
            print(err)
        if connection:
            self.close(connection)
    
    def close(self, conn):
        if conn:
            return conn.close()

    def connect_to_db(self):
        conn = None
        try:
            conn = sqlite3.connect(self.database)
            return conn
        except sqlite3.Error as err:
            print(err)
        finally:
            self.close(conn)

    def execute_sql(self, conn, sql_statement):
        try:
            cursor  = conn.cursor()
            cursor.execute(sql_statement)
        except sqlite3.Error as err:
            print(err)
        finally:
            self.close(conn)