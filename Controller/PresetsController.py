import importlib
import json
import os
import time

from pynput import keyboard, mouse

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PresetModel = importlib.import_module("Model.Preset", package=parent_dir)


class PresetsController():
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

    def run_eventos(self, preset):
        for event in preset.eventos:
            if not self.is_running:
                break
            time.sleep(event["tempo_iniciar"])
            if event["tipo"] == "tecla":
                if event["acao"] == "pressionar":
                    preset.keyboard.press(event["tecla"])
                elif event["acao"] == "soltar":
                    preset.keyboard.release(event["tecla"])
            elif event["tipo"] == "mouse":
                if event["acao"] == "pressionar":
                    preset.mouse.position = (event["x"], event["y"])
                    botao = preset._get_mouse_button(event["botao"])
                    preset.mouse.press(botao)
                elif event["acao"] == "soltar":
                    preset.mouse.position = (event["x"], event["y"])
                    botao = preset._get_mouse_button(event["botao"])
                    preset.mouse.release(botao)

    def run_preset(self, preset, qt_repetir, repetir_continuamente):
        self.is_running = True
        while repetir_continuamente:
            self.run_eventos(preset)
        for _ in range(qt_repetir):
            self.run_eventos(preset)

    def record_preset(self, preset, stop_key):
        self.stop_keyboard_listener()
        preset.eventos = []
        with mouse.Listener(on_click=preset.add_mouse_press) as mouse_listener:
            with keyboard.Listener(on_press=lambda key: preset.add_key_press(key, stop_key),
                                   on_release=preset.add_key_release) as keyboard_listener:
                keyboard_listener.join()
                mouse_listener.stop()
                mouse_listener.join()

        preset.eventos = preset.eventos[1:]

        print(preset.eventos)

    def on_key_press(self, key, keys, preset):
        try:
            if isinstance(key.char, str):
                key = key.char
        except:
            key = key.name.upper()

        if key == keys["presets-keys"]["iniciar"]:

            if not self.is_running:
                self.run_preset(preset, keys["qt_repetir"], keys["repetir"])
            else:
                self.is_running = False



        elif key == keys["presets-keys"]["gravar"]:
            print("Gravando preset")
            self.record_preset(preset, keys["presets-keys"]["gravar"])
