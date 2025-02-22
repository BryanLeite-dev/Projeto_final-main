import json
import os

class UserController:
    def __init__(self):
        self.logged_in_user = None
        self.users_file = "app/data/users.json"
        self.load_users()

    def load_users(self):
        try:
            if os.path.exists(self.users_file):
                with open(self.users_file, 'r') as file:
                    data = file.read()
                    print(f"Dados lidos do arquivo users.json: {data}")  # Log para depuração
                    self.users = json.loads(data) if data else {}
            else:
                print("Arquivo users.json não encontrado. Inicializando dicionário vazio.")
                self.users = {}
        except Exception as e:
            print(f"Erro ao carregar usuários: {e}")
            self.users = {}

    def save_users(self):
        with open(self.users_file, 'w') as file:
            json.dump(self.users, file, indent=4)

    def register_user(self, nome, email, senha):
        if email in self.users:
            return False
        self.users[email] = {
            "nome": nome,
            "email": email,
            "senha": senha,
            "avaliacoes": []
        }
        self.save_users()
        return True

    def login_user(self, email, senha):
        user = self.users.get(email)
        if user and user["senha"] == senha:
            self.logged_in_user = user
            return True
        return False

    def logout_user(self):
        self.logged_in_user = None

    def is_authenticated(self):
        return self.logged_in_user is not None

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

    def get_user_reviews(self, email):
        """Retorna as avaliações do usuário com o nome do filme."""
        user_data = self.users.get(email, {})
        reviews = user_data.get("avaliacoes", [])

        # Busca o nome do filme para cada avaliação
        enriched_reviews = []
        for review in reviews:
            movie_id = review.get("filme_id")
            if movie_id:
                try:
                    movie_details = self.movie_controller.get_movie_details(int(movie_id))
                    review["movie_title"] = movie_details.get("title", "Título Desconhecido")
                except Exception as e:
                    print(f"Erro ao buscar detalhes do filme com ID {movie_id}: {e}")
                    review["movie_title"] = "Título Desconhecido"
            else:
                review["movie_title"] = "Título Desconhecido"

            enriched_reviews.append(review)

        return enriched_reviews
    
    def add_review_to_user(self, email, review):
        """Adiciona uma avaliação ao perfil do usuário."""
        if email in self.users:
            self.users[email]["avaliacoes"].append(review)
            self.save_users()

            # Atualiza o usuário logado
            if self.logged_in_user and self.logged_in_user.get("email") == email:
                self.logged_in_user["avaliacoes"] = self.users[email]["avaliacoes"]
    
user_controller = UserController()