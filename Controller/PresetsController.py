import json
import time
from pynput.keyboard import Key
from pynput import keyboard, mouse
from Model.Preset import Preset

class PresetsController:
    def __init__(self):
        self.is_running = False
        self.is_recording = False
        self._listener_keyboard = None
        self._listener_mouse = None
        self.teclas_especiais = {
            "ENTER": Key.enter,
            "ESC": Key.esc,
            "TAB": Key.tab,
            "BACKSPACE": Key.backspace,
            "SHIFT": Key.shift,
            "CTRL": Key.ctrl,
            "CTRL_L": Key.ctrl_l,
            "CTRL_R": Key.ctrl_r,
            "ALT": Key.alt,
            "CAPS LOCK": Key.caps_lock,
            "SPACE": Key.space,
            "LEFT": Key.left,
            "RIGHT": Key.right,
            "UP": Key.up,
            "DOWN": Key.down,
            "DELETE": Key.delete,
            "F1": Key.f1,
            "F2": Key.f2,
            "F3": Key.f3,
            "F4": Key.f4,
            "F5": Key.f5,
            "F6": Key.f6,
            "F7": Key.f7,
            "F8": Key.f8,
            "F9": Key.f9,
            "F10": Key.f10,
            "F11": Key.f11,
            "F12": Key.f12,
            "PRINT SCREEN": Key.print_screen,
            "INSERT": Key.insert,
            "HOME": Key.home,
            "END": Key.end,
            "PAGE UP": Key.page_up,
            "PAGE DOWN": Key.page_down,
            "NUM LOCK": Key.num_lock,
            "SCROLL LOCK": Key.scroll_lock,
            "PAUSE": Key.pause,
            "WIN": Key.cmd,
        }
        self.release_all_keys()

    def initPresets(self):
        with open("util/presets.json") as file:
            presets = list(json.load(file))
        presets_name = list()
        presets_instances = list()

        for x in presets:
            p = Preset(x["nome"], x["eventos"])
            presets_instances.append(p)

            presets_name.append(x["nome"])
        presets_instances = sorted(presets_instances, key=lambda y: y.nome)
        presets_name = sorted(presets_name)

        return presets_name, presets_instances

    def save(self, presets_objects):
        lista_para_arquivo = list()
        for x in presets_objects:
            lista_para_arquivo.append(x.to_dictionary())
        with open("util/presets.json", "w") as outfile:
            json.dump(lista_para_arquivo, outfile)

    def run_eventos(self, preset):
        for event in preset.eventos:
            if not self.is_running:
                break
            time.sleep(event["tempo_iniciar"])
            if event["tipo"] == "tecla":
                if event["acao"] == "pressionar":
                    try:
                        preset.keyboard.press(self.teclas_especiais[event["tecla"]])
                    except:
                        preset.keyboard.press(event["tecla"])
                elif event["acao"] == "soltar":
                    try:
                        preset.keyboard.release(self.teclas_especiais[event["tecla"]])
                    except:
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
        print("PARANDO PRESET")
        self.is_running = False

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
                print("INICIANDO PRESET")
                self.run_preset(preset, keys["qt_repetir"], keys["repetir"])
            else:
                self.is_running = False
                self.release_all_keys()

        elif key == keys["presets-keys"]["gravar"]:
            if self.is_running:
                self.is_running = False
            if not self.is_recording:
                print("GRAVANDO PRESET")
                self.record_preset(preset)
            else:
                self.is_recording = False
                self._listener_mouse.stop()
                self._listener_keyboard.stop()
                preset.eventos = preset.eventos[1:]
                preset.eventos = preset.eventos[:len(preset.eventos) - 1]
                print("PRESET SALVO")
                self.release_all_keys()

    def release_all_keys(self):
        _k = keyboard.Controller()
        for i in Key:
            _k.release(i)
        for i in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                  'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ' ', '`', '-', '=',
                  '[', ']', '\\', ';', "'", ',', '.', '/', '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_',
                  '+', '{', '}', '|', ':', '"', '<', '>', '?']:
            _k.release(i)
