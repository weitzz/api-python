from passlib.context import CryptContext

CRIPTO = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verificar_senha(password: str, hash_senha: str) -> bool:

    return CRIPTO.verify(password, hash_senha)


def gerar_hash_senha(password: str) -> str:
    return CRIPTO.hash(password)
