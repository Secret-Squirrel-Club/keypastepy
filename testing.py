import asyncio
import pyautogui
import threading
import pdb
from keypaste.keypaste import Keypaste
from pynput import keyboard

controller = keyboard.Controller()
key1 = Keypaste("<cmd>+z", "command z")
key2 = Keypaste("<cmd>+x", "command x")
def create_hot_key_list():
    return [key1, key2]

def create_hot_key_dict():
    main_dict = {}
    for key in create_hot_key_list():
        main_dict[key.get_command()] = key.write
    return main_dict

def keyboard_listener():
    listener = keyboard.GlobalHotKeys(
        create_hot_key_dict()
    )
    return listener

thread = keyboard_listener().start()
thread.stop()
import time 
while True:
    print("time")
    time.sleep(5)

"""
#def stuff():
    pyautogui.typewrite("helo")

def keyboard_worker():
        keyboard.add_hotkey('command+x', stuff())
     

def gui_worker():
    while True:
        print("GUI WORKER")

#threading.Thread(target=keyboard_worker).start()
#async def master():
#loop = asyncio.get_event_loop()
#loop.create_task(keyboard_worker())
#loop.create_task(gui_worker())
#loop.run_forever()
"""