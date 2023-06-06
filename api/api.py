from fastapi import APIRouter
from api.endpoints import medicamentos

api_router = APIRouter()

api_router.include_router(medicamentos.router, prefix="/medicamentos", tags=["medicamentos"])

