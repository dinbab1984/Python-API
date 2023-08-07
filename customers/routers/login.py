from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from typing import List
from sqlalchemy.orm import Session
from .. import models, schemas, auth
from ..database import get_db, engine
from ..utils import hash

models.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/login"
    , tags=["login"]
    )

@router.post("/", response_model=schemas.Token)
def login(user_credentials : OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials")
    if not hash.verify(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials")
    token = auth.generate_access_token({"id" : user.id})
    return token




