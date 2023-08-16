from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest
from customers.config import settings
from customers.main import app 
from customers.database import get_db
from customers import models
from customers import schemas
from typing import List

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency
def overrride_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = overrride_get_db

@pytest.fixture()
def client():
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    yield TestClient(app)

def test_root(client):
    res = client.get("/")
    # print(res.json().get("message"))
    assert res.json().get("message") == "Hello World!"
    assert res.status_code == 200

@pytest.mark.parametrize("payload, response_code",[
    ({"email": "dinesh@gmail.com" , "password" : "password123"},201),
    ({"email": "ramesh@gmail.com" , "password" : "password123"},201)
])
def test_create_user(client, payload, response_code):
    res = client.post("/users", json=payload)
    user = schemas.UsersResponse(**res.json())
    assert res.status_code == response_code
    res = client.post("/users", json=payload)
    assert res.status_code == 409
    # res = client.get("/users")
    # print(res.json())
    # assert res.status_code == 200

@pytest.mark.parametrize("payload, reponse_code",[
    ({"email": "dinesh@gmail" , "password" : "password123"},422),
    ({"email": "dinesh.com" , "password" : "password123"},422),
    ({"email": "@gmail.com" , "password" : "password123"},422),
    ({"email": None , "password" : "password123"},422),
    ({"email": "dinesh@gmail.com" , "password" : None},422)
])

def test_incorrect_user(client,payload,reponse_code):
    res = client.post("/users", json=payload)
    assert res.status_code == reponse_code