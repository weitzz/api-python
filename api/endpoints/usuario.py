# from pathlib import Path
from typing import List

import sqlalchemy.exc
from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.auth import autenticar, criar_token_acesso, verificar_email, criar_refresh_token, update_refresh_token
from core.deps import get_session, get_current_user
from core.security import gerar_hash_senha
from models.usuario_model import UsuarioModel
from schemas.usuario_schema import UsuarioSchemaBase, UsuarioSchemaCreate, UsuarioSchemaUpdate

router = APIRouter()


@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=UsuarioSchemaBase)
async def post_usuario(usuario: UsuarioSchemaCreate, db: AsyncSession = Depends(get_session)):
    if await verificar_email(usuario.email, db):
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="E-mail já cadastrado"
        )

    novo_usuario: UsuarioModel = UsuarioModel(
        nome=usuario.nome,
        email=usuario.email,
        password=gerar_hash_senha(usuario.password)
    )

    async with db as session:
        try:
            session.add(novo_usuario)
            await session.commit()
            return novo_usuario
        except sqlalchemy.exc.IntegrityError as e:
            await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro no servidor: {str(e)}"
        )


@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    usuario = await autenticar(email=form_data.username, password=form_data.password, db=db)

    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )


    token_data = {
        "access_token": criar_token_acesso(sub=usuario.id),
        "refresh_token": criar_refresh_token(sub=usuario.id),
        "token_type": "bearer",
        "name": usuario.nome,
        "email": usuario.email
    }
    await update_refresh_token(db, usuario.id, token_data["refresh_token"])

    return JSONResponse(
        content=token_data,
        status_code=status.HTTP_200_OK)


@router.post("/refresh-token", status_code=status.HTTP_200_OK)
async def refresh_access_token(usuario: dict = Depends(get_current_user)):
    return criar_refresh_token(sub=usuario.id)


@router.get('/', response_model=List[UsuarioSchemaBase])
async def get_usuarios(current_user: UsuarioModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel)
        result = await session.execute(query)
        usuarios: List[UsuarioSchemaBase] = result.scalars().unique().all()

        return usuarios


@router.get('/{usuario_id}', response_model=UsuarioSchemaBase, status_code=status.HTTP_200_OK)
async def get_usuario(usuario_id: int, current_user: UsuarioModel = Depends(get_current_user),
                      db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario: UsuarioSchemaBase = result.scalars().unique().one_or_none()

        if usuario:
            return usuario
        else:
            raise HTTPException(detail='Usuário não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)


@router.put('/{usuario_id}', response_model=UsuarioSchemaBase, status_code=status.HTTP_202_ACCEPTED)
async def put_usuario(usuario_id: int, usuario: UsuarioSchemaUpdate, db: AsyncSession = Depends(get_session)):

    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario_up: UsuarioSchemaBase = result.scalars().unique().one_or_none()

        if usuario_up:
            if usuario.nome:
                usuario_up.nome = usuario.nome
            if usuario.email:
                usuario_up.email = usuario.email
            if usuario.password:
                usuario_up.password = gerar_hash_senha(usuario.password)

            await session.commit()
            return usuario_up
        else:
            raise HTTPException(detail='Usuário não encontrado', status_code=status.HTTP_404_NOT_FOUND)


@router.delete('/{usuario_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario(usuario_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario_delete: UsuarioSchemaBase = result.scalars().unique().one_or_none()

        if usuario_delete:
            await session.delete(usuario_delete)
            await session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Usuário não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)
