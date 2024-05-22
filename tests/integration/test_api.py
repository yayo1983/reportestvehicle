import pytest
import asyncio
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
async def test_create_service_order(async_client):
    response = await async_client.post(
        "/api/v1/vehicles/",
        json={"license_plate": "XYZ789", "model": "Car", "year": 2015, "current_mileage": 50000.0},
    )
    vehicle_id = response.json()["id"]

    service_order_response = await async_client.post(
        f"/api/v1/vehicles/{vehicle_id}/service_orders/",
        json={"description": "Oil change", "date": "2024-05-21T10:00:00", "cost": 200.0},
    )
    assert service_order_response.status_code == 200
    service_order_data = service_order_response.json()
    assert service_order_data["description"] == "Oil change"
    assert service_order_data["date"] == "2024-05-21T10:00:00"
    assert service_order_data["cost"] == 200.0
    assert "id" in service_order_data
    assert service_order_data["vehicle_id"] == vehicle_id

@pytest.mark.asyncio
async def test_get_service_order(async_client):
    response = await async_client.post(
        "/api/v1/vehicles/",
        json={"license_plate": "DEF456", "model": "Van", "year": 2020, "current_mileage": 30000.0},
    )
    vehicle_id = response.json()["id"]

    service_order_response = await async_client.post(
        f"/api/v1/vehicles/{vehicle_id}/service_orders/",
        json={"description": "Tire replacement", "date": "2024-05-21T12:00:00", "cost": 300.0},
    )
    service_order_id = service_order_response.json()["id"]

    response = await async_client.get(f"/api/v1/service_orders/{service_order_id}")
    assert response.status_code == 200
    service_order_data = response.json()
    assert service_order_data["description"] == "Tire replacement"
    assert service_order_data["date"] == "2024
