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

    def start_keyboard_listener(self, run_preset, record_preset, preset):
        self.listener = keyboard.Listener(
            on_press=lambda key: self.on_key_press(key, run_preset, record_preset, preset()))
        self.listener.start()

    def on_key_press(self, key, run_preset, record_preset, preset):
        try:
            if isinstance(key.char, str):
                key = key.char
        except:
            key = key.name.upper()

        if key == self.keys["presets-keys"]["iniciar"]:
            run_preset(preset, self.keys["qt_repetir"], self.keys["repetir"])
            print("iniciar preset")

        elif key == self.keys["presets-keys"]["gravar"]:
            record_preset(preset)
            print("Gravando preset")

    def stop_keyboard_listener(self):
        if self.listener:
            self.listener.stop()
