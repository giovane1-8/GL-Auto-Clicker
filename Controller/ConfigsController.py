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
            
    def save_config(self):
        pass
