import tkinter as tk
from tkinter import messagebox

class Settings:
    def __init__(self, parent, system):
        self.parent = parent
        self.system = system
        self.frame = tk.Frame(parent)

        # Título
        tk.Label(self.frame, text="Configurações", font=("Arial", 16)).pack(pady=10)

        # Campos de configuração
        config_frame = tk.Frame(self.frame)
        config_frame.pack(pady=10)

        tk.Label(config_frame, text="Tema:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_tema = tk.Entry(config_frame)
        self.entry_tema.grid(row=0, column=1, padx=5, pady=5)
        self.entry_tema.insert(0, self.system.obter_configuracao("tema"))

        tk.Label(config_frame, text="Idioma:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_idioma = tk.Entry(config_frame)
        self.entry_idioma.grid(row=1, column=1, padx=5, pady=5)
        self.entry_idioma.insert(0, self.system.obter_configuracao("idioma"))

        tk.Label(config_frame, text="Notificações:").grid(row=2, column=0, padx=5, pady=5)
        self.var_notif = tk.BooleanVar(value=self.system.obter_configuracao("notificacoes"))
        tk.Checkbutton(config_frame, variable=self.var_notif).grid(row=2, column=1, padx=5, pady=5)

        tk.Button(self.frame, text="Salvar Configurações", command=self.salvar_configuracoes).pack(pady=10)

    def salvar_configuracoes(self):
        tema = self.entry_tema.get().strip()
        idioma = self.entry_idioma.get().strip()
        notif = self.var_notif.get()

        self.system.atualizar_configuracao("tema", tema)
        self.system.atualizar_configuracao("idioma", idioma)
        self.system.atualizar_configuracao("notificacoes", notif)

        messagebox.showinfo("Sucesso", "Configurações salvas com sucesso!")