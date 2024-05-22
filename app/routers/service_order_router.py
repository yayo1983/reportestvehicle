from fastapi import APIRouter
from typing import List
from app.models import ServiceOrder
from app.schemas import ServiceOrderCreate, ServiceOrderRead
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends

router = APIRouter()

@router.post("/", response_model=ServiceOrderRead)
def create_service_order(service_order: ServiceOrderCreate, db: Session = Depends(get_db)):
    db_service_order = ServiceOrder(**service_order.dict())
    db.add(db_service_order)
    db.commit()
    db.refresh(db_service_order)
    return db_service_order

@router.get("/", response_model=List[ServiceOrderRead])
def get_service_orders(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    service_orders = db.query(ServiceOrder).offset(skip).limit(limit).all()
    return service_orders
