from passlib.hash import pbkdf2_sha256


def hash(password):
    hashed = pbkdf2_sha256.encrypt(password, rounds=10000, salt_size=16)
    return hashed


def verify(password, hash):
    return pbkdf2_sha256.verify(password, hash)
