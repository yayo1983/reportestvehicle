from sqlalchemy.orm import Session

from . import models
from . import schemas

def get_vehicle(db: Session, vehicle_id: int):
    return db.query(models.Vehicle).filter(models.Vehicle.id == vehicle_id).first()

def get_vehicles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Vehicle).offset(skip).limit(limit).all()

def create_vehicle(db: Session, vehicle: schemas.VehicleCreate):
    db_vehicle = models.Vehicle(**vehicle.dict())
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

def get_service_order(db: Session, service_order_id: int):
    return db.query(models.ServiceOrder).filter(models.ServiceOrder.id == service_order_id).first()

def create_service_order(db: Session, service_order: schemas.ServiceOrderCreate, vehicle_id: int):
    db_service_order = models.ServiceOrder(**service_order.dict(), vehicle_id=vehicle_id)
    db.add(db_service_order)
    db.commit()
    db.refresh(db_service_order)
    return db_service_order
