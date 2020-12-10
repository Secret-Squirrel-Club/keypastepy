#!/usr/bin/env python3

from abc import ABC


class Formulate(ABC):
    @staticmethod
    def query():
        pass


class FormulateTable(Formulate):
    @staticmethod
    def query(table: str):
        return f"CREATE TABLE {table} \
            (Command varchar(255), Paste varchar(255));"


class FormulateInsertData(Formulate):
    @staticmethod
    def query(table: str, command: str, p: str):
        return f"INSERT INTO {table} (Command, Paste) VALUES ({command}, {p})"


class FormulateDeleteEntry(Formulate):
    @staticmethod
    def query(table, command: str):
        return f"DELETE FROM {table} WHERE Command = {command}"


class FormulateViewQuery(Formulate):
    @staticmethod
    def query(table: str):
        return f"SELECT * FROM {table}"


class FormulateDropTable(Formulate):
    @staticmethod
    def query(table: str):
        return f"DROP TABLE {table}"


class FormulateShowTables(Formulate):
    @staticmethod
    def query():
        return "SHOW TABLES"
