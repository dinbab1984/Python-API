from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

def hashed_value(value : str):
    hashed_value = pwd_context.hash(value)
    return hashed_value

def verify(value: str , hash : str):
    return pwd_context.verify(value,hash)
     