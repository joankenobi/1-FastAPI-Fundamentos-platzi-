from jwt import encode, decode

def create_token(data:dict):
    '''
        Combierte data en token
    '''
    token: str = encode(payload=data, key="my_secrete_key", algorithm="HS256")
    return token

def validate_token(token: str) -> dict:
    '''
        Combierte token en data
    '''
    data: dict = decode(token, key="my_secret_key", algorithms=['HS256'])
    return data

if __name__=="__main__":
    print("te pica")
    ## para activar un VENV usar en win .\venv\Scripts\activate  
    #Notas del curso: https://telegra.ph/Curso-de-FastAPI-Base-de-Datos-Modularizaci%C3%B3n-y-Deploy-a-Producci%C3%B3n-01-21