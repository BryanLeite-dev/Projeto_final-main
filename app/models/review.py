class Review:
    def __init__(self, usuario, titulo, filme_id, comentario, nota):
        self.usuario = usuario
        self.filme_id = filme_id
        self.comentario = comentario
        self.titulo = titulo
        self.nota = nota

    def to_dict(self):
        return {
            "usuario": self.usuario,
            "filme_id": self.filme_id,
            "comentario": self.comentario,
            "titulo": self.titulo,
            "nota": self.nota
            
        }