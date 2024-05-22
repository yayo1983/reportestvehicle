from app.presenters.vehicle_presenter import VehiclePresenter
from app.schemas import VehicleCreate


def test_create_vehicle(db):
    presenter = VehiclePresenter(db)
    vehicle_data = VehicleCreate(
        license_plate="ABC123",
        model="Truck",
        year=2010,
        current_mileage=100000.0,
        
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
