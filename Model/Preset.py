import time
from pynput import keyboard, mouse


class Preset(object):

    def __init__(self, nome, events):
        self.nome = nome
        self.eventos = events
        self.keyboard = keyboard.Controller()
        self.mouse = mouse.Controller()
        self.start_time = None

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
                    self.mouse.press(botao)
                elif event["acao"] == "soltar":
                    self.mouse.position = (event["x"], event["y"])
                    botao = self._get_mouse_button(event["botao"])
                    self.mouse.release(botao)

    def add_key_press(self, key, stop_key):
        try:
            if isinstance(key.char, str):
                key = key.char
        except:
            key = key.name.upper()
        print(key)
        if key == stop_key:
            return False
        event = {"tipo": "tecla", "acao": "pressionar", "tecla": key, "tempo_iniciar": self.get_elapsed_time()}
        self.eventos.append(event)

    def add_key_release(self, key):
        try:
            if isinstance(key.char, str):
                key = key.char
        except:
            key = key.name.upper()

        event = {"tipo": "tecla", "acao": "soltar", "tecla": key, "tempo_iniciar": self.get_elapsed_time()}
        self.eventos.append(event)

    def add_mouse_press(self, x, y, button, pressed):
        event = {"tipo": "mouse", "acao": "pressionar" if pressed else "soltar", "x": x, "y": y, "botao": button.name,
                 "tempo_iniciar": self.get_elapsed_time()}
        print(event)
        self.eventos.append(event)



    def get_elapsed_time(self):
        if self.start_time is None:
            self.start_time = time.time()
            return 0
        _t = self.start_time
        self.start_time = time.time()
        return round(time.time() - _t, 2)

    def _get_mouse_button(self, botao):
        if botao == "left":
            return mouse.Button.left
        elif botao == "right":
            return mouse.Button.right
        elif botao == "middle":
            return mouse.Button.middle
        else:
            return mouse.Button.left  # Botão esquerdo como padrão
