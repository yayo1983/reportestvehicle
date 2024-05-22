from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from schemas import VehicleCreate, VehicleRead
from database import get_db
from presenters.vehicle_presenter import VehiclePresenter


class VehicleRouter:
    def __init__(self):
        self.router = APIRouter()
        self._setup_routes()

    def _setup_routes(self):
        self.router.post("/", response_model=VehicleRead)(self.create_vehicle)
        self.router.get("/", response_model=List[VehicleRead])(self.get_vehicles)


    def create_vehicle(self, vehicle: VehicleCreate, db: Session = Depends(get_db)):
        presenter = VehiclePresenter(db)
        return presenter.create_vehicle(vehicle)

    def get_vehicles(self, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
        presenter = VehiclePresenter(db)
        return presenter.get_vehicles(skip, limit)
