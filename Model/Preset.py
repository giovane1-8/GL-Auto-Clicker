class Preset(object):

    def __init__(self, nome, events):
        self.nome = nome
        self.eventos = events

    def to_dictionary(self):
        return dict(nome=self.nome, eventos=self.eventos)
