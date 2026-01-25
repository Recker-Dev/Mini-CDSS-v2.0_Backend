from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher()


def create_hash(password: str) -> str:
    return ph.hash(password)


def verify_hash(hash: str, password: str) -> bool:
    try:
        return ph.verify(hash, password)
        
    except VerifyMismatchError:
        return False

