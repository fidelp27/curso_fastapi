from models.movie import Movie as MovieModel
from schemas.movie import Movie
from fastapi.responses import JSONResponse


class MovieService():

    def __init__(self, db) -> None:
        self.db = db

    def get_movies(self):
        result = self.db.query(MovieModel).all()
        return result

    def get_movie(self, id):
        result = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        return result

    def get_category(self, category: str):
        result = self.db.query(MovieModel).filter(
            MovieModel.category == category).all()
        return result

    def create_movie(self, movie: Movie):
        new_movie = MovieModel(**movie.dict())
        self.db.add(new_movie)
        self.db.commit()
        return

    def update_movie(self, id: int, movie: Movie):
        result = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        if movie:
            movie_attributes = [k for k, v in vars(movie).items(
            ) if not callable(v)]
            for attr in movie_attributes:
                if hasattr(result, attr) and hasattr(movie, attr):
                    setattr(result, attr, getattr(movie, attr))
        self.db.commit()
        return

    def delete_movie(self, id: int):
        self.db.query(MovieModel).filter(MovieModel.id == id).delete()
        self.db.commit()
        return
