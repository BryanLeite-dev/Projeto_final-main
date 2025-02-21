import requests

class MovieController:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.themoviedb.org/3"

    def get_popular_movies(self):
        url = f"{self.base_url}/movie/popular"
        params = {"api_key": self.api_key}
        response = requests.get(url, params=params)
        return response.json().get("results", [])

    def get_now_playing_movies(self):
        url = f"{self.base_url}/movie/now_playing"
        params = {"api_key": self.api_key}
        response = requests.get(url, params=params)
        return response.json().get("results", [])

    def get_movie_details(self, movie_id):
        try:
            if not isinstance(movie_id, int):
                raise ValueError("O ID do filme deve ser um número inteiro.")

            url = f"{self.base_url}/movie/{movie_id}"
            params = {"api_key": self.api_key}

            response = requests.get(url, params=params)
            response.raise_for_status() # Levanta uma exceção para códigos HTTP de erro (4xx, 5xx)

            data = response.json()

            if "success" in data and not data["success"]:
                error_message = data.get("status_message", "Erro desconhecido ao buscar detalhes do filme.")
                raise Exception(f"Erro na API do TMDB: {error_message}")                   

            return {
                "id": data.get("id"),
                "title": data.get("title", "Título Desconhecido"),
                "poster_path": data.get("poster_path", ""),
                "release_date": data.get("release_date", "Data desconhecida"),
                "runtime": data.get("runtime", "Duração desconhecida"),
                "vote_average": data.get("vote_average", "Avaliação desconhecida"),
                "overview": data.get("overview", "Sinopse indisponível")
            }                     
        
        except ValueError as ve:
            # Captura erros relacionados à validação do movie_id
            print(f"Erro de validação: {ve}")
            return None

        except requests.exceptions.RequestException as re:
            # Captura erros relacionados à requisição HTTP (ex.: timeout, conexão falhou)
            print(f"Erro de requisição HTTP: {re}")
            return None

        except KeyError as ke:
            # Captura erros relacionados à estrutura incorreta dos dados JSON
            print(f"Erro ao acessar os dados da API: chave '{ke}' não encontrada.")
            return None

        except Exception as e:
            # Captura qualquer outro erro inesperado
            print(f"Erro inesperado ao buscar detalhes do filme: {e}")
            return None