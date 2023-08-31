import os
import shutil
import uuid
from pathlib import Path
from typing import List, Optional
from fastapi import APIRouter, status, Depends, HTTPException, Response, UploadFile, File, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from models.medicamento_model import MedicamentoModel
from schemas.medicamento_schema import MedicamentoSchema
from core.deps import get_session

IMAGEDIR = "images/"

#
# app = FastAPI()
#
#
# origins = [
#     "http://localhost",
#     "http://localhost:3000",
#     "http://localhost:3000/medicamentos",
#     "https://localhost:3000/medicamentos",
#     "http://localhost:3000/",
#     "https://localhost:3000"
#
# ]
#
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["GET", "POST", "PUT", "DELETE"],
#     allow_headers=["*"],
# )

router = APIRouter()

# @router.post('/img', status_code=status.HTTP_201_CREATED)
# async def post_image(medicamento: MedicamentoSchema, file: UploadFile = File(...)):
#     file.filename = f"{medicamento.nome}.jpg"
#     contents = await file.read()
#     # save the file
#     with open(f"{IMAGEDIR}{file.filename}", "wb") as f:
#         f.write(contents)
#
#     return {"filename": file.filename}
#
#
# @router.get("/show")
# async def read_random_file():
#     # get random file from the image directory
#     files = os.listdir(IMAGEDIR)
#     random_index = randint(0, len(files) - 1)
#
#     path = f"{IMAGEDIR}{files[random_index]}"
#
#     return FileResponse(path)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=MedicamentoSchema)
async def post_medicamento(nome: str,
    preco: float,
    data_de_validade: str,
    imagem: UploadFile = File(...), db: AsyncSession = Depends(get_session)):
    # criar img
    imagem.filename = f"{nome}.jpg"
    contents = await imagem.read()

    # salvar
    with open(f"{IMAGEDIR}{imagem.filename}", "wb") as f:
        f.write(contents)
        image_url = f"http://localhost:8000/api/medicamentos/images/{imagem.filename}"

    novo_medicamento = MedicamentoModel(
        nome=nome,
        preco=preco,
        data_de_validade=data_de_validade,
        imagem=image_url)

    db.add(novo_medicamento)
    await db.commit()
    return novo_medicamento


@router.get('/', response_model=List[MedicamentoSchema])
async def get_medicamentos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(MedicamentoModel)
        result = await  session.execute(query)
        medicamentos: List[MedicamentoModel] = result.scalars().all()

        return medicamentos



# @router.get('/', response_model=List[MedicamentoSchema])
# async def get_medicamentos(nome: Optional[str] = None, db: AsyncSession = Depends(get_session)):
#     async with db as session:
#         query = select(MedicamentoModel)
#         if nome:
#             query = query.filter(MedicamentoModel.nome.ilike(f'%{nome}%'))
#         result = await session.execute(query)
#         medicamentos: List[MedicamentoModel] = result.scalars().all()
#
#         return medicamentos



@router.get("/images/{image_filename}")
async def get_image(image_filename: str):
    image_path = os.path.join(IMAGEDIR, image_filename)
    return FileResponse(image_path)



@router.get('/{medicamento_id}', response_model=MedicamentoSchema, status_code=status.HTTP_200_OK)
async def get_medicamento(medicamento_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(MedicamentoModel).filter(MedicamentoModel.id == medicamento_id)
        result = await session.execute(query)
        medicamento = result.scalar_one_or_none()

        if medicamento:
            return medicamento
        else:
            raise HTTPException(detail='Medicamento não encontrado.', status_code=status.HTTP_404_NOT_FOUND)











@router.put('/{medicamento_id}', response_model=MedicamentoSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_medicamento(medicamento_id: int, medicamento: MedicamentoSchema, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(MedicamentoModel).filter(MedicamentoModel.id == medicamento_id)
        result = await session.execute(query)
        medicamento_up = result.scalar_one_or_none()

        if medicamento_up:
            medicamento_up.nome = medicamento.nome
            medicamento_up.preco = medicamento.preco
            medicamento_up.data_de_validade = medicamento.data_de_validade
            medicamento_up.imagem = medicamento.imagem

            await session.commit()

            return medicamento_up
        else:
            raise HTTPException(detail='Medicamento não encontrado.', status_code=status.HTTP_404_NOT_FOUND)






@router.delete('/{medicamento_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_medicamento(medicamento_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(MedicamentoModel).filter(MedicamentoModel.id == medicamento_id)
        result = await session.execute(query)
        medicamento_delete = result.scalar_one_or_none()

        if medicamento_delete:
            await session.delete(medicamento_delete)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Medicamento não encontrado.', status_code=status.HTTP_404_NOT_FOUND)
