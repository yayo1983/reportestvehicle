from sqlalchemy.orm import Session
from app.models import ServiceOrder
from sqlalchemy.exc import NoResultFound 
from app.schemas import ServiceOrderCreate, ServiceOrderRead, ServiceOrderUpdate


class ServiceOrderPresenter:

    def __init__(self, db: Session):
        self.db = db

    def create_service_order(
        self, service_order: ServiceOrderCreate
    ) -> ServiceOrderRead:
        db_service_order = ServiceOrder(**service_order.model_dump())
        print("a salvar", db_service_order.description)
        self.db.add(db_service_order)
        try:
            self.db.commit()
            self.db.refresh(db_service_order)
            return db_service_order
        except Exception as e:
            print("The error", e)
        return False
    
    def get_service_order(self, order_id: int) -> ServiceOrderRead:
        db_service_order = self.db.query(ServiceOrder).filter(ServiceOrder.id == order_id).first()
        if not db_service_order:
            raise NoResultFound(f"Service order with id {order_id} not found")
        return db_service_order

    def get_service_orders(self, skip: int = 0, limit: int = 10):
        service_orders = self.db.query(ServiceOrder).offset(skip).limit(limit).all()
        print(
            "eeeeeeeeeeee",
            service_orders[0].id,
            service_orders[0].description,
            service_orders[0].date,
            service_orders[0].cost,
            service_orders[0].vehicle_id,
        )
        for order in service_orders:
            print(order)
        return [order for order in service_orders]
    
    def update_service_order(self, order_id: int, service_order: ServiceOrderUpdate) -> ServiceOrderRead:
        db_service_order = self.db.query(ServiceOrder).filter(ServiceOrder.id == order_id).first()
        if not db_service_order:
            raise NoResultFound(f"Service order with id {order_id} not found")
        for key, value in service_order.model_dump(exclude_unset=True).items():
            setattr(db_service_order, key, value)
        self.db.commit()
        self.db.refresh(db_service_order)
        return db_service_order

    def delete_service_order(self, order_id: int):
        db_service_order = self.db.query(ServiceOrder).filter(ServiceOrder.id == order_id).first()
        if not db_service_order:
            raise NoResultFound(f"Service order with id {order_id} not found")
        self.db.delete(db_service_order)
        self.db.commit()
        return {"message": "Service order deleted successfully"}