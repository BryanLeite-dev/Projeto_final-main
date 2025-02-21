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
        if os.path.exists(self.reviews_file):
            with open(self.reviews_file, 'r') as file:
                self.reviews = json.load(file)
        else:
            self.reviews = []

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
        for client in websocket_controller.clients:
            client.send(f"Nova avaliação adicionada por {usuario} para o filme {filme_id}.")

    def get_reviews_by_movie(self, filme_id):
        """Retorna as avaliações de um filme específico."""
        print(f"Reviews disponíveis: {self.reviews}")
        return [review for review in self.reviews if review['filme_id'] == filme_id]
    
    def add_review_to_user(self, email, review):
        """Adiciona uma avaliação ao perfil do usuário."""
        if email in self.users:
            self.users[email]["avaliacoes"].append(review)
            self.save_users()

            # Atualiza o usuário logado
            if self.logged_in_user and self.logged_in_user.get("email") == email:
                self.logged_in_user["avaliacoes"] = self.users[email]["avaliacoes"]