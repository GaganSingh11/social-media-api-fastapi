from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.main import app

from app.config import setting
from app.database import get_db
from app.database import Base

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:gagan@localhost:5433/fastapi_test'
# SQLALCHEMY_DATABASE_URL = f'postgresql://{setting.database_username}:{setting.database_password}@{setting.database_hostname}:{setting.database_port}/{setting.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind = engine)



@pytest.fixture()
def session():
    Base.metadata.drop_all(bind = engine)
    Base.metadata.create_all(bind = engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    # Dependency
    def overrid_get_db():
        try:
            yield session
        finally:
            session.close()

    # Swap development database with test database
    app.dependency_overrides[get_db] = overrid_get_db
    yield TestClient(app)

@pytest.fixture
def test_user(client):
    user_data = {"email": "raavi@gmail.com",
                "password":"123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data["password"]
    return new_user