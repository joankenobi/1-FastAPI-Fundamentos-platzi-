from fastapi import FastAPI #crea la app
from fastapi import status # status code con alguna definicion
from fastapi import Body #se usa para que un conjunto de datos de entrada 
                            #se comporten como un request body y no como un query parameter
from fastapi import Path # permiten aplicar validaciones y configuracion a los tipos de parametros
from fastapi import Query # permiten aplicar validaciones y configuracion a los tipos de parametros
from fastapi.responses import HTMLResponse # permite respuestas en formato HTML
from fastapi.responses import JSONResponse # permite repuestas en formato Json
from pydantic import BaseModel #permite la creacion facil de modelos
from pydantic import Field #permite la implementacion de validaciones y datos defaults
from typing import Optional # indica condiciones a las variables
from typing import List # indica tipo de variable, puede contener otros tipos.
from jwt_manager import create_token

# inicia la app
app =FastAPI()
app.title = "Mi aplicacion con FastApi (Joan)"
app.version = "0.0.1"


#------------ El modelo (clase) para la creacion de objetos "movies" --------

class User(BaseModel):
    '''
        Clase para el ojeto user, datos para autenticar.
    '''
    email:str
    pasword:str

class Movie(BaseModel):
    ''''
        Con esta clase no es necesario estar agregando cada parametro de las "Movies" en los metodos post and delete.
    '''
    id: Optional[int] = None
    title: str = Field(min_length=5, max_length=15)
    overview: str = Field(min_length=15, max_length=50)
    year: int = Field(le=2022)
    rating: float = Field(ge=1, le=10)
    category: str = Field(min_length=5, max_length=15)

    class Config:
        '''
            con esta clase se puden colocar datos de ejemplo a los bodies.
        '''
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Mi película",
                "overview": "Descripción de la película",
                "year": 2022,
                "rating": 9.8,
                "category" : "Acción"
            }
        }

# Datos a modificar
movies= [
    {
        "id": 1,
        "title": "Avatar Ang",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        "year": "2009",
        "rating": 7.8,
        "category": "Comedia"
    },
    {
        "id": 2,
        "title": "Avatar",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        "year": "2009",
        "rating": 7.8,
        "category": "Acción"
    },
]

#------------ Get method --------
@app.get(path='/', tags=['home'])
#queremos que al entrar a la raiz de la web imprima un mensaje.
def message():
    return HTMLResponse('<h1>Hello word</h1>')

#queremos que cuando habra la direccion de Movies muestre la lista de peliculas
@app.get(
    path='/movies', 
    tags=['Movies'], 
    status_code=status.HTTP_200_OK,
    response_model= List[Movie] # indica el tipo de repuesta
        ) #path decorator
def get_movies() -> List[Movie]:
    return JSONResponse( content=movies, status_code=status.HTTP_200_OK) # se especifica que es un formato Json

    #*********************** Path parameter *****************************

#queremos que al indicar el {id} en la direccion retorne la pelicula con el {id} indicado
#NOTA: por alguna razon solo funciona con id=1 //////// la identacion del return era erronea.
@app.get(path='/movies/{id}', tags=['Movies'], response_model=Movie )
def get_movie(id: int = Path(ge=0, le=2000)) -> Movie: #aplica validaciones al Path parameter.
    for item in movies:
        if item["id"] == id:
            return JSONResponse( content=item, status_code=status.HTTP_200_OK)
    return JSONResponse( content=[], status_code=status.HTTP_404_NOT_FOUND)
    #********************************************************************

    #*********************** Query parameter *****************************

#queremos que por medio de el path /movies/ filtre las movies con query parameters
@app.get(path='/movies/', tags=['Movies'], response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    data= [item for item in movies if item['category'] == category]
    return JSONResponse( content=data)
    #********************************************************************

#------------ Post method --------
@app.post('/login', tags=['auth'])
def login(user: User):
    if user.email == "admin@gmail.com" and user.pasword == "admin":
        token: str = create_token(user.dict())
        return JSONResponse(status_code= status.HTTP_200_OK, content= token)

#queremos que con el metodo post de cree una nueva pelucula
@app.post(path='/movies', tags=['Movies'], response_model=dict)
def create_movie(movie:Movie)-> dict:
    movies.append(movie) #revisar los commits para ver como se hacia antes de aplicar las clases
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": f"Se ha registrado la pelicula con el id {movie.id}"})

#------------ Put method --------

#con el metodo put se busca actualizar una movie en especifico
@app.put('/movies/{id}', tags=['Movies'], response_model=dict, status_code=status.HTTP_201_CREATED)
def update_movie(id:int, movie:Movie) -> dict:
    for item in movies:
        if item["id"]==id:
            item["title"]= movie.title
            item["overview"]= movie.overview
            item["year"]= movie.year
            item["rating"]= movie.rating
            item["category"]= movie.category
            return JSONResponse( content={"message":f"Se actualizo la pelicula con el id : {id}"})


#------------ Delete method --------

#queremos que cuando se le pase un {id} al movies/{id} pero con el metodo delete, se borre la peli con ese id
@app.delete('/movies/{id}', tags=['Movies'], response_model=dict, status_code=status.HTTP_202_ACCEPTED) # los tags organizan los metodos en la documentacion automatica
def delete_movie(id: int) -> dict:
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
            return JSONResponse( content={"message":f"Se elimino la pelicula con el id : {id}"})

if __name__=="__main__":
    print(movies)            