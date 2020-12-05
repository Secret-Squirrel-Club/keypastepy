#!/usr/bin/env python3


import sqlite3
from keypaste.formulate_queries import FormulateShowTables, FormulateViewQuery, FormulateTable

class Sqler(object):

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
            connection.close()

    def connect_to_db(self):
        conn = None
        try:
            conn = sqlite3.connect(self.database)
            return conn
        except sqlite3.Error as err:
            print(err)
        finally:
            conn.close()

    def execute_sql(self, conn, sql_statement):
        try:
            cursor = conn.cursor()
            cursor.execute(sql_statement)
            return cursor.fetchone()
        except sqlite3.Error as err:
            print(err)
        finally:
            conn.close()

class SQLChecker():
    
    def __init__(self, database: str) -> None:
        super().__init__()
        self.database = database
        self.sqler = Sqler(self.database)
       
    def check_if_table_exists(self):
        query = FormulateShowTables.query()
        connection = self.sqler.connect_to_db()
        try:
            results = self.execute_sql(connection, query)
        except Exception as e:
            return False
        return True if str(self.database) in results else False