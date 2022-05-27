#!/usr/bin/python3

from pynput import keyboard
from time import time
from datetime import datetime

from settings import KEY_FILE_NAME

KEY_FILE_NAME = 'key.csv'
date = datetime.now()
file = open(KEY_FILE_NAME, 'w')



def on_press(key):
    try:
        print(f'{key.char} pressed')
        data = f'{key.char}, {time()}\n'
    except:
        print(f'{key.name} pressed')
        data = f'{key.name}, {time()}\n'
    file.write(data)


def on_release(key):
    if key == keyboard.Key.esc:
        return False

listener = keyboard.Listener(on_press=on_press,
        on_release=on_release)
listener.run()


#with keyboard.Listener(
#        on_press=on_press,
#        on_release=on_release) as listener:
#    listener.join()
