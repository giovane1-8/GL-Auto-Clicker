from tkinter import *
from tkinter import ttk, messagebox
import importlib, os
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ConfigsModel = importlib.import_module("Model.Configs", package=parent_dir)
ConfigsController = importlib.import_module("Controller.ConfigsController", package=parent_dir)

class MainScreen():
    def __init__(self, master: Tk):
        # propriedades
        self.presets = ["Padrao", "teste1", "teste2"]
        self.presets = sorted(self.presets)
        # criando janela principal
        self.main_screen = master
        #
        self.configs = ConfigsModel.Configs()
        self.configsController = ConfigsController.ConfigsController()
        self.configsController.get_press_key()
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

        ttk.Button(frm, text="Gravar ["+self.configs.keys["presets-keys"]["gravar"]+"]", command=lambda: print(
            "gravando comandos")).grid(column=0, row=0)

        ttk.Button(frm, text="Executar ["+self.configs.keys["presets-keys"]["iniciar"]+"]", command=lambda: print("Executando comandos")).grid(
            column=1, row=0)

        ttk.Button(frm, text="Configurações",
                   command=self.janela_configuracoes).grid(column=2, row=0, sticky=E, padx=(110, 0))

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
                name = var.get()[:len(name)-1]

            messagebox.showinfo(title="Já existe um preset com esse nome",
                                message="Coloque outro nome para o preset")
        except ValueError:
            name = var.get()

        finally:
            self.presets[self.presets.index(var_list.get())] = name
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
            self.atualizar_all_widgets()

    # funcao abre uma janela filha de main_screen de configurações
    def janela_configuracoes(self):
        self.child_window = Toplevel(self.main_screen)
        self.child_window.title("Configurações")
        self.child_window.resizable(False, False)
        self.child_window.geometry("225x210")
        # bloquear a janela principal
        self.child_window.grab_set()

        # definir o método destruir para a janela filha
        self.child_window.protocol(
            "WM_DELETE_WINDOW", lambda *x: self.on_child_window_close(btn_gravar.get(), btn_iniciar.get(), num_repeticao.get(), selected.get()))

        # cria um frame para configurar botoes
        frame_botoes = ttk.Frame(self.child_window, padding=0)
        frame_botoes.grid(rowspan=2, columnspan=3, pady=(0, 15))

        # Adiciona um label ao botão de setar tecla para gravar
        Label(frame_botoes, text="Tecla para inciar gravação:").grid(
            column=0, row=0, pady=(0, 20))

        # botão de escolher tecla de gravar
        ttk.Button(frame_botoes, text="["+self.configs.keys["presets-keys"]["gravar"]+"]", command=lambda: print(
            "aperte uma tecla...")).grid(column=1, row=0, pady=(0, 20))
        # variavel que grava o valor do botao de gravar
        btn_gravar = StringVar()
        btn_gravar.set(self.configs.keys["presets-keys"]["gravar"])

        # Adiciona um label ao botão de setar tecla para iniciar comandos
        Label(frame_botoes, text="Tecla para inciar repetição:").grid(
            column=0, row=1)

        # botão escolher tecla de repetir comandos
        ttk.Button(frame_botoes, text="["+self.configs.keys["presets-keys"]["iniciar"]+"]", command=lambda: print(
            "aperte uma tecla...")).grid(column=1, row=1)
        # variavel que grava o valor do botao de gravar
        btn_iniciar = StringVar()
        btn_iniciar.set(self.configs.keys["presets-keys"]["iniciar"])

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
        frames_janelas.grid(sticky=SE, columnspan=3)
        ttk.Button(frames_janelas, text="Salvar", padding=0, command=lambda *x: self.on_child_window_close(btn_gravar.get(), btn_iniciar.get(), num_repeticao.get(), selected.get())).grid(
            column=0, row=0)
        ttk.Button(frames_janelas, text="Cancelar", padding=0,
                   command=self.child_window.destroy).grid(column=1, row=0)
        mostrar_esconder_num()

    # funcao que roda ao fechar janela de configurações
    def on_child_window_close(self, *values):
        # liberar a janela principal quando a janela filha for fechada
        self.main_screen.grab_release()
        self.configs.keys["presets-keys"]["gravar"] = values[0]
        self.configs.keys["presets-keys"]["iniciar"] = values[1]
        self.configs.keys["qt_repetir"] = values[2]
        self.configs.keys["repetir"] = values[3]
        # destruir a janela filha
        self.child_window.destroy()
        self.child_window = None
        
        self.configs.save()
        print("configurações salvas")
