from core.user import User

class AccessService:
    def __init__(self):
        self.usuarios = []

    def adicionar_usuario(self, nome, nivel):
        if not nome or not nivel:
            raise ValueError("Nome e nível são obrigatórios")
        usuario = User(nome, nivel)
        self.usuarios.append(usuario)

    def listar_usuarios(self):
        return self.usuarios

    def remover_usuario(self, nome):
        self.usuarios = [u for u in self.usuarios if u.nome != nome]