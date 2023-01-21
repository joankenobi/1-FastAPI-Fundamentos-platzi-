from config.database import d_base #declara una entidad de la base de datos

from sqlalchemy import Column
from sqlalchemy import Integer,String, Float

class Movie (d_base):
    """Modelo de objeto para movie"""

    __tablename__= "movies"

    id=Column(Integer, primary_key=True)
    title=Column(String)
    overview=Column(String)
    year=Column(Float)
    rating=Column(Integer)
    category=Column(String)