import json
from jose import jwt
import pytest
from app import schemas
# from .database import client, session
from app.config import setting

# @pytest.fixture
# def test_user(client):
#     user_data = {"email": "raavi@gmail.com",
#                 "password":"123"}
#     res = client.post("/users/", json=user_data)

#     assert res.status_code == 201
#     new_user = res.json()
#     new_user['password'] = user_data["password"]
#     return new_user


def test_root(client):
    res = client.get("/")
    print(res.json().get('message'))

def test_create_user(client):
    res = client.post("/users/", json={"email":"raavi@gmail.com", "password":"123"})

    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "raavi@gmail.com"
    assert res.status_code == 201

def test_login_user(client, test_user):
    res = client.post("/login", data={"username":test_user["email"], "password":test_user["password"]})
    login_res = schemas.Token(**res.json())

    payload = jwt.decode(login_res.access_token, setting.secret_key, algorithms=[setting.algoritham])
    id = payload.get("user_id")

    assert id == test_user['id']
    assert login_res.token_type == 'bearer'
    assert res.status_code == 200