from bottle import Bottle, template, request, redirect, abort, static_file
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from app.controllers.websocket_controller import WebSocketController
from app.controllers.user_controller import UserController
from app.controllers.movie_controller import MovieController
from app.controllers.review_controller import ReviewController

app = Bottle()
websocket_controller = WebSocketController()
user_controller = UserController()
movie_controller = MovieController(api_key="dc1dffa08f0aca6d03c2e75d3c25de0a")
review_controller = ReviewController()

# Rotas estáticas
@app.route('/static/<filename:path>')
def serve_static(filename):
    return static_file(filename, root='app/views/static/')

# Página inicial
@app.route('/')
def index():
    if not user_controller.is_authenticated():
        return redirect('/inicio')
    return template('app/views/html/inicio.html')

@app.route('/home')
def home():
    popular_movies = movie_controller.get_popular_movies()
    now_playing_movies = movie_controller.get_now_playing_movies()
    print(f"Filmes populares: {popular_movies}")
    print(f"Filmes em cartaz: {now_playing_movies}")
    return template('app/views/html/home.html', popular_movies=popular_movies, now_playing_movies=now_playing_movies)

# Registro de usuário
@app.route('/register', method=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.forms.get('nome')
        email = request.forms.get('email')
        senha = request.forms.get('senha')
        if user_controller.register_user(nome, email, senha):
            pass
        else:
            return """
             Erro: Email já em uso
Voltar para a Página Inicial
            """
    return template('app/views/html/register.html')

# Login de usuário
@app.route('/login', method=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.forms.get('email')
        senha = request.forms.get('senha')
        if user_controller.login_user(email, senha):
            return redirect('/home')
        else:
            return """
             Erro: Email ou senha incorretos!
Voltar para a Página Inicial
            """
    return template('app/views/html/login.html')

# Logout de usuário
@app.route('/logout')
def logout():
    user_controller.logout_user()
    return redirect('/inicio')

@app.route('/inicio')
def inicio():
    return template('app/views/html/inicio.html')

# Página de perfil
@app.route('/profile')
def profile():
    try:
        if not user_controller.is_authenticated():
            print("Usuário não autenticado. Redirecionando para /login.")
            return redirect('/login')

        # Obtém o email do usuário logado
        if not user_controller.logged_in_user or 'email' not in user_controller.logged_in_user:
            raise ValueError("Usuário logado não possui email.")

        email = user_controller.logged_in_user['email']
        print(f"Email do usuário logado: {email}")

        # Obtém as avaliações do usuário
        user_reviews = user_controller.get_user_reviews(email)
        print(f"Avaliações do usuário: {user_reviews}")

        # Passa as avaliações como parte do contexto do template
        return template('app/views/html/profile.html', user=user_controller.logged_in_user, reviews=user_reviews)

    except Exception as e:
        print(f"Erro ao processar a rota /profile: {e}")
        return "Erro interno no servidor. Por favor, tente novamente mais tarde."

# Detalhes do filme
@app.route('/movie/<movie_id>', method=['GET', 'POST'])
def movie_details(movie_id):
    if not user_controller.is_authenticated():
        return redirect('/login')

    try:
        # Busca os detalhes do filme usando a API do TMDB
        movie = movie_controller.get_movie_details(movie_id)

        # Obtém as avaliações do filme
        reviews = review_controller.get_reviews_by_movie(movie_id)

        if request.method == 'POST':
            comentario = request.forms.get('comentario')
            nota = request.forms.get('nota')

            # Validação dos dados do formulário
            if not comentario or not nota:
                return "Erro: Comentário e nota são obrigatórios."

            try:
                nota = int(nota)
                if nota < 1 or nota > 10:
                    return "Erro: A nota deve ser um número entre 1 e 10."
            except ValueError:
                return "Erro: A nota deve ser um número válido."

            # Adiciona a avaliação
            review_controller.add_review(user_controller.logged_in_user['email'], movie_id, comentario, nota)
            return redirect(f'/movie/{movie_id}')

        return template('app/views/html/movie_details.html', movie=movie, reviews=reviews)

    except Exception as e:
        print(f"Erro ao processar a rota /movie/{movie_id}: {e}")
        return "Erro interno no servidor. Por favor, tente novamente mais tarde."

# WebSocket
@app.route('/websocket')
def handle_websocket():
    ws = request.environ.get('wsgi.websocket')
    if not ws:
        abort(400, "Expected WebSocket request.")
    
    websocket_controller.add_client(ws)

    try:
        while True:
            message = ws.receive()
            if message is None:
                break
            ws.send(f"Echo: {message}")
    finally:
        websocket_controller.remove_client(ws)
    
if __name__ == '__main__':
    server = WSGIServer(("localhost", 8080), app, handler_class=WebSocketHandler)
    print("Servidor iniciado em http://localhost:8080/")
    server.serve_forever()