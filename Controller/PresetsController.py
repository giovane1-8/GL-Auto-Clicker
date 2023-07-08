import importlib
import json
import os
import time
from pynput import keyboard, mouse

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PresetModel = importlib.import_module("Model.Preset", package=parent_dir)


class PresetsController(object):
    def __init__(self):
        self.is_running = False
        self.is_recording = False
        self.listener = None

    def initPresets(self):
        with open("Model/util/presets.json") as file:
            presets = list(json.load(file))
        presets_name = list()
        presets_instances = list()

        for x in presets:
            p = PresetModel.Preset(x["nome"], x["eventos"])
            presets_instances.append(p)

            presets_name.append(x["nome"])
        presets_instances = sorted(presets_instances, key=lambda y: y.nome)
        presets_name = sorted(presets_name)

        return presets_name, presets_instances

    def save(self, presets_objects):
        lista_para_arquivo = list()
        for x in presets_objects:
            lista_para_arquivo.append(x.to_dictionary())
        with open("Model/util/presets.json", "w") as outfile:
            json.dump(lista_para_arquivo, outfile)

    def run_preset(self, preset, qt_repetir, repetir_continuamente):
        self.is_running = not self.is_running
        if repetir_continuamente:
            while self.is_running:
                preset.run()
        else:
            for _ in range(qt_repetir):
                preset.run()
    def record_preset(self, preset, stop_key):
        self.stop_keyboard_listener()
        preset.eventos = []
        with mouse.Listener(on_click=preset.add_mouse_press) as mouse_listener:
            with keyboard.Listener(on_press=lambda key: preset.add_key_press(key, stop_key), on_release=preset.add_key_release) as keyboard_listener:
                keyboard_listener.join()
                mouse_listener.stop()
                mouse_listener.join()

        preset.eventos = preset.eventos[1:]

        print(preset.eventos)

    def start_keyboard_listener(self, keys, preset):
        self.listener = keyboard.Listener(on_press=lambda key: self.on_key_press(key, keys, preset()))
        self.listener.start()

    def on_key_press(self, key, keys, preset):
        try:
            if isinstance(key.char, str):
                key = key.char
        except:
            key = key.name.upper()

        if key == keys["presets-keys"]["iniciar"]:
            self.run_preset(preset, keys["qt_repetir"], keys["repetir"])
            print("Iniciando preset")

        elif key == keys["presets-keys"]["gravar"]:
            print("Gravando preset")
            self.record_preset(preset, keys["presets-keys"]["gravar"])

    def stop_keyboard_listener(self):
        if self.listener:
            self.listener.stop()
