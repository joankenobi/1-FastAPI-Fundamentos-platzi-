import os
from sqlalchemy import create_engine #crear motor de la base de datos
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base # permite manejar las tablas de la db
#Valores de configuracion para aplicar con sqlalchemy

sqlite_file_name="database.sqlite" #nombre de la base de datos
base_dir= os.path.dirname(os.path.realpath(__file__))#direccion del presente archivo

data_base_url=f"""sqlite:///{os.path.join(
    base_dir, 
    "../",#construir en la carpeta raiz
    sqlite_file_name
    )}""" #la direccion de la base de datos y donde se desea crear

engine=create_engine(
    data_base_url,
    echo=True, # retorna el codigo implementado en las acciones con la base de datos
    ) # el motor se crea con la url de la base de datos

session=sessionmaker(
    bind=engine #no se que es esto ????????
    ) 


if __name__=="__main__":
    print(f"base_dir==== {base_dir}")
    print(f"data_base_url ==== {data_base_url}")
    print(f"engine ==== {engine}")
d_base=declarative_base()