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