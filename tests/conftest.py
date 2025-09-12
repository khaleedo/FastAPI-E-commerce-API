import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_db, Base
from main import app

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session")
def db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db):
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def admin_token(client):
    # Create admin user
    admin_data = {
        "email": "admin@example.com",
        "username": "admin",
        "full_name": "Admin User",
        "password": "adminpass",
        "role": "admin"
    }
    client.post("/auth/register", json=admin_data)
    
    # Login
    login_data = {"username": "admin", "password": "adminpass"}
    response = client.post("/auth/login", data=login_data)
    return response.json()["access_token"]


@pytest.fixture
def customer_token(client):
    # Create customer user
    customer_data = {
        "email": "customer@example.com",
        "username": "customer",
        "full_name": "Customer User",
        "password": "customerpass"
    }
    client.post("/auth/register", json=customer_data)
    
    # Login
    login_data = {"username": "customer", "password": "customerpass"}
    response = client.post("/auth/login", data=login_data)
    return response.json()["access_token"]