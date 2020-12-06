from keypaste.keypaste import (
    Command,
    Paste,
    Keypaste,
    BuildKeypaste
)
import unittest


class TestCommand(unittest.TestCase):

    def test_get_command(self):
        expected = "Test"
        command = Command("Test")
        self.assertEqual(command.get_command(), expected)


class TestKeypaste(unittest.TestCase):

    def test_if_passed_str(self):
        keypaste_test = Keypaste("TEST", "TEST")
        self.assertIsInstance(keypaste_test.get_command(), Command)
        self.assertIsInstance(keypaste_test.get_paste(), Paste)

    def test_if_passed_objects(self):
        command_obj = Command("TEST")
        keypaste_obj = Paste("TEST")
        keypaste_test = Keypaste(command_obj, keypaste_obj)
        self.assertIsInstance(keypaste_test.get_command(), Command)
        self.assertIsInstance(keypaste_test.get_paste(), Paste)


class TestBuildKeypaste(unittest.TestCase):

    def test_construct(self):
        keypaste = BuildKeypaste.constuct("TEST", "TEST")
        self.assertIsInstance(keypaste, Keypaste)

    def test_deconstruct_to_command_and_paste(self):
        test_keypaste = BuildKeypaste.constuct("TEST", "TEST")
        command, paste = BuildKeypaste.deconst_to_cmd_and_paste(test_keypaste)
        self.assertIsInstance(command, Command)
        self.assertIsInstance(paste, Paste)
        self.assertEqual(command.get_command(), "TEST")
        self.assertEqual(paste.get_paste(), "TEST")

    def test_decontruct_to_str(self):
        test_keypaste = BuildKeypaste.constuct("TEST", "TEST")
        str_command, str_paste = BuildKeypaste.deconst_to_str(test_keypaste)
        self.assertEqual(str_command, "TEST")
        self.assertEqual(str_paste, "TEST")
