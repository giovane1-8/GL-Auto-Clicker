from time import *
from pynput.keyboard import Controller


teclado = Controller()

def keyDown(key):
    teclado.press(key)

def keyUp(key):
    teclado.release(key)

def keyPress(key):
    teclado.tap(key)

def stringPress(string,t):
    for x in string:
        teclado.tap(x)
        sleep(t)
