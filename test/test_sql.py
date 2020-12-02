#!/usr/bin/env python3

import unittest
from keypaste.sql_wrapper import Sqler


class TestSQLWrapper(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.inst = Sqler(":memory:")

    def test_create_the_db_true(self):
        instance = Sqler(":memory:")
        self.assertEqual(instance.create_the_db(), None)
