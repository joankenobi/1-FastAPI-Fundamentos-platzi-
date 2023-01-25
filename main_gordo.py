from fastapi import Depends
from fastapi import FastAPI #crea la app
from fastapi import Body #se usa para que un conjunto de datos de entrada 
                            #se comporten como un request body y no como un query parameter
from fastapi import HTTPException
from fastapi import Path # permiten aplicar validaciones y configuracion a los tipos de parametros
from fastapi import Query # permiten aplicar validaciones y configuracion a los tipos de parametros
from fastapi import status # status code con alguna definicion
from fastapi import Request
from fastapi.responses import HTMLResponse # permite respuestas en formato HTML
from fastapi.responses import JSONResponse # permite repuestas en formato Json
from fastapi.security import HTTPBearer
from fastapi.encoders import jsonable_encoder # encodear datos a Json

from pydantic import BaseModel #permite la creacion facil de modelos
from pydantic import Field #permite la implementacion de validaciones y datos defaults
from typing import Optional # indica condiciones a las variables

from typing import List # indica tipo de variable, puede contener otros tipos.

from jwt_manager import create_token
from jwt_manager import validate_token

from config.database import d_base, session, engine
from models.movie import Movie as Movie_dbmodel
from routers.movie import movie_router



# inicia la app
app =FastAPI()
app.title = "Mi aplicacion con FastApi (Joan)"
app.version = "0.0.1"
app.include_router(movie_router)

d_base.metadata.create_all(
    bind=engine #parece que bind debe recibir el motor
    )

#------------ El modelo (clase) para la creacion de objetos "movies" --------

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data["email"] != "admin@gmail.com":
            raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail="Credenciales invalidas")

class User(BaseModel):
    '''
        Clase para el ojeto user, datos para autenticar.
    '''
    email:str
    pasword:str

#------------ Post method --------
@app.post('/login', tags=['auth'])
def login(user: User):
    if user.email == "admin@gmail.com" and user.pasword == "admin":
        token: str = create_token(user.dict())
        return JSONResponse(status_code= status.HTTP_200_OK, content= token)

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

if __name__=="__main__":
    print(movies)            