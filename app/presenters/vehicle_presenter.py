from sqlalchemy.orm import Session
from app import models, schemas

class VehiclePresenter:
    def __init__(self, db: Session):
        self.db = db

    def create_vehicle(self, vehicle: schemas.VehicleCreate) -> models.Vehicle:
        db_vehicle = models.Vehicle(**vehicle.dict())
        self.db.add(db_vehicle)
        self.db.commit()
        self.db.refresh(db_vehicle)
        return db_vehicle

    def get_vehicles(self) -> list[models.Vehicle]:
        return self.db.query(models.Vehicle).all()
