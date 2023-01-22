from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse

app = FastAPI(title="nombreAPP",
    description="un intento de api",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact = {
        "name": "Fidelp27",
        "url": "https://fidelp27.github.io/portfolio/",
        "email": "telocreiste@gmail.com"
    },    
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    })

movies =[
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

@app.get('/', tags=["home"])
def message():
    return HTMLResponse("<h1>Hola pana</h1>")

@app.get("/movies", tags=["movies"])
def get_movies():
    return movies
    
@app.get("/movies/{id}",  tags=["movies"])
def get_movie(id: int):
    movie = list(filter(lambda x: x["id"] == id, movies))
    return movie
    
@app.get("/movies/",tags=["movies"])
def get_category(category: str):
    categoria = [movie for movie in movies if movie["category"] == category]
    return categoria

@app.post("/movies", tags=["movies"])
def create_movie(id: int = Body(), title: str = Body(), overview: str = Body(), year:int = Body(), rating: float = Body(), category: str = Body()):
    movies.append(
        {
            "id": id,
            "title": title,
            "overview": overview,
            "year": year,
            "rating": rating,
            "category": category
        }
    )
    return movies

@app.delete("/movies/{id}", tags=["movies"])
def delete_movie(id: int):
    global movies
    
    return peliculas
    
@app.put("/movies/", tags=["movies"])
def update_movie(id: int = Body(), title: str = Body(), overview: str = Body(), year:int = Body(), rating: float = Body(), category: str = Body()):
    for movie in movies:
        if movie["id"] == id:
            movie.update(
                {
                    "id": id,
                    "title": title,
                    "overview": overview,
                    "year": year,
                    "rating": rating,
                    "category": category
                }
            )
    return movies


            
