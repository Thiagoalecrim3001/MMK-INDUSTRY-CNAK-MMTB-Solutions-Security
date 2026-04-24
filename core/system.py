class System:
    def __init__(self):
        self.configuracoes = {
            "tema": "claro",
            "idioma": "portugues",
            "notificacoes": True
        }

    def atualizar_configuracao(self, chave, valor):
        self.configuracoes[chave] = valor

    def obter_configuracao(self, chave):
        return self.configuracoes.get(chave)