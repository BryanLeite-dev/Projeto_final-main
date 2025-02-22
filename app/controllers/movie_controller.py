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
            url = f"{self.base_url}/movie/{movie_id}"
            params = {"api_key": self.api_key}
            response = requests.get(url, params=params)
            response.raise_for_status()  # Levanta exceção para códigos HTTP de erro (4xx, 5xx)
            data = response.json()

            if "success" in data and not data["success"]:
                error_message = data.get("status_message", "Erro desconhecido ao buscar detalhes do filme.")
                raise Exception(f"Erro na API do TMDB: {error_message}")

            return {
                "id": data.get("id"),
                "title": data.get("title", "Título Desconhecido"),
                "poster_path": f"https://image.tmdb.org/t/p/w500{data.get('poster_path', '')}" if data.get('poster_path') else None,
                "release_date": data.get("release_date", "Data desconhecida"),
                "runtime": data.get("runtime", "Duração desconhecida"),
                "vote_average": data.get("vote_average", "Avaliação desconhecida"),
                "overview": data.get("overview", "Sinopse indisponível")
            }

        except Exception as e:
            print(f"Erro ao buscar detalhes do filme com ID {movie_id}: {e}")
            return None