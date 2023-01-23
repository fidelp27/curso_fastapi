from http.client import HTTPException
from fastapi import FastAPI, Body, Path, Query, Request, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPBearer
from pydantic import BaseModel, Field
from typing import Optional
from jwt_manager import create_token, validate_token

app = FastAPI(title="nombreAPP",
              description="un intento de api",
              version="0.0.1",
              terms_of_service="http://example.com/terms/",
              contact={
                  "name": "Fidelp27",
                  "url": "https://fidelp27.github.io/portfolio/",
                  "email": "telocreiste@gmail.com"
              },
              license_info={
                  "name": "Apache 2.0",
                  "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
              })


class User(BaseModel):
    email: str
    password: str


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data["email"] != "admin@gmail.com":
            raise HTTPException(
                status_code=403, detail="Credenciales no válidas")


class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5, max_length=40, msg='madura')
    overview: str = Field(min_length=5, max_length=100)
    year: int = Field(le=2022)
    rating: float = Field(ge=0, le=10)
    category: str = Field(min_length=5, max_length=15)

    class Config:
        schema_extra = {
            "default": {
                "id": 1,
                "title": "Mi película",
                "overview": "Descripción",
                "year": 2022,
                "rating": 8.0,
                "category": "Accion"
            }
        }


movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'
    },
    {
        'id': 2,
        'title': 'Avatar 2',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2022',
        'rating': 8.8,
        'category': 'Drama'
    }]


@app.get("/movies", tags=["movies"], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies():
    return JSONResponse(status_code=200, content=movies)


@app.get("/movies/{id}",  tags=["movies"])
def get_movie(id: int = Path(ge=1, le=2000)):
    movie = list(filter(lambda x: x["id"] == id, movies))
    if movie != []:
        return JSONResponse(content=movie)
    else:
        return JSONResponse(status_code=404, content={"message": "Movie not found"})


@app.get("/movies/", tags=["movies"])
def get_category(category: str = Query(min_length=5, max_length=15)):
    categoria = [movie for movie in movies if movie["category"] == category]
    return JSONResponse(content=categoria)


@app.post("/movies", tags=["movies"], status_code=201)
def create_movie(movie: Movie):
    movies.append(movie)
    return JSONResponse(status_code=201, content={"message": "Movie created successfully"})


@app.delete("/movies/{id}", tags=["movies"])
def delete_movie(id: int):
    for movie in movies:
        if movie["id"] == id:
            movies.remove(movie)
            return JSONResponse(content={"message": "movie deleted"})


@app.put("/movies/{id}", tags=["movies"])
def update_movie(id: int, movie: Movie):
    for mov in movies:
        if mov["id"] == id:
            mov.update(movie)
            return JSONResponse(content={"message": "Movie updated successfully"})


@app.post("/login", tags=["auth"])
def login(user: User):
    if (user.email == "admin@gmail.com" and user.password == "123456"):
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)
    else:
        return JSONResponse(status_code=401, content={"message": "Credenciales inválidas, intente de nuevo"})
