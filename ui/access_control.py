import tkinter as tk
from tkinter import messagebox

class AccessControl:
    def __init__(self, parent, access_service, monitoring_service):
        self.parent = parent
        self.access_service = access_service
        self.monitoring_service = monitoring_service
        self.frame = tk.Frame(parent)

        # Título
        tk.Label(self.frame, text="Controle de Acesso", font=("Arial", 16)).pack(pady=10)

        # Formulário para adicionar usuário
        form_frame = tk.Frame(self.frame)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Nome:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_nome = tk.Entry(form_frame)
        self.entry_nome.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Nível:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_nivel = tk.Entry(form_frame)
        self.entry_nivel.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(form_frame, text="Adicionar Usuário", command=self.adicionar_usuario).grid(row=2, column=0, columnspan=2, pady=10)

        # Lista de usuários
        tk.Label(self.frame, text="Usuários Cadastrados:").pack(pady=5)
        self.listbox = tk.Listbox(self.frame, width=50, height=10)
        self.listbox.pack(pady=5)

        tk.Button(self.frame, text="Atualizar Lista", command=self.atualizar_lista).pack(pady=5)

        self.atualizar_lista()

    def adicionar_usuario(self):
        nome = self.entry_nome.get().strip()
        nivel = self.entry_nivel.get().strip()
        try:
            self.access_service.adicionar_usuario(nome, nivel)
            self.monitoring_service.adicionar_log(f"Usuário '{nome}' adicionado com nível '{nivel}'")
            self.entry_nome.delete(0, tk.END)
            self.entry_nivel.delete(0, tk.END)
            self.atualizar_lista()
            messagebox.showinfo("Sucesso", "Usuário adicionado com sucesso!")
        except ValueError as e:
            messagebox.showerror("Erro", str(e))

    def atualizar_lista(self):
        self.listbox.delete(0, tk.END)
        for usuario in self.access_service.listar_usuarios():
            self.listbox.insert(tk.END, str(usuario))