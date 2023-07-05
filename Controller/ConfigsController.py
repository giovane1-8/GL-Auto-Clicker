from pynput.keyboard import Listener


class ConfigsController():
    def get_press_key(self):
        key = ["F3"]

        def press_ke(x, key):
            key[0] = x

        with Listener(on_press=lambda x: press_ke(x, key), on_release=lambda x: listener.stop()) as listener:
            listener.join()
        try:
            if isinstance(key[0].char, str):
                return key[0].char
            else:
                return -1
        except:
            return key[0].name.upper()


    def start_keyboard_listener(self, callback_preset_name_return):

        self.listener = keyboard.Listener(on_press=lambda key: self.on_key_press(key, callback_preset_name_return()))
        self.listener.start()

    def stop_keyboard_listener(self):
        if self.listener:
            self.listener.stop()

    def on_key_press(self, key, preset):
        try:
            if isinstance(key.char, str):
                key = key.char
        except:
            key = key.name.upper()

        if key == self.keys["presets-keys"]["iniciar"]:
            if(self.is_execultando):
                preset.stop()

            print("iniciar preset")
        elif key == self.keys["presets-keys"]["gravar"]:
            print("Gravando preset")
