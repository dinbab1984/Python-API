from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import  status, HTTPException, Depends
from .schemas import Token
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = settings.jwt_secret_key
ALGORITHM = settings.jwt_algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.jwt_access_token_expire_minutes

def generate_access_token(payload: dict):
    to_encode = payload.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    Token.access_token = encoded_jwt
    Token.token_type = "bearer"
    return Token

def verify_access_token(token : str, credentials_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id : str = payload.get("id")
        if id == None :
            raise credentials_exception
        token_data = id
    except JWTError:
        raise credentials_exception
    return token_data

def get_current_user(token : str = Depends (oauth2_scheme)):
    credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_access_token(token,credentials_exception)
    





