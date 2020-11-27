#!/usr/bin/env python3

from abc import ABC

class Formulate(ABC):
    def query(self):
        pass

class FormulateTable(Formulate):
    def query(self, table):
       return f"""
       CREATE TABLE {table} (
       Command varchar(255),
       Paste varchar(255)
       );  """ 

