#!/usr/bin/env python3


import logging
from keypaste.base import BaseKeyClass
import sqlite3
from keypaste.formulate_queries import FormulateShowTables


class Sqler(BaseKeyClass):
    
    def __init__(self, 
                database: str, 
                timeout=300):
        super().__init__()
        self.database = database
        self.timeout = timeout

    def create_the_db(self):
        connection = None
        try:
            self.debug("Attempting to connect/create database")
            connection = sqlite3.connect(self.database)
            self.info(f"Established Connection version: {sqlite3.version}")
        except Exception as err:
            self.error(err)
        if connection:
            self.debug("Closing Database Connection")
            connection.close()

    def connect_to_db(self):
        conn = None
        try:
            self.debug("Attempting to connect to database")
            conn = sqlite3.connect(self.database)
            self.debug("Returning connection object")
            return conn
        except sqlite3.Error as err:
            self.error(err)

    def execute_sql(self, conn, sql_statement):
        try:
            self.debug(f"Executing SQL statement {sql_statement}")
            cursor = conn.cursor()
            cursor.execute(sql_statement)
            return cursor.fetchall()
        except sqlite3.Error as err:
            self.exception(err)
        finally:
            self.debug("Closing Database Connection")
            conn.close()


class SQLChecker(BaseKeyClass):

    def __init__(self, database: str) -> None:
        self.database = database
        self.sqler = Sqler(self.database)

    def check_if_table_exists(self):
        query = FormulateShowTables.query()
        connection = self.sqler.connect_to_db()
        try:
            results = self.sqler.execute_sql(connection, query)
        except Exception as e:
            self.exception(e)
            return False
        return True if str(self.database) in results else False

    def check_if_database_exists(self):
        pass
