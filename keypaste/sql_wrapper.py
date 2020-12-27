#!/usr/bin/env python3


import sqlite3
import logging

formatter = logging.Formatter(
    "%(levelname)s:%(asctime)s:%(name)s: %(message)s"
)
sh = logging.StreamHandler()
sh.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(sh)
logger.setLevel(logging.DEBUG)

class Sqler(object):

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
            logger.debug("Attempting to connect/create database")
            connection = sqlite3.connect(self.database)
            logger.info(f"Established Connection version: {sqlite3.version}")
        except Exception as err:
            logger.error(err)
            self.close_conn(connection)

    def close_conn(self, conn):
        logger.debug("Closing Connection")
        return conn.close()

    def connect_to_db(self):
        conn = None
        try:
            logger.debug("Attempting to connect to database")
            conn = sqlite3.connect(self.database)
            logger.debug("Returning connection object")
            return conn
        except sqlite3.Error as err:
            logger.error(err)
            self.close_conn(conn)

    def execute_sql(self, conn, sql_statement):
        try:
            logger.debug(f"Executing SQL statement {sql_statement}")
            cursor = conn.cursor()
            cursor.execute(sql_statement)
            if "INSERT" or "DELETE" or "CREATE" in sql_statement:
                conn.commit()
            return cursor.fetchall()
        except sqlite3.Error as err:
            logger.exception(err)
            self.close_conn()
