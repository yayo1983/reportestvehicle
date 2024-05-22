from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from sqlalchemy.exc import NoResultFound
from app.presenters.service_order_presenter import ServiceOrderPresenter
from app.schemas import ServiceOrderCreate, ServiceOrderRead, ServiceOrderUpdate
from typing import List

router = APIRouter()


@router.post("/", response_model=ServiceOrderRead)
def create_service_order(
    service_order: ServiceOrderCreate, db: Session = Depends(get_db)
):
    presenter = ServiceOrderPresenter(db)
    return presenter.create_service_order(service_order)


@router.get("/", response_model=List[ServiceOrderRead])
def get_service_orders(skip: int = 0, limit: int = 30, db: Session = Depends(get_db)):
    presenter = ServiceOrderPresenter(db)
    return presenter.get_service_orders(skip, limit)


@router.get("/{order_id}", response_model=ServiceOrderRead)
def get_service_order(order_id: int, db: Session = Depends(get_db)):
    presenter = ServiceOrderPresenter(db)
    try:
        return presenter.get_service_order(order_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Service order not found")


@router.put("/{order_id}", response_model=ServiceOrderRead)
def update_service_order(
    order_id: int, service_order: ServiceOrderUpdate, db: Session = Depends(get_db)
):
    presenter = ServiceOrderPresenter(db)
    try:
        return presenter.update_service_order(order_id, service_order)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Service order not found")


@router.delete("/{order_id}")
def delete_service_order(order_id: int, db: Session = Depends(get_db)):
    presenter = ServiceOrderPresenter(db)
    try:
        return presenter.delete_service_order(order_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Service order not found")
