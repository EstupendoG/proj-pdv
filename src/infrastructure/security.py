from passlib.context import CryptContext

_contexto = CryptContext(schemes=["bcrypt"], deprecated="auto")


def criar_hash_senha(senha: str) -> str:
    return _contexto.hash(senha)


def verificar_senha(senha: str, hash: str) -> bool:
    return _contexto.verify(senha, hash)
