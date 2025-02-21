from models.list import Lista

class ListController:
    def __init__(self):
        self.lists = []

    def create_list(self, nome):
        lista = Lista(nome)
        self.lists.append(lista.to_dict())

    def add_movie_to_list(self, list_name, movie):
        for lista in self.lists:
            if lista['nome'] == list_name:
                lista['filmes'].append(movie)