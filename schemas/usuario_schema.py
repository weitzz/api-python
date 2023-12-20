from typing import Optional

from pydantic import BaseModel as SCBaseModel, EmailStr


class UsuarioSchemaBase(SCBaseModel):
    id: Optional[int]
    nome: str
    email: EmailStr

    class Config:
        orm_mode = True


class UsuarioSchemaCreate(UsuarioSchemaBase):
    password: str


class UsuarioSchemaUpdate(UsuarioSchemaBase):
     nome: Optional[str]
     email: Optional[EmailStr]
     password: Optional[str]


