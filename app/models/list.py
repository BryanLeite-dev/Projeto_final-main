class Lista:
    def __init__(self, nome):
        self.nome = nome
        self.filmes = []

    def to_dict(self):
        return {
            "nome": self.nome,
            "filmes": self.filmes
        }