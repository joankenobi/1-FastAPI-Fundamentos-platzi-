from fastapi import FastAPI #crea la app
from fastapi import Body #se usa para que un conjunto de datos de entrada 
                            #se comporten como un request body y no como un query parameter
from fastapi.responses import HTMLResponse
from pydantic import BaseModel #permite la creacion facil de modelos
from typing import Optional # indica condiciones a las variables


# inicia la app
app =FastAPI()
app.title = "Mi aplicacion con FastApi"
app.version = "0.0.1"


#------------ El modelo (clase) para la creacion de objetos "movies" --------
class Movie(BaseModel):
	''''
		Con esta clase no es necesario estar agregando cada parametro de las "Movies" en los metodos post and delete.
	'''
	id: Optional[int] = None
	title: str
	overview: str
	year: int
	rating: float
	category: str


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
@app.get(path='/movies', tags=['Movies']) #path decorator
def get_movies():
	return movies

#queremos que al indicar el {id} en la direccion retorne la pelicula con el {id} indicado
#NOTA: por alguna razon solo funciona con id=1 //////// la identacion del return era erronea.
@app.get(path='/movies/{id}', tags=['Movies'])
def get_movie(id: int):
	for item in movies:
		if item["id"] == id:
			return item
	return []

#queremos que por medio de el path /movies/ filtre las movies con query parameters
@app.get(path='/movies/', tags=['Movies'])
def get_movies_by_category(category: str, year: int):
	return [item for item in movies if item['category'] == category]

#------------ Post method --------

#
@app.post(path='/movies', tags=['Movies'])
def create_movie(
	id: int = Body(),
	title: str = Body(),
	overview: str = Body(),
	year:int = Body(), 
	rating: float = Body(), 
	category: str = Body(),
):
	movies.append({
			"id": id,
			"title": title,
			"overview": overview,
			"year": year,
			"rating": rating,
			"category": category
	})
	return movies

#------------ Delete method --------

#queremos que cuando se le pase un {id} al movies/{id} pero con el metodo delete, se borre la peli con ese id
@app.delete('/movies/{id}', tags=['movies'])
def delete_movie(id: int):
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
            return movies