from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from sqlalchemy.exc import NoResultFound
from presenters.service_order_presenter import ServiceOrderPresenter
from schemas import ServiceOrderCreate, ServiceOrderRead, ServiceOrderUpdate
from typing import List

class ServiceOrderRouter:
    def __init__(self):
        self.router = APIRouter()
        self._setup_routes()

    def _setup_routes(self):
        self.router.post("/", response_model=ServiceOrderRead)(self.create_service_order)
        self.router.get("/", response_model=List[ServiceOrderRead])(self.get_service_orders)
        self.router.get("/{order_id}", response_model=ServiceOrderRead)(self.get_service_order)
        self.router.put("/{order_id}", response_model=ServiceOrderRead)(self.update_service_order)
        self.router.delete("/{order_id}")(self.delete_service_order)

    def create_service_order(self, service_order: ServiceOrderCreate, db: Session = Depends(get_db)):
        presenter = ServiceOrderPresenter(db)
        return presenter.create_service_order(service_order)

    def get_service_orders(self, skip: int = 0, limit: int = 30, db: Session = Depends(get_db)):
        presenter = ServiceOrderPresenter(db)
        return presenter.get_service_orders(skip, limit)

    def get_service_order(self, order_id: int, db: Session = Depends(get_db)):
        presenter = ServiceOrderPresenter(db)
        try:
            return presenter.get_service_order(order_id)
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Service order not found")

    def update_service_order(self, order_id: int, service_order: ServiceOrderUpdate, db: Session = Depends(get_db)):
        presenter = ServiceOrderPresenter(db)
        try:
            return presenter.update_service_order(order_id, service_order)
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Service order not found")

    def delete_service_order(self, order_id: int, db: Session = Depends(get_db)):
        presenter = ServiceOrderPresenter(db)
        try:
            return presenter.delete_service_order(order_id)
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Service order not found")
