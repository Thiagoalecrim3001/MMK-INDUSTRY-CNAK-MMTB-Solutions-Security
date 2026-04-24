class User:
    def __init__(self, nome, nivel):
        self.nome = nome
        self.nivel = nivel

    def __str__(self):
        return f"Nome: {self.nome}, Nível: {self.nivel}"