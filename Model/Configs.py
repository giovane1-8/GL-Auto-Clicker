import json
from pynput import keyboard


class Configs:
    def __init__(self):
        self.keys = {}
        self.get()
        self.listener = None

    def save(self):
        with open("Model/util/configs.json", "w") as outfile:
            json.dump(self.keys, outfile)

    def get(self):
        with open("Model/util/configs.json") as file:
            self.keys = json.load(file)

    def start_keyboard_listener(self):

        self.listener = keyboard.Listener(on_press=self.on_key_press)
        self.listener.start()

    def stop_keyboard_listener(self):
        if self.listener is not None:
            self.listener.stop()

    def restart_keyboard_listener(self):
        self.stop_keyboard_listener()
        self.start_keyboard_listener()

    def on_key_press(self, key):
        try:
            if isinstance(key.char, str):
                key = key.char
        except:
            key = key.name.upper()

        if key == self.keys["presets-keys"]["iniciar"]:
            print("Iniciando preset")
        elif key == self.keys["presets-keys"]["gravar"]:
            print("Gravando preset")
