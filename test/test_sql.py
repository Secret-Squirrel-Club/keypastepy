#!/usr/bin/env python3

import sqlite3
from sqlite3.dbapi2 import Connection
import unittest
from unittest import mock
from unittest.mock import Mock
from keypaste.sql_wrapper import Sqler
import pdb


class TestSQLWrapper(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.inst = Sqler(":memory:")

    def test_create_the_db_true(self):
        instance = Sqler(":memory:")
        self.assertEqual(instance.create_the_db(), None) 

    def test_create_the_db_fail(self):
        instance = Sqler(":memory:")