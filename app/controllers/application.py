# from app.controllers.datarecord import DataRecord
# from bottle import template, redirect, request


# class Application:
#     def __init__(self):
#         self.pages = {
#             'pagina': self.pagina,
#             'portal': self.portal,
#             'comentarios': self.comentarios
#         }

#         self.__model = DataRecord()
#         self.__current_username = None

#     def render(self, page, parameter=None, filme=None):
#         content = self.pages.get(page, self.helper)
#         if not parameter and not filme:
#             return content()
#         else:
#             return content(parameter, filme)


#     def get_session_id(self):
#         return request.get_cookie('session_id')

#     def helper(self):
#         return template('app/views/html/helper')

#     def portal(self):
#         return template('app/views/html/portal')

#     def pagina(self, usuario=None, filme=None):
#         if self.is_authenticated(usuario):
#             id_sessao = self.get_session_id()
#             usuario_atual = self.__model.getCurrentUser(id_sessao)
#             return template('app/views/html/pagina', usuario_atual=usuario_atual, filme=filme)
#         else:
#             return template('app/views/html/pagina', usuario_atual=None, filme=filme)
        
#     def is_authenticated(self, username):
#         session_id = self.get_session_id()
#         current_username = self.__model.getUserName(session_id)
#         return username == current_username

#     def authenticate_user(self, username, password):
#         session_id = self.__model.checkUser(username, password)
#         if session_id:
#             self.logout_user()
#             self.__current_username = self.__model.getUserName(session_id)
#             return session_id, username
#         return None

#     def logout_user(self):
#         self.__current_username = None
#         session_id = self.get_session_id()
#         if session_id:
#             self.__model.logout(session_id)
    
#     def comentarios(self):
#         return template('app/views/html/comentarios')

    
#     def create_user(self, username, password):
#         # Tenta criar o novo usuário
#         user_created = self.__model.create_new_user(username, password)
        
#         if user_created:
#             return True 
#         else:
#             return False 


from bottle import Bottle, run, template, request, redirect
from controllers.user_controller import UserController
from controllers.movie_controller import MovieController
from controllers.review_controller import ReviewController
from controllers.list_controller import ListController

app = Bottle()

# Instâncias dos controladores
user_controller = UserController()
movie_controller = MovieController()
review_controller = ReviewController()
list_controller = ListController()

# Rota inicial
@app.route('/')
def home():
    return template('views/html/home.html')

# Rota para registro de usuário
@app.route('/register', method='POST')
def register():
    nome = request.forms.get('nome')
    email = request.forms.get('email')
    senha = request.forms.get('senha')
    user_controller.register_user(nome, email, senha)
    return "Usuário registrado com sucesso!"

# Rota para login
@app.route('/login', method='POST')
def login():
    email = request.forms.get('email')
    senha = request.forms.get('senha')
    if user_controller.login_user(email, senha):
        return "Login bem-sucedido!"
    else:
        return "Falha no login."

# Rota para adicionar filme
@app.route('/add_movie', method='POST')
def add_movie():
    titulo = request.forms.get('titulo')
    diretor = request.forms.get('diretor')
    genero = request.forms.get('genero')
    movie_controller.add_movie(titulo, diretor, genero)
    return "Filme adicionado com sucesso!"

if __name__ == '__main__':
    run(app, host='localhost', port=8080, debug=True)