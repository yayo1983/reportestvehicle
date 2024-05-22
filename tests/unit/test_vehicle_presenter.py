import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Vehicle
from app.presenters.vehicle_presenter import VehiclePresenter
from app.schemas import VehicleCreate

# Configuración de la base de datos en memoria para pruebas
SQLALCHEMY_DATABASE_URL_TEST = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL_TEST, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
    Base.metadata.drop_all(bind=engine)

def test_create_vehicle(db):
    presenter = VehiclePresenter(db)
    vehicle_data = VehicleCreate(
        license_plate="ABC123",
        model="Truck",
        year=2010,
        current_mileage=100000.0
    )
    vehicle = presenter.create_vehicle(vehicle_data)
    assert vehicle.license_plate == "ABC123"
    assert vehicle.model == "Truck"
    assert vehicle.year == 2010
    assert vehicle.current_mileage == 100000.0

def test_get_vehicles(db):
    presenter = VehiclePresenter(db)
    vehicle_data = VehicleCreate(
        license_plate="ABC123",
        model="Truck",
        year=2010,
        current_mileage=100000.0
    )
    presenter.create_vehicle(vehicle_data)
    vehicles = presenter.get_vehicles()
    assert len(vehicles) == 1
    assert vehicles[0].license_plate == "ABC123"
