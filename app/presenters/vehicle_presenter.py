from sqlalchemy.orm import Session
from app.models import Vehicle
from app.schemas import VehicleCreate, VehicleRead

class VehiclePresenter:

    def __init__(self, db: Session):
        self.db = db

    def create_vehicle(self, vehicle: VehicleCreate) -> VehicleRead:
        db_vehicle = Vehicle(**vehicle.model_dump())
        self.db.add(db_vehicle)
        self.db.commit()
        self.db.refresh(db_vehicle)
        return db_vehicle

    def get_vehicles(self, skip: int = 0, limit: int = 10):
        vehicles = self.db.query(Vehicle).offset(skip).limit(limit).all()
        return [vehicle for vehicle in vehicles]
