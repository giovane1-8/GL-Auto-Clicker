from pynput import keyboard
from APIs.presets import *

class Controller(object):
    def __init__(self, KI, KG):
        self.keyIniciar = KI
        self.KeyGravar = KG
        self.escutar = object

    def Hello(self):
        print("Hello")

    def escutarTeclado(self):
        self.escutar = keyboard.GlobalHotKeys({
            self.keyIniciar: self.Hello,
            self.KeyGravar: self.pararEscutarTeclado})
        self.escutar.setName("controllerMainHotkeys")
        self.escutar.start()

    def pararEscutarTeclado(self):
        try:
            self.escutar.locked()
        except:
            print("Não foi inicado a escuta do teclado")

    def setKeyInciar(self, value):
        self.keyInicar = value

    def setKeyGravar(self, value):
        self.KeyGravar = value


main = Main('<ctrl>+<alt>+h', '<ctrl>+<alt>+i')
main.escutarTeclado()

while True:
    pass
