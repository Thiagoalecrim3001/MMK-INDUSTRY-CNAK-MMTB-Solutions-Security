import tkinter as tk
import random

class Dashboard:
    def __init__(self, parent, monitoring_service):
        self.parent = parent
        self.monitoring_service = monitoring_service
        self.frame = tk.Frame(parent)

        # Título
        tk.Label(self.frame, text="Dashboard - Mapa de Calor Simulado", font=("Arial", 16)).pack(pady=10)

        # Grid para mapa de calor (10x10)
        self.grid_frame = tk.Frame(self.frame)
        self.grid_frame.pack(pady=10)

        self.cells = []
        for i in range(10):
            row = []
            for j in range(10):
                color = self.gerar_cor_aleatoria()
                cell = tk.Label(self.grid_frame, width=3, height=1, bg=color)
                cell.grid(row=i, column=j, padx=1, pady=1)
                row.append(cell)
            self.cells.append(row)

        # Botão para atualizar mapa
        tk.Button(self.frame, text="Atualizar Mapa", command=self.atualizar_mapa).pack(pady=10)

    def gerar_cor_aleatoria(self):
        # Cores quentes para simular calor
        cores = ["#FF0000", "#FF4500", "#FFA500", "#FFFF00", "#ADFF2F", "#00FF00"]
        return random.choice(cores)

    def atualizar_mapa(self):
        for row in self.cells:
            for cell in row:
                cell.config(bg=self.gerar_cor_aleatoria())
        self.monitoring_service.adicionar_log("Mapa de calor atualizado")