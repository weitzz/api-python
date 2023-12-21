from typing import Optional

from pydantic import BaseModel as SCBaseModel, EmailStr, Field, validator


class UsuarioSchemaBase(SCBaseModel):
    id: Optional[int]
    nome: str
    email: EmailStr

    class Config:
        orm_mode = True


class UsuarioSchemaCreate(UsuarioSchemaBase):
    password: str = Field(..., min_length=8, max_length=20, description="A senha deve conter no mínimo 8 caracteres")


class UsuarioSchemaUpdate(UsuarioSchemaBase):
    nome: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]


@validator("password")
def password_length(cls, value):
    if len(value) < 8:
        raise ValueError("A senha deve ter no mínimo 8 caracteres")
    return value


# {
#   "id": 0,
#   "nome": "teste refresh token",
#   "email": "user@example.com",
#   "password": "123123123"
# }