#!/usr/bin/python3

from calendar import c
from pynput import keyboard
from time import time
from datetime import datetime

from settings import KEY_FILE_NAME

KEY_FILE_NAME = 'key.csv'
date = datetime.now()
file = open(KEY_FILE_NAME, 'w')


alphabet = ['space', 'enter', 'q', 'p', 'z', 'g', 'm', '6']
NUM = 100


count_press = NUM
count_key = 0



def on_press(key):
    pressed_key = ''
    try:
        pressed_key = key.char
    except:
        pressed_key = key.name

    global count_key
    global count_press

    if pressed_key == alphabet[count_key]:
        data = f'{pressed_key}, {time()}\n'
        file.write(data)

        count_press -= 1
        if count_press == 0:
            count_press = NUM
            count_key += 1


def on_release(key):
    if key == keyboard.Key.esc:
        return False

    if count_key == len(alphabet):
        return False

    if count_press == NUM:
        print('\n' + '*' * 5, alphabet[count_key], '*' * 5 +'\n')

    
    print(f'Press \'{alphabet[count_key]}\' {count_press}: ')




listener = keyboard.Listener(on_press=on_press,
        on_release=on_release)

print('\n' + '*' * 5, alphabet[count_key], '*' * 5 +'\n')
print(f'Press \'{alphabet[count_key]}\' {count_press}: ')
listener.run()


#with keyboard.Listener(
#        on_press=on_press,
#        on_release=on_release) as listener:
#    listener.join()
