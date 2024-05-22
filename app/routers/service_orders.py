from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app import schemas
from app.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/vehicles/{vehicle_id}/service_orders/", response_model=schemas.ServiceOrder)
def create_service_order_for_vehicle(
    vehicle_id: int, service_order: schemas.ServiceOrderCreate, db: Session = Depends(get_db)
):
    return crud.create_service_order(db=db, service_order=service_order, vehicle_id=vehicle_id)

@router.get("/service_orders/{service_order_id}", response_model=schemas.ServiceOrder)
def read_service_order(service_order_id: int, db: Session = Depends(get_db)):
    db_service_order = crud.get_service_order(db, service_order_id=service_order_id)
    if db_service_order is None:
        raise HTTPException(status_code=404, detail="Service order not found")
    return db_service_order
