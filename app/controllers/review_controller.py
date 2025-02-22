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
        try:
            if os.path.exists(self.reviews_file):
                with open(self.reviews_file, 'r') as file:
                    data = file.read()
                    print(f"Dados lidos do arquivo reviews.json: {data}")  # Log para depuração
                    self.reviews = json.loads(data) if data else []
            else:
                print("Arquivo reviews.json não encontrado. Inicializando lista vazia.")
                self.reviews = []
        except Exception as e:
            print(f"Erro ao carregar avaliações: {e}")
            self.reviews = []

    def save_users(self):
        try:
            with open(self.users_file, 'w') as file:
                json.dump(self.users, file, indent=4)
                print(f"Dados salvos em users.json: {self.users}")  # Log para depuração
        except Exception as e:
            print(f"Erro ao salvar usuários: {e}")

    def is_duplicate_review(self, usuario, filme_id):
        """Verifica se o usuário já avaliou o filme."""
        return any(review['filme_id'] == filme_id and review['usuario'] == usuario for review in self.reviews)

    def add_review(self, usuario, filme_id, comentario, nota):
        """Adiciona uma avaliação e notifica via WebSocket."""
        review = Review(usuario, filme_id, comentario, nota)
        review_data = review.to_dict()

        # Verifica se o usuário já avaliou o filme
        if any(r['filme_id'] == filme_id and r['usuario'] == usuario for r in self.reviews):
            raise Exception("Você já avaliou este filme.")

        # Adiciona a avaliação à lista global
        self.reviews.append(review_data)

        # Salva as avaliações no arquivo JSON
        self.save_reviews()

        # Salva a avaliação no perfil do usuário
        user_controller.add_review_to_user(usuario, review_data)

        # Notifica todos os clientes conectados via WebSocket
        websocket_controller.broadcast({
            "type": "new_review",
            "data": review_data
        })

    def get_reviews_by_movie(self, filme_id):
        try:
            if not isinstance(filme_id, int):
                raise ValueError("O ID do filme deve ser um número inteiro.")

            print(f"Reviews disponíveis: {self.reviews}")  # Log para depuração
            reviews = [review for review in self.reviews if review['filme_id'] == filme_id]

            if not reviews:
                print(f"Nenhuma avaliação encontrada para o filme com ID {filme_id}.")
                return []

            return reviews
        except Exception as e:
            print(f"Erro ao buscar avaliações do filme com ID {filme_id}: {e}")
            return []

    
    def save_reviews(self):
        try:
            with open(self.reviews_file, 'w') as file:
                json.dump(self.reviews, file, indent=4)
                print(f"Dados salvos em reviews.json: {self.reviews}")  # Log para depuração
        except Exception as e:
            print(f"Erro ao salvar avaliações: {e}")

