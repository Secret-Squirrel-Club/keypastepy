#!/usr/bin/env python3


class Command():
    def __init__(self, command: str):
        self.__command = command 
    
    def get_command(self):
        return self.__command
    
    def set_command(self, new_command):
        self.__command = new_command
class Paste():
    def __init__(self, paste: str):
        self.__paste = paste

    def get_paste(self):
        return self.__paste
    
    def set_paste(self, new_paste):
        self.__paste = new_paste

class Keypaste():
    def __init__(self, command: Command, paste: Paste):
        self.__command = command
        self.__paste = paste

    def get_keypaste(self):
        return self.__command, self.__paste

    def set_keypaste(self, new_command: Command, new_paste: Paste):
       self.__command = new_command
       self.__paste = new_paste

    def get_command(self):
        return self.__command

    def set_command(self, command: Command):
        self.__command = command

    def get_paste(self):
        return self.__paste

    def set_paste(self, new_paste: Paste):
        self.__paste = new_paste 