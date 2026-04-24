import tkinter as tk
from tkinter import ttk
from ui.dashboard import Dashboard
from ui.access_control import AccessControl
from ui.monitoring import Monitoring
from ui.settings import Settings
from services.access_service import AccessService
from services.monitoring_service import MonitoringService
from core.system import System

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Segurança MMK")
        self.root.geometry("800x600")

        # Instanciar serviços e sistema
        self.access_service = AccessService()
        self.monitoring_service = MonitoringService()
        self.system = System()

        # Frame lateral para botões
        self.sidebar = tk.Frame(root, width=200, bg="lightgray")
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        # Botões do menu
        self.btn_dashboard = tk.Button(self.sidebar, text="Dashboard", command=self.mostrar_dashboard)
        self.btn_dashboard.pack(fill=tk.X, pady=5)

        self.btn_acesso = tk.Button(self.sidebar, text="Controle de Acesso", command=self.mostrar_acesso)
        self.btn_acesso.pack(fill=tk.X, pady=5)

        self.btn_monitoramento = tk.Button(self.sidebar, text="Monitoramento", command=self.mostrar_monitoramento)
        self.btn_monitoramento.pack(fill=tk.X, pady=5)

        self.btn_config = tk.Button(self.sidebar, text="Configurações", command=self.mostrar_configuracoes)
        self.btn_config.pack(fill=tk.X, pady=5)

        # Frame principal para conteúdo
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Instanciar módulos UI
        self.dashboard = Dashboard(self.main_frame, self.monitoring_service)
        self.access_control = AccessControl(self.main_frame, self.access_service, self.monitoring_service)
        self.monitoring = Monitoring(self.main_frame, self.monitoring_service)
        self.settings = Settings(self.main_frame, self.system)

        # Mostrar dashboard por padrão
        self.mostrar_dashboard()

    def mostrar_dashboard(self):
        self.ocultar_todos()
        self.dashboard.frame.pack(fill=tk.BOTH, expand=True)

    def mostrar_acesso(self):
        self.ocultar_todos()
        self.access_control.frame.pack(fill=tk.BOTH, expand=True)

    def mostrar_monitoramento(self):
        self.ocultar_todos()
        self.monitoring.frame.pack(fill=tk.BOTH, expand=True)

    def mostrar_configuracoes(self):
        self.ocultar_todos()
        self.settings.frame.pack(fill=tk.BOTH, expand=True)

    def ocultar_todos(self):
        self.dashboard.frame.pack_forget()
        self.access_control.frame.pack_forget()
        self.monitoring.frame.pack_forget()
        self.settings.frame.pack_forget()