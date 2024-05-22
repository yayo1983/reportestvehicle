from sqlalchemy.orm import Session
from app.models import Vehicle
from app.schemas import VehicleCreate, VehicleRead
from sqlalchemy.exc import SQLAlchemyError


class VehiclePresenter:

    def __init__(self, db: Session):
        self.db = db

    def create_vehicle(self, vehicle: VehicleCreate) -> VehicleRead:
        try:
            db_vehicle = Vehicle(**vehicle.model_dump())
            self.db.add(db_vehicle)
            self.db.commit()
            self.db.refresh(db_vehicle)
            return db_vehicle
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e  # Re-raise the exception for further handling

    def get_vehicles(self, skip: int = 0, limit: int = 10):
        try:
            vehicles = self.db.query(Vehicle).offset(skip).limit(limit).all()
            return [vehicle for vehicle in vehicles]
        except SQLAlchemyError as e:
            raise e  # Re-raise the exception for further handling
