from Views.Configs import *

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ConfigsModel = importlib.import_module("Model.Configs", package=parent_dir)
ConfigsController = importlib.import_module(
    "Controller.ConfigsController", package=parent_dir)
PresetsController = importlib.import_module(
    "Controller.PresetsController", package=parent_dir)
PresetModel = importlib.import_module("Model.Preset", package=parent_dir)


class MainScreen:
    def __init__(self, master):

        self.presetsController = PresetsController.PresetsController()

        self.presets, self.presetsInstances = self.presetsController.initPresets()

        # criando janela principal
        self.main_screen = master

        # Instanciando Model de configurações
        self.configs = ConfigsModel.Configs()

        # Instanciando Controller de configurações
        self.configsController = ConfigsController.ConfigsController()

        # definindo tamanho da janela
        self.main_screen.geometry("350x180")
        # bloqueando redimensionamento
        self.main_screen.resizable(False, False)
        # mudando titulo
        self.main_screen.title("AutoClickGL")
        self.init_componentes()

    def init_componentes(self):
        self.colocar_widgets()
        self.colocar_presets()

    def atualizar_all_widgets(self):
        for widget in self.main_screen.winfo_children():
            widget.destroy()
        self.colocar_widgets()
        self.colocar_presets()
        print("Todos Widgets atualizados")

    def colocar_widgets(self):
        frm = ttk.Frame(self.main_screen, padding=0)
        frm.grid(sticky=EW, columnspan=3, pady=(0, 10))

        self.button_gravar = StringVar()
        self.button_gravar.set(self.configs.keys["presets-keys"]["gravar"])
        ttk.Button(frm, textvariable=self.button_gravar,
                   command=lambda: print("TESTE")).grid(column=0, row=0)

        self.button_executar = StringVar()
        self.button_executar.set(self.configs.keys["presets-keys"]["iniciar"])
        ttk.Button(frm, textvariable=self.button_executar, command=lambda: print(
            "Executando comandos")).grid(column=1, row=0)

        ttk.Button(frm, text="Configurações",
                   command=lambda *x: self.janela_configuracoes()).grid(column=2, row=0, sticky=E, padx=(110, 0))

    def colocar_presets(self):
        # cria um frame
        frm = ttk.Frame(self.main_screen, padding=0)
        frm.grid(sticky=EW, columnspan=4, rowspan=2)

        # cria a variavel que carrega o preset selecionado
        var_input_text = StringVar()
        var_option_menu = StringVar()
        # setamos o preset selecionado como o primeiro do vetor
        try:
            var_input_text.set(self.presets[self.presets.index("New Preset")])
            var_option_menu.set(self.presets[self.presets.index("New Preset")])
        except:
            var_input_text.set(self.presets[0])
            var_option_menu.set(self.presets[0])

        # criamos o input de selecionar um preset existente
        drop = OptionMenu(frm, var_option_menu, *self.presets)

        # imprimimos na tela o input para selecionar um preset existente
        drop.grid(row=0, column=0, sticky=EW)

        ttk.Button(frm, text="New", padding=0,
                   command=self.new_preset).grid(sticky=W)

        # criamos um input para mudar o nome do preset selecionado
        ttk.Entry(frm, textvariable=var_input_text).grid(
            row=0, column=0, padx=(4, 30), sticky=EW, ipadx=90)
        # botão para salvar os presets modificados e criados
        ttk.Button(frm, text="Salvar", padding=0,
            command=lambda: self.presetsController.save(self.presetsInstances)).grid(sticky=E, row=1)
        # adicionamos um evento quando o nome do preset for mudado
        var_input_text.trace_add(
            "write", lambda *args: self.preset_name_update(var_input_text, var_option_menu, drop))

        var_option_menu.trace_add(
            "write", lambda *args: var_input_text.set(var_option_menu.get()))

    def preset_name_update(self, var=StringVar, var_list=StringVar, drop=OptionMenu):
        var.set(var.get()[:40])
        name = var.get()
        try:
            teste = self.presets.copy()
            teste[self.presets.index(var_list.get())] = name
            for _ in range(2):
                teste.pop(teste.index(name))

            if (len(name) < 40):
                name = var.get()[:len(name) - 1]

            messagebox.showinfo(title="Já existe um preset com esse nome",
                                message="Coloque outro nome para o preset")
        except ValueError:
            name = var.get()

        finally:
            index = self.presets.index(var_list.get())
            self.presetsInstances[index].nome = name
            self.presets[index] = name

            var_list.set(name)
            drop['menu'].delete(0, 'end')
            # Adicione as novas opções ao menu suspenso
            for option in self.presets:
                drop['menu'].add_command(
                    label=option, command=lambda value=option: var_list.set(value))

    def new_preset(self):
        try:
            self.presets.index("New Preset")
            messagebox.showinfo(title="Já existe um 'New Preset'",
                                message="Mude o nome de 'New Preset'")
        except ValueError:
            self.presets.append("New Preset")
            self.presetsInstances.append(PresetModel.Preset("New Preset", []))
            self.atualizar_all_widgets()

    def janela_configuracoes(self):
        janela_configs = Configs(self.configs, self.main_screen)
        janela_configs.janela_configuracoes()

        def atualizar_botoes(c):
            self.button_executar.set(
                self.configs.keys["presets-keys"]["iniciar"])
            self.button_gravar.set(self.configs.keys["presets-keys"]["gravar"])
            janela_configs.child_window.unbind("<Destroy>")

        janela_configs.child_window.bind("<Destroy>", atualizar_botoes)
