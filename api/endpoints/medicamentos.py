import os
import pathlib
from PIL import Image
from io import BytesIO
from typing import List, Optional
from fastapi_pagination import Page, add_pagination, paginate

from fastapi import APIRouter, status, Depends, HTTPException, Response, UploadFile, File, Form
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from core.deps import get_session
from models.medicamento_model import MedicamentoModel
from schemas.medicamento_schema import MedicamentoSchema, MedicamentoUpdateSchema

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
                           quantidade: float = Form(),
                           imagem: UploadFile = File(...), db: AsyncSession = Depends(get_session)):
    try:
        extensao = os.path.splitext(imagem.filename)[1].lower()
        allowed_extensions = {'.png', '.jpg', '.jpeg', '.gif'}

        if extensao not in allowed_extensions:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Extensão de imagem não suportada")

        arquivo_imagem = f"{nome}{extensao}"
        contents = await imagem.read()

        # Salvar a imagem no caminho correto
        image_path = os.path.join(IMAGEDIR, arquivo_imagem)
        save_image(contents, image_path)
        # Salvar a imagem no caminho correto

        image_url = f"http://localhost:8000/api/medicamentos/images/{os.path.basename(image_path)}"

        novo_medicamento = MedicamentoModel(
            nome=nome,
            preco=preco,
            data_de_validade=data_de_validade,
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
async def get_medicamentos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(MedicamentoModel)
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
        query = select(MedicamentoModel).filter(
            MedicamentoModel.id == medicamento_id)
        result = await session.execute(query)
        medicamento = result.scalar_one_or_none()

        if medicamento:
            return medicamento
        else:
            raise HTTPException(
                detail='Medicamento não encontrado.', status_code=status.HTTP_404_NOT_FOUND)


@router.get('/{name}', response_model=MedicamentoSchema, status_code=status.HTTP_200_OK)
async def get_name_medicamento(name: str, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(MedicamentoModel).filter(MedicamentoModel.nome == name)
        result = await session.execute(query)
        medicamento = result.scalar_one_or_none()

        if medicamento:
            return medicamento
        else:
            raise HTTPException(
                detail='Medicamento não encontrado.', status_code=status.HTTP_404_NOT_FOUND)


@router.put('/{medicamento_id}', response_model=MedicamentoUpdateSchema)
async def put_medicamento(
        medicamento_id: int,
        nome: str = Form(),
        preco: float = Form(),
        data_de_validade: str = Form(),
        quantidade: float = Form(),
        imagem: UploadFile = File(...),
        db: AsyncSession = Depends(get_session)
):
    try:
        async with db as session:
            # Verifica se o medicamento existe no banco de dados
            query = select(MedicamentoModel).filter(
                MedicamentoModel.id == medicamento_id)
            medicamento_existente = await session.execute(query)
            medicamento_existente = medicamento_existente.scalar_one_or_none()

            if not medicamento_existente:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Medicamento não encontrado"
                )

            # Atualiza os campos do medicamento com os valores fornecidos
            medicamento_existente.nome = nome
            medicamento_existente.preco = preco
            medicamento_existente.data_de_validade = data_de_validade
            medicamento_existente.quantidade = quantidade

            # Salva a nova imagem (caso seja fornecida)
            if imagem:
                extensao = os.path.splitext(imagem.filename)[1].lower()
                allowed_extensions = {'.png', '.jpg', '.jpeg', '.gif'}

                if extensao not in allowed_extensions:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Extensão de imagem não suportada"
                    )

                arquivo_imagem = f"{nome}{extensao}"
                contents = await imagem.read()

                # Salvar a imagem no caminho correto
                image_path = os.path.join(IMAGEDIR, arquivo_imagem)
                save_image(contents, image_path)

                medicamento_existente.imagem = f"http://localhost:8000/api/medicamentos/images/{os.path.basename(image_path)}"

            await session.commit()

            return medicamento_existente

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao processar a solicitação: {str(e)}"
        )


@router.delete('/{medicamento_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_medicamento(medicamento_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(MedicamentoModel).filter(
            MedicamentoModel.id == medicamento_id)
        result = await session.execute(query)
        medicamento_delete = result.scalar_one_or_none()

        if medicamento_delete:
            await session.delete(medicamento_delete)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(
                detail='Medicamento não encontrado.', status_code=status.HTTP_404_NOT_FOUND)


@router.get('/paginate/default', response_model=Page[MedicamentoSchema])
async def pagination_medicamentos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(MedicamentoModel)
        result = await session.execute(query)
        medicamentos: List[MedicamentoModel] = result.scalars().all()

        return paginate(medicamentos)


add_pagination(router)
