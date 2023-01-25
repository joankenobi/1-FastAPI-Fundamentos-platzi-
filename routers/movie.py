from fastapi import APIRouter
from fastapi import Body #se usa para que un conjunto de datos de entrada 
                            #se comporten como un request body y no como un query parameter
from fastapi import Path # permiten aplicar validaciones y configuracion a los tipos de parametros
from fastapi import Query # permiten aplicar validaciones y configuracion a los tipos de parametros
from fastapi import status # status code con alguna definicion
from fastapi.responses import JSONResponse # permite repuestas en formato Json
from fastapi.encoders import jsonable_encoder # encodear datos a Json

from pydantic import BaseModel #permite la creacion facil de modelos
from pydantic import Field #permite la implementacion de validaciones y datos defaults
from typing import Optional # indica condiciones a las variables

from typing import List # indica tipo de variable, puede contener otros tipos.

from config.database import session
from models.movie import Movie as Movie_dbmodel
movie_router=APIRouter()

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

#queremos que cuando habra la direccion de Movies muestre la lista de peliculas
@movie_router.get(
    path='/movies', 
    tags=['Movies'], 
    status_code=status.HTTP_200_OK,
    response_model= List[Movie] # indica el tipo de repuesta
    #dependencies=[
    #    Depends(JWTBearer())
    #]
        ) #path decorator

def get_movies() -> List[Movie]:
    db = session()
    result = db.query(Movie_dbmodel).all() #query es para consultar, se le pasa el nombre de la tabla (el modelo)
    return JSONResponse( content=jsonable_encoder(result), status_code=status.HTTP_200_OK) # se especifica que es un formato Json

    #*********************** Path parameter *****************************

#queremos que al indicar el {id} en la direccion retorne la pelicula con el {id} indicado
#NOTA: por alguna razon solo funciona con id=1 //////// la identacion del return era erronea.
@movie_router.get(path='/movies/{id}', tags=['Movies'], response_model=Movie )
def get_movie(id: int = Path(ge=0, le=2000)) -> Movie: #aplica validaciones al Path parameter.
    db=session()
    result=db.query(Movie_dbmodel).filter(Movie_dbmodel.id == id).first()
    if not result:
        return JSONResponse( content=[], status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse( content=jsonable_encoder(result), status_code=status.HTTP_200_OK)
    #********************************************************************

    #*********************** Query parameter *****************************

#queremos que por medio de el path /movies/ filtre las movies con query parameters
@movie_router.get(path='/movies/', tags=['Movies'], response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    db=session()
    result=db.query(Movie_dbmodel).filter(Movie_dbmodel.category == category).all()
    if not result:
        return JSONResponse( content=[], status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse( content=jsonable_encoder(result))
    #********************************************************************


#queremos que con el metodo post de cree una nueva pelucula
@movie_router.post(path='/movies', tags=['Movies'], response_model=dict,status_code=status.HTTP_201_CREATED)
def create_movie(movie:Movie)-> dict:
    db=session() #para conectar con la base de datos
    new_movie=Movie_dbmodel(**movie.dict()) #completamos la entidad db con el modelo dict
    db.add(new_movie)#agrega a la tabla
    db.commit()#guarda cambios en la tabla
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": f"Se ha registrado la pelicula con el id {movie.id}"})

#------------ Put method --------

#con el metodo put se busca actualizar una movie en especifico
@movie_router.put('/movies/{id}', tags=['Movies'], response_model=dict, status_code=status.HTTP_201_CREATED)
def update_movie(id:int, movie:Movie) -> dict:
    db=session()
    result=db.query(Movie_dbmodel).filter(Movie_dbmodel.id == id).first()
    if not result:
        return JSONResponse( content=[], status_code=status.HTTP_404_NOT_FOUND)
    #Actualizar los siguientes datos del result
    result.title = movie.title
    result.overview = movie.overview
    result.year = movie.year
    result.rating = movie.rating
    result.category = movie.category
    db.commit() #guardar los cambios.
    return JSONResponse( content={"message":f"Se actualizo la pelicula con el id : {id}"})


#------------ Delete method --------

#queremos que cuando se le pase un {id} al movies/{id} pero con el metodo delete, se borre la peli con ese id
@movie_router.delete('/movies/{id}', tags=['Movies'], response_model=dict, status_code=status.HTTP_202_ACCEPTED) # los tags organizan los metodos en la documentacion automatica
def delete_movie(id: int) -> dict:
    db=session()
    result=db.query(Movie_dbmodel).filter(Movie_dbmodel.id == id).first()
    if not result:
        return JSONResponse( content=[], status_code=status.HTTP_404_NOT_FOUND)
    db.delete(result)
    db.commit() #guardar los cambios.
    return JSONResponse( content={"message":f"Se elimino la pelicula con el id : {id}"})
