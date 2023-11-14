import os
import pathlib
import shutil
import uuid
from pathlib import Path
from typing import List, Optional, Annotated
from fastapi import APIRouter, status, Depends, HTTPException, Response, UploadFile, File, Form

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi.responses import FileResponse
from PIL import Image
from models.medicamento_model import MedicamentoModel
from schemas.medicamento_schema import MedicamentoSchema
from core.deps import get_session
from fastapi.staticfiles import StaticFiles

IMAGEDIR = "images/"
uploads_dir = pathlib.Path(os.getcwd(), IMAGEDIR)

router = APIRouter()
router.mount("/images", StaticFiles(directory="images"), name="images")


def save_image(contents, file_path):
    with open(file_path, "wb") as f:
        f.write(contents)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=MedicamentoSchema)
async def post_medicamento(nome: str = Form(),
                           preco: float = Form(),
                           data_de_validade: str = Form(),
                           estoque: bool = Form(),
                           quantidade: str = Form(),
                           imagem: UploadFile = File(...), db: AsyncSession = Depends(get_session)):
    try:
        extensao = os.path.splitext(imagem.filename)[1].lower()
        allowed_extensions = {'.png', '.jpg', '.jpeg', '.gif'}

        if extensao not in allowed_extensions:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Extensão de imagem não suportada")

        arquivo_imagem = f"{nome}{extensao}"
        contents = await imagem.read()

        # Salvar a imagem no caminho correto
        image_path = os.path.join(IMAGEDIR, arquivo_imagem)
        save_image(contents, image_path)

        # Verificar e converter para JPEG, se necessário
        # image_path = convert_to_jpeg(image_path)

        image_url = f"http://localhost:8000/api/medicamentos/images/{os.path.basename(image_path)}"

        novo_medicamento = MedicamentoModel(
            nome=nome,
            preco=preco,
            data_de_validade=data_de_validade,
            estoque=estoque,
            quantidade=quantidade,
            imagem=image_url
        )

        db.add(novo_medicamento)
        await db.commit()
        return novo_medicamento
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Erro ao processar a solicitação: {str(e)}")


@router.get('/', response_model=List[MedicamentoSchema])
async def get_medicamentos(nome: Optional[str] = None, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(MedicamentoModel)
        if nome:
            query = query.filter(MedicamentoModel.nome.ilike(f'%{nome}%'))
        result = await session.execute(query)
        medicamentos: List[MedicamentoModel] = result.scalars().all()

        return medicamentos


@router.get("/images/{image_filename}")
async def get_image(image_filename: str):
    image_path = os.path.join(IMAGEDIR, image_filename)
    if not os.path.isfile(image_path):
        raise HTTPException(status_code=404, detail="Imagem não encontrada")

    name, ext = os.path.splitext(image_filename)

    image_path_without_extension = os.path.join(IMAGEDIR, name + ext)

    return FileResponse(image_path_without_extension)


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
