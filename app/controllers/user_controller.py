import json
import os

class UserController:
    def __init__(self):
        self.logged_in_user = None
        self.users_file = "app/data/users.json"
        self.load_users()

    def load_users(self):
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as file:
                self.users = json.load(file)
        else:
            self.users = {}

    def save_users(self):
        with open(self.users_file, 'w') as file:
            json.dump(self.users, file, indent=4)

    def register_user(self, nome, email, senha):
        if email in self.users:
            return False
        self.users[email] = {
            "nome": nome,
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

    def add_review_to_user(self, email, review):
        """Adiciona uma avaliação ao perfil do usuário."""
        if email in self.users:
            self.users[email]["avaliacoes"].append(review)
            self.save_users()

            # Atualiza o usuário logado
            if self.logged_in_user and self.logged_in_user.get("email") == email:
                self.logged_in_user["avaliacoes"] = self.users[email]["avaliacoes"]

    def get_user_reviews(self, email):
        return self.users.get(email, {}).get("avaliacoes", [])
    
user_controller = UserController()