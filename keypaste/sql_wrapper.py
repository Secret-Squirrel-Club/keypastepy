#!/usr/bin/env python3


from sqlite3.dbapi2 import connect
from keypaste.base import BaseKeyClass
import sqlite3
import pdb
from keypaste.formulate_queries import FormulateShowTables


class Sqler(BaseKeyClass):

    def __init__(
        self,
        database: str,
        timeout=300
    ):
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
            self.close_conn(connection)
            
    def close_conn(self, conn):
        self.debug("Closing Connection")
        return conn.close()

    def connect_to_db(self):
        conn = None
        try:
            self.debug("Attempting to connect to database")
            conn = sqlite3.connect(self.database)
            self.debug("Returning connection object")
            return conn
        except sqlite3.Error as err:
            self.error(err)
            self.close_conn(conn)

    def execute_sql(self, conn, sql_statement):
        try:
            self.debug(f"Executing SQL statement {sql_statement}")
            cursor = conn.cursor()
            cursor.execute(sql_statement)
            if "INSERT" or "DELETE" or "CREATE" in sql_statement:
                conn.commit()
            return cursor.fetchall()
        except sqlite3.Error as err:
            self.exception(err)
            self.close_conn

class SQLChecker(BaseKeyClass):

    def __init__(self, database: str) -> None:
        self.database = database
        self.sqler = Sqler(database)