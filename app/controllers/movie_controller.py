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
        url = f"{self.base_url}/movie/{movie_id}"
        params = {"api_key": self.api_key}
        response = requests.get(url, params=params)
        data = response.json()

        if response.status_code != 200 or "success" in data and not data["success"]:
            raise Exception("Erro ao buscar detalhes do filme.")

        movie_data = {
            "id": data.get("id"),
            "title": data.get("title", "Título Desconhecido"),
            "poster_path": data.get("poster_path", ""),
            "release_date": data.get("release_date", "Data desconhecida"),
            "runtime": data.get("runtime", "Duração desconhecida"),
            "vote_average": data.get("vote_average", "Avaliação desconhecida"),
            "overview": data.get("overview", "Sinopse indisponível")
        }

        return movie_data