class Review:
    def __init__(self, usuario, filme_id, comentario, nota):
        self.usuario = usuario
        self.filme_id = filme_id
        self.comentario = comentario
        self.nota = nota

    def to_dict(self):
        return {
            "usuario": self.usuario,
            "filme_id": self.filme_id,
            "comentario": self.comentario,
            "nota": self.nota
        }