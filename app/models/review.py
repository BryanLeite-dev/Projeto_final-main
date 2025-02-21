class Review:
    def __init__(self, usuario, filme_id, comentario, nota):
        self.usuario = usuario
        self.filme_id = filme_id
        self.comentario = comentario
        self.nota = nota

        if comentario or not nota:
             return "Erro: Comentário e nota são obrigatórios."
                
        try:
            nota = int(nota)
            if nota < 1 or nota > 10:
                return "Erro: A nota deve ser um número entre 1 e 10."
        
        except ValueError:
            return "Erro: A nota deve ser um número válido."
        
        print(f"Comentário recebido: {comentario}")
        print(f"Nota recebida: {nota}")

    def to_dict(self):
        return {
            "usuario": self.usuario,
            "filme_id": self.filme_id,
            "comentario": self.comentario,
            "nota": self.nota
        }
    