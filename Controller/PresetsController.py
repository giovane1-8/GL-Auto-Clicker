import importlib
import json
import os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PresetModel = importlib.import_module("Model.Preset", package=parent_dir)


class PresetsController(object):
    def __init__(self):
        self.is_runing = False
        self.is_recording = False

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
        self.is_runing = not self.is_runing
        if repetir_continuamente:
            while self.is_runing:
                preset.run()
        else:
            for _ in range(qt_repetir):
                preset.run()

    def record_preset(self, preset):
        pass
