#!/usr/bin/env python3
from typing import Tuple
import keyboard
import pyperclip


class Command(object):
    def __init__(self, command: str) -> None:
        self.__command = command

    def get_command(self) -> str:
        return self.__command

    def set_command(self, new_command) -> None:
        self.__command = new_command


class Paste(object):
    def __init__(self, paste: str):
        self.__paste = paste

    def get_paste(self) -> str:
        return self.__paste

    def set_paste(self, new_paste):
        self.__paste = new_paste


class Keypaste(object):
    def __init__(self, command: str, paste: str):
        self.__command = command
        self.__paste = paste

    def get_keypaste(self) -> Tuple[str, str]:
        return self.__command, self.__paste

    def set_keypaste(self, new_command: str, new_paste: str):
        self.__command = new_command
        self.__paste = new_paste

    def get_command(self) -> str:
        return self.__command

    def set_command(self, command: str):
        self.__command = command

    def get_paste(self) -> str:
        return self.__paste

    def set_paste(self, new_paste: str):
        self.__paste = new_paste

    def write(self, _):
        keyboard.write(self.get_paste())

    def copy_to_clipboard(self, _):
        pyperclip.copy(self.get_paste())


class BuildKeypaste(object):

    @staticmethod
    def construct_from_obj(command: str, paste: str) -> Keypaste:
        command_obj = Command(command)
        paste_obj = Paste(paste)
        return Keypaste(command_obj, paste_obj)

    @staticmethod
    def construct_from_str(command: str, paste: str) -> Keypaste:
        if not isinstance(command, str):
            command = str(command)
        if not isinstance(paste, str):
            paste = str(paste)
        return Keypaste(command, paste)

    @staticmethod
    def deconst_to_cmd_and_paste(keypaste: Keypaste) -> Tuple[Command, Paste]:
        command_obj = keypaste.get_command()
        paste_obj = keypaste.get_paste()
        return command_obj, paste_obj

    @staticmethod
    def deconst_to_str(keypaste: Keypaste) -> Tuple[str, str]:
        return keypaste.get_command(), keypaste.get_paste()
