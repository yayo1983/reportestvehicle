import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app

# Configurar base de datos de pruebas
SQLALCHEMY_DATABASE_URL_TEST = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL_TEST, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear base de datos de pruebas
Base.metadata.create_all(bind=engine)

# Depender de la base de datos de pruebas en lugar de la base de datos real
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# Función para limpiar la base de datos después de cada prueba
@pytest.fixture(autouse=True)
def clear_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def test_create_vehicle():
    response = client.post(
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

def test_get_vehicles():
    # Crear un vehículo
    client.post(
        "/api/v1/vehicles/",
        json={"license_plate": "ABC123", "model": "Truck", "year": 2010, "current_mileage": 100000.0},
    )
    response = client.get("/api/v1/vehicles/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["license_plate"] == "ABC123"

def test_create_service_order():
    # Crear un vehículo
    vehicle_response = client.post(
        "/api/v1/vehicles/",
        json={"license_plate": "ABC123", "model": "Truck", "year": 2010, "current_mileage": 100000.0},
    )
    vehicle_id = vehicle_response.json()["id"]

    # Crear una orden de servicio
    service_order_response = client.post(
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

def test_get_service_order():
    # Crear un vehículo
    vehicle_response = client.post(
        "/api/v1/vehicles/",
        json={"license_plate": "ABC123", "model": "Truck", "year": 2010, "current_mileage": 100000.0},
    )
    vehicle_id = vehicle_response.json()["id"]

    # Crear una orden de servicio
    service_order_response = client.post(
        f"/api/v1/vehicles/{vehicle_id}/service_orders/",
        json={"description": "Oil change", "date": "2024-05-21T10:00:00", "cost": 200.0},
    )
    service_order_id = service_order_response.json()["id"]

    # Obtener la orden de servicio
    response = client.get(f"/api/v1/service_orders/{service_order_id}")
    assert response.status_code == 200
    service_order_data = response.json()
    assert service_order_data["description"] == "Oil change"
    assert service_order_data["date"] == "2024-05-21T10:00:00"
    assert service_order_data["cost"] == 200.0
    assert service_order_data["id"] == service_order_id
    assert service_order_data["vehicle_id"] == vehicle_id
