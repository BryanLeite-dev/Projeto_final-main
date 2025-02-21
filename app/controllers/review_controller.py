from app.models.review import Review
from app.controllers.user_controller import user_controller
from app.controllers.websocket_controller import websocket_controller
import os
import json

class ReviewController:
    def __init__(self):
        self.reviews = []
        self.reviews_file = "app/data/reviews.json"
        self.load_reviews()

    def load_reviews(self):
        """Carrega as avaliações do arquivo JSON."""
        try:
            if os.path.exists(self.reviews_file):
                with open(self.reviews_file, 'r') as file:
                    self.reviews = json.load(file)
            else:
                self.reviews = []

        except Exception as e:
            print(f"Erro ao carregar usuários: {e}")
            self.users = {}

    def save_reviews(self):
        """Salva as avaliações no arquivo JSON."""
        with open(self.reviews_file, 'w') as file:
            json.dump(self.reviews, file, indent=4)

    def is_duplicate_review(self, usuario, filme_id):
        """Verifica se o usuário já avaliou o filme."""
        return any(review['filme_id'] == filme_id and review['usuario'] == usuario for review in self.reviews)

    def add_review(self, usuario, filme_id, comentario, nota):
        """Adiciona uma avaliação e a salva no perfil do usuário."""
        review = Review(usuario, filme_id, comentario, nota)
        review_data = review.to_dict()
        self.reviews.append(review_data)

        # Salva a avaliação no perfil do usuário
        user_controller.add_review_to_user(usuario, review_data)        

        # Notifica todos os clientes conectados via WebSocket
        try:
            for client in websocket_controller.clients:
                client.send(f"Nova avaliação adicionada por {usuario} para o filme {filme_id}.")
        except Exception as e:
            print(f"Erro ao enviar mensagem via WebSocket: {e}")
            websocket_controller.remove_client(client)

    def get_reviews_by_movie(self, filme_id):
        try:
        # Verifica se o filme_id é válido
            if not isinstance(filme_id, int):
                raise ValueError("O ID do filme deve ser um número inteiro.")
            
        # Imprime os reviews disponíveis para depuração
            print(f"Reviews disponíveis: {self.reviews}")

        #Retorna as avaliações de um filme específico.
            reviews = [review for review in self.reviews if review['filme_id'] == filme_id]

            if not reviews:
                print(f"Nenhuma avaliação encontrada para o filme com ID {filme_id}.")
                return []
        
            return reviews
    
        except ValueError as ve:
            print(f"Erro de validação: {ve}")
            return []

        except TypeError as te:
            print(f"Erro de tipo: {te}. Verifique se os dados em 'self.reviews' estão corretos.")
            return []

        except Exception as e:
            print(f"Erro inesperado ao buscar avaliações do filme com ID {filme_id}: {e}")
            return []
    
    def add_review_to_user(self, email, review):
        """Adiciona uma avaliação ao perfil do usuário."""
        if email in self.users:
            self.users[email]["avaliacoes"].append(review)
            self.save_users()

            # Atualiza o usuário logado
            if self.logged_in_user and self.logged_in_user.get("email") == email:
                self.logged_in_user["avaliacoes"] = self.users[email]["avaliacoes"]

