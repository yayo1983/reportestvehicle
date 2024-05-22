from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import schemas, database
from app.presenters.service_order_presenter import ServiceOrderPresenter

router = APIRouter()

@router.post("/vehicles/{vehicle_id}/service_orders/", response_model=schemas.ServiceOrder)
def create_service_order(vehicle_id: int, service_order: schemas.ServiceOrderCreate, db: Session = Depends(database.get_db)):
    presenter = ServiceOrderPresenter(db)
    return presenter.create_service_order(vehicle_id, service_order)

@router.get("/service_orders/", response_model=list[schemas.ServiceOrder])
def get_service_orders(db: Session = Depends(database.get_db)):
    presenter = ServiceOrderPresenter(db)
    return presenter.get_service_orders()
