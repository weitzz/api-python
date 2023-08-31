from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from core.configs import settings
from api.api import api_router


app = FastAPI(title='Pharma API')

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:3000/medicamentos",
    "https://localhost:3000/medicamentos",
    "http://localhost:3000/",
    "https://localhost:3000"

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_STR)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000,
                log_level='info', reload=True)
