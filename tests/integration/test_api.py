import pytest
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_test_db

# Configuración de la base de datos en memoria para pruebas
SQLALCHEMY_DATABASE_URL_TEST = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL_TEST, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear la base de datos de pruebas
Base.metadata.create_all(bind=engine)

# Sobrescribir la dependencia de la base de datos para usar la base de datos de pruebas
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_test_db] = override_get_db

@pytest.fixture(scope="module")
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    # Configuración antes de las pruebas
    Base.metadata.create_all(bind=engine)
    yield
    # Teardown después de las pruebas
    Base.metadata.drop_all(bind=engine)

@pytest.mark.asyncio
async def test_create_vehicle(async_client):
    response = await async_client.post(
        "/api/v1/vehicles/",
        json={"license_plate": "ABC123", "model": "Truck", "year": 2010, "current_mileage": 100000.0},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["license_plate"] == "ABC123"
    assert data["model"] == "Truck"
    assert data["year"] == 2010
    assert data["current_mileage"] == 100000.0
    assert "id" in data

@pytest.mark.asyncio
async def test_get_vehicles(async_client):
    response = await async_client.get("/api/v1/vehicles/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["license_plate"] == "ABC123"

@pytest.mark.asyncio
def test_create_service_order(client):
    response = client.post("/api/v1/service_orders/", json={
        "description": "Test",
        "date": "2024-05-21T00:00:00",
        "cost": 100.0,
        "vehicle_id": None
    })
    assert response.status_code == 200
    data = response.json()
    assert data["id"] is not None
    assert data["description"] == "Test"

def test_get_service_orders(client):
    response = client.get("/api/v1/service_orders/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

def test_get_service_order(client):
    response = client.get("/api/v1/service_orders/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1

def test_update_service_order(client):
    response = client.put("/api/v1/service_orders/1", json={
        "description": "Updated",
        "date": "2024-05-21T00:00:00",
        "cost": 150.0,
        "vehicle_id": None
    })
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Updated"

def test_delete_service_order(client):
    response = client.delete("/api/v1/service_orders/1")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Service order deleted successfully"

    response = client.get("/api/v1/service_orders/1")
    assert response.status_code == 404
