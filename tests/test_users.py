import pytest
from typing import List
from customers import schemas


def test_root(client):
    res = client.get("/")
    # print(res.json().get("message"))
    assert res.json().get("message") == "Hello World!"
    assert res.status_code == 200

def test_create_user(client, test_create_testuser):
    assert test_create_testuser

def test_get_all_users(client,test_create_testusers):
    res = client.get("/users")
    for test_user in res.json():
        user = schemas.UsersResponse(**test_user)
    assert res.status_code == 200

def test_recreate_user(client, test_create_testuser):
    res = client.post("/users",json=test_create_testuser)
    assert res.status_code == 409

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

def test_login_user(client,test_create_testusers):
    # print(test_create_testuser)
    res = client.post("/login",data={"username": test_create_testusers["email"] , "password" : test_create_testusers["password"]})
    assert res.status_code == 200
    


