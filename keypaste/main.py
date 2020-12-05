#!/usr/bin/env  python3
from sqlite3.dbapi2 import connect
import pynupt
from keypaste.formulate_queries import (
    FormulateTable,
    FormulateInsertData,
    FormulateViewQuery,
    FormulateDeleteEntry,
    FormulateDropTable
)
from keypaste.keypaste import Keypaste
from keypaste.command import Command
from keypaste.paste import Paste
from keypaste.sql_wrapper import Sqler

def run():
    pass 

if __name__ == "__main__":
    sql = Sqler("keypaste")
    
        
