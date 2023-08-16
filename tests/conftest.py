from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest
from customers.config import settings
from customers.main import app 
from customers.database import get_db
from customers import models
from customers import schemas

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency
@pytest.fixture()
def session():
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def overrride_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = overrride_get_db
    yield TestClient(app)


test = {"email": "dinesh@gmail.com" , "password" : "password123"}
@pytest.fixture()
def test_create_testuser(client):
    res = client.post("/users", json=test)
    user = schemas.UsersResponse(**res.json())
    test_user = res.json()
    assert res.status_code == 201
    test_user['password']=test['password']
    return test_user


test_users=[{ "payload" : {"email": "dinesh@gmail.com" , "password" : "password123"}, "response_code": 201},
            { "payload" : {"email": "ramesh@gmail.com" , "password" : "password123"}, "response_code": 201}
           ]           
@pytest.fixture()
def test_create_testusers(client):
    for test_user in test_users:
        res = client.post("/users", json=test_user["payload"])
        user = schemas.UsersResponse(**res.json())
        new_user = res.json()
        assert res.status_code == test_user["response_code"]
        new_user['password']=test_user["payload"]["password"]
        return new_user
