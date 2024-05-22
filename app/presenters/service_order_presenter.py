from sqlalchemy.orm import Session
from app import models, schemas

class ServiceOrderPresenter:
    def __init__(self, db: Session):
        self.db = db

    def create_service_order(self, vehicle_id: int, service_order: schemas.ServiceOrderCreate) -> models.ServiceOrder:
        db_service_order = models.ServiceOrder(**service_order.dict(), vehicle_id=vehicle_id)
        self.db.add(db_service_order)
        self.db.commit()
        self.db.refresh(db_service_order)
        return db_service_order

    def get_service_orders(self) -> list[models.ServiceOrder]:
        return self.db.query(models.ServiceOrder).all()
