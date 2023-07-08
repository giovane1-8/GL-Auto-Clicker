import json


class Configs:
    def __init__(self):
        self.keys = {}
        self.get()

    def save(self):
        with open("Model/util/configs.json", "w") as outfile:
            json.dump(self.keys, outfile)

    def get(self):
        with open("Model/util/configs.json") as file:
            self.keys = json.load(file)
