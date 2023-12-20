from fastapi import APIRouter


from api.endpoints import medicamentos, usuario


api_router = APIRouter()






api_router.include_router(medicamentos.router, prefix="/medicamentos", tags=["medicamentos"])
api_router.include_router(usuario.router, prefix="/usuario", tags=["usuario"])

