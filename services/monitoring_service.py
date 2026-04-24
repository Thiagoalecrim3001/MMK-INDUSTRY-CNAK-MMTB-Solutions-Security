import datetime

class MonitoringService:
    def __init__(self):
        self.logs = []

    def adicionar_log(self, mensagem):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log = f"[{timestamp}] {mensagem}"
        self.logs.append(log)

    def obter_logs(self):
        return self.logs

    def limpar_logs(self):
        self.logs = []