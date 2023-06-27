from passlib.hash import pbkdf2_sha256


def hash(password: str) -> str:
    return pbkdf2_sha256.encrypt(password, rounds=10000, salt_size=16)  # type: ignore


def verify(password: str, hash: str) -> bool:
    return pbkdf2_sha256.verify(password, hash)  # type: ignore
