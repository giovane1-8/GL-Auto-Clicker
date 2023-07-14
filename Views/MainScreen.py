from Views.Configs import *
from threading import Thread
from pynput import keyboard

from Model.Configs import Configs as ConfigsModel
from Model.Preset import Preset as PresetModel
from Controller.PresetsController import PresetsController
from Controller.ConfigsController import ConfigsController


class MainScreen:
    def __init__(self, master):
        # propriedades
        self.listener_keyboard = None

        # classes Controllers
        self.presetsController = PresetsController()
        self.configsController = ConfigsController()

        # classes Models
        self.presets, self.presetsInstances = self.presetsController.initPresets()
        self.model_configs = ConfigsModel()

        # criando janela principal
        self.main_screen = master

        # Configurações da janela principal
        # self.main_screen.geometry("410x180")
        self.main_screen.resizable(False, False)  # bloqueando redimensionamento
        self.main_screen.title("AutoClickGL")  # mudando titulo

        # variaveis tkinter
        self.button_gravar = StringVar()
        self.button_executar = StringVar()
        self.var_option_menu = StringVar()

        # carrega as janelas
        self.init_componentes()

    def on_key_press_thread(self, key):
        preset = self.presetsInstances[self.presets.index(self.var_option_menu.get())]
        thread = Thread(target=self.presetsController.on_key_press, args=(key, self.model_configs.keys, preset))
        thread.start()

    def event_on_key_press(self):
        self.listener_keyboard = keyboard.Listener(on_press=self.on_key_press_thread)
        self.listener_keyboard.start()

    def stop(self):
        self.presetsController.stop()
        if self.listener_keyboard:
            self.listener_keyboard.stop()

    def stop_keyboard_listener(self):
        if self.listener_keyboard:
            self.listener_keyboard.stop()

    def init_componentes(self):
        self.colocar_widgets()
        self.colocar_presets()
        self.event_on_key_press()
        """self.presetsController.start_keyboard_listener(self.model_configs.keys, lambda: self.presetsInstances[
            self.presets.index(self.var_option_menu.get())])
        
        self.model_configs.start_keyboard_listener(self.presetsController.run_preset,
                                                   self.presetsController.record_preset,
                                                   lambda: self.presetsInstances[
                                                       self.presets.index(self.var_option_menu.get())])
        """
        # lambda: self.presetsInstances[self.presets.index(self.var_option_menu.get())])

    def atualizar_all_widgets(self):
        for widget in self.main_screen.winfo_children():
            widget.destroy()
        self.init_componentes()
        print("Todos Widgets atualizados")

    def colocar_widgets(self):
        frm = ttk.Frame(self.main_screen, padding=0)
        frm.grid(sticky=NW, columnspan=3, pady=(0, 10))

        self.button_gravar.set(self.model_configs.keys["presets-keys"]["gravar"])
        ttk.Button(frm, textvariable=self.button_gravar,
                   command=lambda: print("TESTE")).grid(column=0, row=0)

        self.button_executar.set(self.model_configs.keys["presets-keys"]["iniciar"])
        ttk.Button(frm, textvariable=self.button_executar, command=lambda: self.presetsController.run_preset(
            self.presetsInstances[self.presets.index(self.var_option_menu.get())],
            self.model_configs.keys["qt_repetir"], self.model_configs.keys["repetir"])).grid(column=1, row=0)

        ttk.Button(frm, text="Configurações",
                   command=self.janela_configuracoes).grid(column=2, row=0, sticky=SE, padx=(130, 2))

    def colocar_presets(self):
        # cria um frame
        frm = ttk.Frame(self.main_screen, padding=0)
        frm.grid(sticky=EW, pady=(5, 0))

        # cria a variavel que carrega o preset selecionado
        var_input_text = StringVar()
        self.var_option_menu = StringVar()
        # setamos o preset selecionado como o primeiro do vetor
        try:
            var_input_text.set(self.presets[self.presets.index("New Preset")])
            self.var_option_menu.set(self.presets[self.presets.index("New Preset")])
        except:
            var_input_text.set(self.presets[0])
            self.var_option_menu.set(self.presets[0])

        # criamos o input de selecionar um preset existente
        drop = OptionMenu(frm, self.var_option_menu, *self.presets)

        # imprimimos na tela o input para selecionar um preset existente
        drop.grid(row=0, column=0, sticky=EW)

        # criamos um input para mudar o nome do preset selecionado
        ttk.Entry(frm, textvariable=var_input_text).grid(row=0, column=0, padx=(4, 40), sticky=EW, ipadx=110)

        ttk.Button(frm, text="New",
                   command=self.new_preset).grid(row=1, sticky=SW)

        # botão para salvar os presets modificados e criados
        ttk.Button(frm, text="Salvar",
                   command=lambda: self.presetsController.save(self.presetsInstances)).grid(row=1, sticky=SE)
        # adicionamos um evento quando o nome do preset for mudado
        var_input_text.trace_add(
            "write", lambda *args: self.preset_name_update(var_input_text, drop))

        self.var_option_menu.trace_add(
            "write", lambda *args: var_input_text.set(self.var_option_menu.get()))

    def preset_name_update(self, var=StringVar, drop=OptionMenu):
        var.set(var.get()[:40])
        name = var.get()
        try:
            teste = self.presets.copy()
            teste[self.presets.index(self.var_option_menu.get())] = name
            for _ in range(2):
                teste.pop(teste.index(name))

            if len(name) < 40:
                name = var.get()[:len(name) - 1]

            messagebox.showinfo(title="Já existe um preset com esse nome",
                                message="Coloque outro nome para o preset")
        except ValueError:
            name = var.get()

        finally:
            index = self.presets.index(self.var_option_menu.get())
            self.presetsInstances[index].nome = name
            self.presets[index] = name

            self.var_option_menu.set(name)
            drop['menu'].delete(0, 'end')
            # Adicione as novas opções ao menu suspenso
            for option in self.presets:
                drop['menu'].add_command(
                    label=option, command=lambda value=option: self.var_option_menu.set(value))

    def new_preset(self):
        try:
            self.presets.index("New Preset")
            messagebox.showinfo(title="Já existe um 'New Preset'",
                                message="Mude o nome de 'New Preset'")
        except ValueError:
            self.presets.append("New Preset")
            self.presetsInstances.append(PresetModel("New Preset", []))
            self.atualizar_all_widgets()

    def janela_configuracoes(self):
        self.stop_keyboard_listener()
        janela_configs = Configs(self.model_configs, self.main_screen)
        janela_configs.janela_configuracoes()

        def atualizar_botoes(c):
            self.button_executar.set(
                self.model_configs.keys["presets-keys"]["iniciar"])
            self.button_gravar.set(self.model_configs.keys["presets-keys"]["gravar"])
            janela_configs.child_window.unbind("<Destroy>")

            self.event_on_key_press()

        janela_configs.child_window.bind("<Destroy>", atualizar_botoes)
