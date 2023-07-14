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
        self._listener_keyboard = None
        self._listener_mouse = None

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
            if not self.is_running:
                break
            self.run_eventos(preset)
        for _ in range(qt_repetir):
            if not self.is_running:
                break
            self.run_eventos(preset)

    def record_preset(self, preset):
        self.is_recording = True
        preset.eventos = []

        self._listener_mouse = mouse.Listener(on_click=preset.add_mouse_press)
        self._listener_keyboard = keyboard.Listener(on_press=preset.add_key_press, on_release=preset.add_key_release)

        self._listener_mouse.start()
        self._listener_keyboard.start()

    def on_key_press(self, key, keys, preset):
        try:
            if isinstance(key.char, str):
                key = key.char
        except:
            key = key.name.upper()

        if key == keys["presets-keys"]["iniciar"]:
            if self.is_recording:
                self.is_recording = False
            if not self.is_running:
                self.run_preset(preset, keys["qt_repetir"], keys["repetir"])
            else:
                self.is_running = False

        elif key == keys["presets-keys"]["gravar"]:
            if self.is_running:
                self.is_running = False
            if not self.is_recording:
                self.record_preset(preset)
            else:
                self._listener_mouse.stop()
                self._listener_keyboard.stop()
                preset.eventos = preset.eventos[1:]
                preset.eventos = preset.eventos[:len(preset.eventos)-1]