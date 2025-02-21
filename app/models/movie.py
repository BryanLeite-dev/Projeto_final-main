class Movie:
    def __init__(self, titulo, diretor, genero):
        self.titulo = titulo
        self.diretor = diretor
        self.genero = genero

    def to_dict(self):
        return {
            "titulo": self.titulo,
            "diretor": self.diretor,
            "genero": self.genero
        }