from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import schemas, database
from app.presenters.vehicle_presenter import VehiclePresenter

router = APIRouter()

@router.post("/vehicles/", response_model=schemas.Vehicle)
def create_vehicle(vehicle: schemas.VehicleCreate, db: Session = Depends(database.get_db)):
    presenter = VehiclePresenter(db)
    return presenter.create_vehicle(vehicle)

@router.get("/vehicles/", response_model=list[schemas.Vehicle])
def get_vehicles(db: Session = Depends(database.get_db)):
    presenter = VehiclePresenter(db)
    return presenter.get_vehicles()
