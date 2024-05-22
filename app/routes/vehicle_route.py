from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.schemas import VehicleCreate, VehicleRead
from app.database import get_db
from app.presenters.vehicle_presenter import VehiclePresenter

router = APIRouter()

@router.post("/", response_model=VehicleRead)
def create_vehicle(vehicle: VehicleCreate, db: Session = Depends(get_db)):
    presenter = VehiclePresenter(db)
    return presenter.create_vehicle(vehicle)

@router.get("/", response_model=List[VehicleRead])
def get_vehicles(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    presenter = VehiclePresenter(db)
    return presenter.get_vehicles(skip, limit)
