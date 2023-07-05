from tkinter import *
from tkinter import ttk, messagebox
import importlib
import os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ConfigsController = importlib.import_module(
    "Controller.ConfigsController", package=parent_dir)


class Configs(object):
    def __init__(self, configs, mainScreen):
        self.configs = configs
        self.main_screen = mainScreen
        self.buttom_save = object
        self.configsController = ConfigsController.ConfigsController()

    # funcao abre uma janela filha de main_screen de configurações

    def janela_configuracoes(self):
        self.child_window = Toplevel(self.main_screen)
        self.child_window.title("Configurações")
        self.child_window.resizable(False, False)
        # self.child_window.geometry("225x210")
        # bloquear a janela principal
        self.child_window.grab_set()

        # definir o método destruir para a janela filha

        # cria um frame para configurar botoes
        frame_botoes = ttk.Frame(self.child_window, padding=0)
        frame_botoes.grid(rowspan=2, columnspan=3, pady=(0, 15))

        # Adiciona um label ao botão de setar tecla para gravar
        Label(frame_botoes, text="Tecla para inciar gravação:").grid(
            column=0, row=0, pady=(0, 20))

        # variavel que grava o valor do botao de gravar
        btn_gravar = StringVar()
        btn_gravar.set(self.configs.keys["presets-keys"]["gravar"])
        # botão de escolher tecla de gravar
        ttk.Button(frame_botoes, text="[" + btn_gravar.get() + "]", textvariable=btn_gravar,
                   command=lambda: btn_gravar.set(
                       self.verifica_key(self.configsController.get_press_key(), btn_gravar.get()))).grid(column=1,
                                                                                                          row=0,
                                                                                                          pady=(0, 20))

        # Adiciona um label ao botão de setar tecla para iniciar comandos
        Label(frame_botoes, text="Tecla para inciar repetição:").grid(
            column=0, row=1)

        # variavel que grava o valor do botao de gravar
        btn_iniciar = StringVar()
        btn_iniciar.set(self.configs.keys["presets-keys"]["iniciar"])
        # botão escolher tecla de repetir comandos
        ttk.Button(frame_botoes, text="[" + btn_iniciar.get() + "]", textvariable=btn_iniciar,
                   command=lambda: btn_iniciar.set(
                       self.verifica_key(self.configsController.get_press_key(), btn_iniciar.get()))).grid(column=1,
                                                                                                           row=1)

        # cria um frame para configuração de repetiçaõ
        frame_repeticao = ttk.Frame(self.child_window, padding=0)
        frame_repeticao.grid(sticky="w", rowspan=3, columnspan=3, pady=(0, 10))

        # Adiciona um label ao botão de setar tecla para iniciar comandos
        Label(frame_repeticao, text="Quantas vezes vai repetir:").grid(
            sticky="w")

        num_repeticao = IntVar()
        num_repeticao.set(self.configs.keys["qt_repetir"])
        input_repeticao = ttk.Entry(
            frame_repeticao, textvariable=num_repeticao)

        selected = BooleanVar()
        selected.set(self.configs.keys["repetir"])

        def mostrar_esconder_num():
            if selected.get():
                input_repeticao.grid_forget()
            else:
                input_repeticao.grid(sticky=SW, padx=(2, 0))
                num_repeticao.set(self.configs.keys["qt_repetir"])

        ttk.Radiobutton(
            frame_repeticao,
            text="até pressionar o botao novamente",
            value=True,
            variable=selected,
            command=mostrar_esconder_num
        ).grid(row=1)

        ttk.Radiobutton(
            frame_repeticao,
            text="Quantidade definida de vezes",
            value=False,
            variable=selected,
            command=mostrar_esconder_num
        ).grid(row=2, sticky=W)
        input_repeticao.grid(sticky=SW, padx=(2, 0))
        frames_janelas = ttk.Frame(self.child_window, padding=0)
        frames_janelas.grid(sticky=SW)
        self.buttom_save = ttk.Button(frames_janelas, text="Salvar", padding=0,
                                      command=lambda *x: self.on_child_window_close(btn_gravar.get(), btn_iniciar.get(),
                                                                                    num_repeticao.get(),
                                                                                    selected.get())).grid(
            column=0, row=0)
        ttk.Button(frames_janelas, text="Cancelar", padding=0,
                   command=self.child_window.destroy).grid(column=1, row=0, sticky=SE, padx=(90, 0))
        mostrar_esconder_num()

    # funcao que roda ao fechar janela de configurações
    def on_child_window_close(self, *values):
        # liberar a janela principal quando a janela filha for fechada
        self.main_screen.grab_release()
        self.configs.keys["presets-keys"]["gravar"] = values[0]
        self.configs.keys["presets-keys"]["iniciar"] = values[1]
        self.configs.keys["qt_repetir"] = values[2]
        self.configs.keys["repetir"] = values[3]
        self.configs.save()

        # destruir a janela filha
        self.child_window.destroy()

        print("configurações salvas")

    def verifica_key(self, key, key_momento):
        if key == -1:
            return key_momento
        return key
