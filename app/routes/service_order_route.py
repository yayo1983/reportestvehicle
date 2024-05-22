from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.presenters.service_order_presenter import ServiceOrderPresenter
from app.schemas import ServiceOrderCreate, ServiceOrderRead
from typing import List

router = APIRouter()

@router.post("/", response_model=ServiceOrderRead)
def create_service_order(service_order: ServiceOrderCreate, db: Session = Depends(get_db)):
    presenter = ServiceOrderPresenter(db)
    return presenter.create_service_order(service_order)

@router.get("/", response_model=List[ServiceOrderRead])
def get_service_orders(skip: int = 0, limit: int = 30, db: Session = Depends(get_db)):
    presenter = ServiceOrderPresenter(db)
    return presenter.get_service_orders(skip, limit)
