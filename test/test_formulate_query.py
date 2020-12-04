import unittest
from keypaste.formulate_queries import (
    FormulateViewQuery,
    FormulateInsertData,
    FormulateDropTable,
    FormulateDeleteEntry,
    FormulateTable
)

class TestFormulate(unittest.TestCase):

    def test_formulatetable_ok(self):
        exp_result = "CREATE TABLE stuff (Command varchar(255), Paste varchar(255));" 
        self.assertEqual(FormulateTable.query("stuff"), exp_result)
    
    def test_formulateinsertdata_ok(self):
        exp_result = "INSERT INTO stuff (Command, Paste) VALUES (test, test)" 
        self.assertEqual(FormulateInsertData.query("stuff", "test", "test"), exp_result)
    
    def test_FormulateDelete_ok(self):
        exp_result = "DELETE FROM main_table WHERE Command = abc"
        self.assertEqual(FormulateDeleteEntry.query("main_table", "abc"), exp_result)

    def test_FormulateView_ok(self):
        exp_result = "SELECT * FROM main_table"
        self.assertEqual(FormulateViewQuery.query("main_table"), exp_result)
    
    def test_FormulateDropTable_ok(self):
        exp_result = "DROP TABLE main_table"
        self.assertEqual(FormulateDropTable.query("main_table"), exp_result)