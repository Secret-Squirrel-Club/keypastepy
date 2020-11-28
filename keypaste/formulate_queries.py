#!/usr/bin/env python3

from abc import ABC

class Formulate(ABC):
    @staticmethod
    def query():
        pass

class FormulateTable(Formulate):
    @staticmethod
    def query(table):
       return f"""
       CREATE TABLE {table} (
       Command varchar(255),
       Paste varchar(255)
       );  """ 

class FormulateInsertData(Formulate):
    @staticmethod
    def query(table, command, paste):
        return f"""
        INSERT INTO {table} (Command, Paste)
        VALUES({command}, {paste})
        """
class FormulateDeleteEntry(Formulate):
    @staticmethod
    def query(table, command):
        return f"""
        DELETE FROM  WHERE Command = {command}
        """
class FormualteViewQuery(Formulate):
    @staticmethod
    def query(table):
        return f"""
        SELECT * FROM {table}
        """

class FormulateDropTable(Formulate):
    @staticmethod
    def query(table):
        return f"""
        SELECT DROP {table}
        """