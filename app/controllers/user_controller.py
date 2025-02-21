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
        try:

            if email not in self.users:
                raise ValueError(f"Usuário com email '{email}' não encontrado.")            

            if "avaliacoes" not in self.users[email]:
                    self.users[email]["avaliacoes"] = []  # Garante que a lista de avaliações exista

            self.users[email]["avaliacoes"].append(review)

            self.save_users()

            # Atualiza o usuário logado
            if self.logged_in_user and self.logged_in_user.get("email") == email:
                self.logged_in_user["avaliacoes"] = self.users[email]["avaliacoes"]

        except ValueError as ve:
            print(f"Erro de validação: {ve}")
            # Aqui você pode optar por lançar novamente o erro ou retornar False para indicar falha
            return False

        except IOError as ioe:
            print(f"Erro ao salvar os dados do usuário: {ioe}")
            # Tratar erro de I/O (ex.: falha ao escrever no arquivo JSON)
            return False

        except Exception as e:
            print(f"Erro inesperado ao adicionar avaliação ao usuário: {e}")
            # Captura qualquer outro erro inesperado
            return False

        return True

    def get_user_reviews(self, email):
        return self.users.get(email, {}).get("avaliacoes", [])
    
user_controller = UserController()