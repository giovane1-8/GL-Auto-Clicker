import time
from pynput.keyboard import Controller as KeyboardController
from pynput.mouse import Controller as MouseController, Button


class Preset(object):

    def __init__(self, nome, events):
        self.nome = nome
        self.eventos = events
        self.keyboard = KeyboardController()
        self.mouse = MouseController()

    def to_dictionary(self):
        return dict(nome=self.nome, eventos=self.eventos)

    def run(self):
        for event in self.eventos:
            time.sleep(event["tempo_iniciar"])
            if event["tipo"] == "tecla":
                if event["acao"] == "pressionar":
                    self.keyboard.press(event["tecla"])
                elif event["acao"] == "soltar":
                    self.keyboard.release(event["tecla"])

            elif event["tipo"] == "mouse":
                if event["acao"] == "pressionar":
                    self.mouse.position = (event["x"], event["y"])
                    botao = self._get_mouse_button(event["botao"])
                    time.sleep(0.06)
                    self.mouse.press(botao)
                elif event["acao"] == "soltar":
                    self.mouse.position = (event["x"], event["y"])
                    botao = self._get_mouse_button(event["botao"])
                    time.sleep(0.06)
                    self.mouse.release(botao)

    def _get_mouse_button(self, botao):
        if botao == "esquerdo":
            return Button.left
        elif botao == "direito":
            return Button.right
        elif botao == "meio":
            return Button.middle
        else:
            return Button.left  # Botão esquerdo como padrão
