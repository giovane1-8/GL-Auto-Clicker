from pynput.keyboard import Listener


class ConfigsController():
    def get_press_key(self):
        
        with Listener(on_press=lambda x: x) as lister:
            lister.join()

    def save_config(self):
        pass