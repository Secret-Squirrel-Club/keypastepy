#!/usr/bin/env python3

from sqlite3 import Connection
import unittest
from keypaste.sql_wrapper import Sqler


class TestSQLWrapper(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.inst = Sqler(":memory:")

    def test_create_the_db_true(self):
        self.assertEqual(self.inst.create_the_db(), None)

    def test_connect_to_db(self):
        conn = self.inst.connect_to_db()
        self.assertIsInstance(conn, Connection)
