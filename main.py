#Python
from typing import Optional, List
from enum import Enum # Permite la creacion de varias opciones para un campo

#Pydantic
from pydantic import BaseModel #Los modelos base estan Relacionado con el curso de SQL
from pydantic import Field # Permite crear validaciones para un campo o variable
from pydantic import NegativeFloat # es un validador de formato dentro de pydantic para numeros menores a cero
from pydantic import EmailStr
from pydantic import HttpUrl

#FastApi
from fastapi import FastAPI
from fastapi import status
from fastapi import Body #permite indicar que un parametro es del tipo Body el cual recibe varios parametros.
from fastapi import Query # permite la query validations
from fastapi import Path # permite los path parameters /{}

#crear un objeto FastAPI 

app= FastAPI()

#Models
class HairColor(Enum):
    white="white"
    brown="brown"
    black="black"
    blonde="blonde"

class Location(BaseModel):
    city: str = Field(
        None,
        example="Caracas",
    )

    state: str =Field(
        None,
        example="Lara",
    )        
    country: str =Field(
        None,
        example="Guatire",
    )        

class Person(BaseModel): #hereda de Base model y se crea la clase (molde)
    first_name: str = Field(
        ...,
        max_length=155,
        min_length=2,
        example="Joel Base model",
        description="El primer nombre"
    )
    last_name: str = Field(
        ...,
        max_length=155,
        example="Blanco Base model",
        min_length=2
    )
    age: int = Field(
        lt=155, 
        example=27,
        gt=0)
    hair_color: Optional[HairColor] = Field(
        None,
        example=HairColor.black,
        )
    is_married: Optional[bool] = Field(None)
    email: Optional[EmailStr] = Field(None)
    ice: Optional[NegativeFloat] = Field(
        None,
        description="indica en numero negativos la temperatura del hielo",
        example=-5
        )
    url: Optional[HttpUrl] = Field(
        None,
        description="la url completa, Example: http://www.elHelado.com",
        example="http://www.base_model_example.com"
    )
    password: str = Field(
        ...,
        min_length=8,
        example="model_pasword_example"
        )

#Decorador
@app.get(
    path='/', 
    status_code=status.HTTP_200_OK
) #Path Operations Decorator (el que entre en esta direccion y ejecute Get)
def home(): #Path Operations Funtion (Obtendra este resultado)
    return {
        "Hola":"World"
    }

@app.post(path='/person/new',
    status_code=status.HTTP_201_CREATED,
    response_model =Person, # defina el modelo de la repuesta
    response_model_exclude ={"password"}, # define que parametro omitir de este modelo
) #Path Operations Decorator (el que entre en esta direccion y ejecute post) enviar
def create_person(
    person: Person = Body(...), # ... indica que el parametro y el atributo es obligatorio.
                    ): # el requets body es el parametro person type(Person)
    return person

# Validations: Query Parameters

@app.get(path="/person/detail",
    status_code=status.HTTP_200_OK
    )
def show_person(
    name: Optional[str] = Query( #El query contiene las caracteristicas del parametro
        default= None,
        min_length= 1,
        max_length= 50,
        title="Person Name",
        example="Joan example Query parameter",
        description= "Thi is the person name. It's between 1 and 50 characters"
    ),
    age: int= Query(
        ..., # es obligatorio colocarlo
        title= "Person Age",
        example=30,
        description= "This is the person age. It's required"
    )
):
    return {name: age}

# Validations: Path Parameters

@app.get(path="/person/detail/{person_id}",
    status_code=status.HTTP_202_ACCEPTED
) # {person_id} es un path parameter
def show_person(
    person_id: int = Path(
        ..., 
        gt=0,
        example=222
        )
):
    return {person_id: "It exist!"}

# Request Body

@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path( # Debe recibir 
        ...,
        title="Person ID",
        description="This is the person ID",
        gt=0,
        example=333
    ),
    person: Person = Body(...),
    location: Location = Body(...),
):
    results = person.dict()
    results.update(location.dict())
    return results
#
#Para correr el codigo usar en el terminal: uvicorn main:app --reload
#Notas: https://telegra.ph/Curso-de-FastAPI-Fundamentos-Path-Operations-y-Validaciones-11-27
#Notas del segundo curso relacionado: https://telegra.ph/Curso-de-FastAPI-Modularizaci%C3%B3n-Datos-Avanzados-y-Errores-12-13
#Para probar los metodos hay que aplicar docs al final de la direccion exampl: http://127.0.0.1:8000/docs
