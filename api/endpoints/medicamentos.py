import shutil
from pathlib import Path
from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.medicamento_model import MedicamentoModel
from schemas.medicamento_schema import MedicamentoSchema
from core.deps import get_session

router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=MedicamentoSchema)
async def post_medicamento(medicamento: MedicamentoSchema, db: AsyncSession = Depends(get_session)):
    novo_medicamento = MedicamentoModel(nome=medicamento.nome, preco=medicamento.preco,
                                        data_de_validade=medicamento.data_de_validade, imagem=medicamento.imagem)

    db.add(novo_medicamento)
    await db.commit()

    return novo_medicamento


@router.get('/', response_model=List[MedicamentoSchema])
async def get_medicamentos(db: AsyncSession = Depends(get_session)):
    async  with db as session:
        query = select(MedicamentoModel)
        result = await  session.execute(query)
        medicamentos = List[MedicamentoModel] = result.scalars().all()

        return medicamentos


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


@router.get('/', response_model=List[MedicamentoSchema])
async def get_medicamentos(nome: Optional[str] = None, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(MedicamentoModel)
        if nome:
            query = query.filter(MedicamentoModel.nome.ilike(f'%{nome}%'))
        result = await session.execute(query)
        medicamentos = List[MedicamentoModel] = result.scalars().all()

        return medicamentos


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


@router.post('/uploadImage', status_code=status.HTTP_201_CREATED, response_model=MedicamentoSchema)
async def upload_image(medicamento: MedicamentoSchema, db: AsyncSession = Depends(get_session)):
    try:
        db.add(medicamento)
        await db.commit()
        db.refresh()
        return {"message": "Passo 1 concluído com sucesso"}
    except Exception as e:
        raise HTTPException(detail='Imagem do medicamento não encontrado.',
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get('/getImage', response_model=MedicamentoSchema)
async def get_image(file: UploadFile = File(...), db: AsyncSession = Depends(get_session)):
    try:
        return {"message": "Passo 2 concluído com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='Imagem do medicamento não encontrado.')
