from typing import Optional
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt
from models.usuario_model import UsuarioModel
from core.configs import settings
from core.security import verificar_senha
from pytz import timezone


oauth2_schema = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_STR}/usuario/login"
)


async def autenticar(email: str, password: str, db: AsyncSession) -> Optional[UsuarioModel]:
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.email == email)
        result = await session.execute(query)
        usuario: UsuarioModel = result.scalars().unique().one_or_none()

        if not usuario:
            return None

        if not verificar_senha(password, usuario.password):
            return None

    return usuario


def criar_token(token_type: str, tempo_vida: timedelta, sub: str) -> str:
    sp = timezone('America/Sao_Paulo')
    expira = datetime.now(tz=sp) + tempo_vida
    payload = {
        "type": token_type,
        "exp": expira,
        "iat": datetime.now(tz=sp),
        "sub": str(sub),
    }

    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)


def criar_token_acesso(sub: str) -> str:
    return criar_token(
        token_type='access_token',
        tempo_vida=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub
    )


def criar_refresh_token(sub: str) -> str:
    return criar_token(
        token_type='refresh_token',
        tempo_vida=timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        sub=sub
    )
