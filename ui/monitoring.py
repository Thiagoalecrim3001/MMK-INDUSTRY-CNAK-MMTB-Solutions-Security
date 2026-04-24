import tkinter as tk

class Monitoring:
    def __init__(self, parent, monitoring_service):
        self.parent = parent
        self.monitoring_service = monitoring_service
        self.frame = tk.Frame(parent)

        # Título
        tk.Label(self.frame, text="Monitoramento - Logs", font=("Arial", 16)).pack(pady=10)

        # Text area para logs
        self.text_logs = tk.Text(self.frame, width=80, height=20)
        self.text_logs.pack(pady=10)

        # Botões
        button_frame = tk.Frame(self.frame)
        button_frame.pack(pady=5)

        tk.Button(button_frame, text="Adicionar Log Simulado", command=self.adicionar_log_simulado).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Limpar Logs", command=self.limpar_logs).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Atualizar", command=self.atualizar_logs).pack(side=tk.LEFT, padx=5)

        self.atualizar_logs()

    def adicionar_log_simulado(self):
        self.monitoring_service.adicionar_log("Evento simulado ocorrido")
        self.atualizar_logs()

    def limpar_logs(self):
        self.monitoring_service.limpar_logs()
        self.atualizar_logs()

    def atualizar_logs(self):
        self.text_logs.delete(1.0, tk.END)
        for log in self.monitoring_service.obter_logs():
            self.text_logs.insert(tk.END, log + "\n")