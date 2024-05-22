import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Vehicle, ServiceOrder
from app.presenters.service_order_presenter import ServiceOrderPresenter
from app.schemas import ServiceOrderCreate

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

def test_create_service_order(db):
    # Crear vehículo para la prueba
    vehicle = Vehicle(license_plate="XYZ789", model="Car", year=2015, current_mileage=50000.0)
    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)

    presenter = ServiceOrderPresenter(db)
    service_order_data = ServiceOrderCreate(
        description="Oil change",
        date="2024-05-21T10:00:00",
        cost=200.0
    )
    service_order = presenter.create_service_order(vehicle.id, service_order_data)
    assert service_order.description == "Oil change"
    assert service_order.date == "2024-05-21T10:00:00"
    assert service_order.cost == 200.0
    assert service_order.vehicle_id == vehicle.id

def test_get_service_orders(db):
    # Crear vehículo para la prueba
    vehicle = Vehicle(license_plate="XYZ789", model="Car", year=2015, current_mileage=50000.0)
    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)

    presenter = ServiceOrderPresenter(db)
    service_order_data = ServiceOrderCreate(
        description="Oil change",
        date="2024-05-21T10:00:00",
        cost=200.0
    )
    presenter.create_service_order(vehicle.id, service_order_data)
    service_orders = presenter.get_service_orders()
    assert len(service_orders) == 1
    assert service_orders[0].description == "Oil change"
