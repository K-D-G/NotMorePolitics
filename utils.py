from constants import*
from singletons import*

def hash_password(pwd):
    return FlaskPasswordHasher.get().generate_password_hash(pwd, BCRYPT_ROUNDS)

def check_password(password, hashed_password):
    return FlaskPasswordHasher.get().check_password_hash(hashed_password, password)
