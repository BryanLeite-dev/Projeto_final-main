from app.models.user_account import UserAccount
import json
import uuid

class DataRecord():
    def __init__(self):
        self.__user_accounts = []
        self.__authenticated_users = {}
        self.read()

    def read(self):
        try:
            with open("app/controllers/db/users.json", "r") as arquivo_json:
                user_data = json.load(arquivo_json)
                self.__user_accounts = [UserAccount(**data) for data in user_data]
        except FileNotFoundError:
            self.__user_accounts.append(UserAccount('Guest', '010101', '101010'))

    def save_to_json(self):
        with open("app/controllers/db/users.json", "w") as arquivo_json:
            user_data = [{"username": user.username, "password": user.password} for user in self.__user_accounts]
            
            json.dump(user_data, arquivo_json, indent=4)


    def book(self, username, password):
        new_user = UserAccount(username, password)
        self.__user_accounts.append(new_user)
        self.save_to_json()

    def getCurrentUser(self, session_id):
        if session_id in self.__authenticated_users:
            return self.__authenticated_users[session_id]
        else:
            return None

    def getUserName(self, session_id):
        if session_id in self.__authenticated_users:
            return self.__authenticated_users[session_id].username
        else:
            return None

    def getUserSessionId(self, username):
        for session_id in self.__authenticated_users:
            if username == self.__authenticated_users[session_id].username:
                return session_id
        return None

    def checkUser(self, username, password):
        for user in self.__user_accounts:
            if user.username == username and user.password == password:
                session_id = str(uuid.uuid4())
                self.__authenticated_users[session_id] = user
                return session_id
        return None

    def logout(self, session_id):
        if session_id in self.__authenticated_users:
            del self.__authenticated_users[session_id]

    def check_if_user_exists(self, username):
        for user in self.__user_accounts:
            if user.username == username:
                return True
        return False

    def create_new_user(self, username, password):
        if not self.check_if_user_exists(username):
            new_user = UserAccount(username, password)
            self.__user_accounts.append(new_user)
            self.save_to_json()
            return True
        return False
