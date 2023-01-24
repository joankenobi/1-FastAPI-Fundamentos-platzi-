from starlette.middleware.base import BaseHTTPMiddleware #manejador de errores HTTP???
from fastapi import FastAPI
from fastapi import Request #permite acceder al request de la peticion
from fastapi import Response #permite acceder al Response de la peticion
from fastapi.responses import JSONResponse
from fastapi import status

class ErrorHandler(BaseHTTPMiddleware):
    """
        Manejador de errores dentro de la app del tipo FastApi
    """
    def __init__(self, app: FastAPI ) -> None:
        super().__init__(app) # al super (de donde hereda) le enviamos la app
        
    async def dispatch(self, 
        request: Request, 
        call_next, # en caso de que no ocurra un error va a ejecutar la siguiente funcion
            ) -> Response | JSONResponse: # si no hay error retorna un Response de lo contrario un JsonResponse
        """
            Escucha y retorna cada error existente al ejecutar un endpoint
            
            """
        try:
            #trata ejecutar la siguiente funcion
            return await call_next(Request)
        except Exception as e:
            return JSONResponse(
                status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, 
                content={"Error":str(e)},
                )