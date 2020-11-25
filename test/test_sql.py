#!/usr/bin/env python3

import unittest
from unittest.mock import patch
from keypaste.sql_wrapper import Sqler

class TestSQLWrapper(unittest.TestCase):

    def setUp(self):
        self.inst = Sqler("randomfile")
    
    @patch("keypaste.sql_wrapper.sqlite3")
    def test_create_the_db_true(self, mock_sql):
        mock_sql.connect.assert_called_with("randomfile")