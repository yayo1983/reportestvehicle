from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound, SQLAlchemyError
from models import ServiceOrder
from schemas import ServiceOrderCreate, ServiceOrderRead, ServiceOrderUpdate

class ServiceOrderPresenter:

    def __init__(self, db: Session):
        self.db = db

    def create_service_order(self, service_order: ServiceOrderCreate) -> ServiceOrderRead:
        try:
            db_service_order = ServiceOrder(**service_order.model_dump())
            self.db.add(db_service_order)
            self.db.commit()
            self.db.refresh(db_service_order)
            return db_service_order
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e  # Re-raise the exception for further handling

    def get_service_orders(self, skip: int = 0, limit: int = 10):
        try:
            service_orders = self.db.query(ServiceOrder).offset(skip).limit(limit).all()
            return [order for order in service_orders]
        except SQLAlchemyError as e:
            raise e  # Re-raise the exception for further handling

    def get_service_order(self, order_id: int) -> ServiceOrderRead:
        try:
            db_service_order = self.db.query(ServiceOrder).filter(ServiceOrder.id == order_id).first()
            if not db_service_order:
                raise NoResultFound(f"Service order with id {order_id} not found")
            return db_service_order
        except SQLAlchemyError as e:
            raise e  # Re-raise the exception for further handling

    def update_service_order(self, order_id: int, service_order: ServiceOrderUpdate) -> ServiceOrderRead:
        try:
            db_service_order = self.db.query(ServiceOrder).filter(ServiceOrder.id == order_id).first()
            if not db_service_order:
                raise NoResultFound(f"Service order with id {order_id} not found")
            for key, value in service_order.model_dump(exclude_unset=True).items():
                setattr(db_service_order, key, value)
            self.db.commit()
            self.db.refresh(db_service_order)
            return db_service_order
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e  # Re-raise the exception for further handling

    def delete_service_order(self, order_id: int):
        try:
            db_service_order = self.db.query(ServiceOrder).filter(ServiceOrder.id == order_id).first()
            if not db_service_order:
                raise NoResultFound(f"Service order with id {order_id} not found")
            self.db.delete(db_service_order)
            self.db.commit()
            return {"message": "Service order deleted successfully"}
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e  # Re-raise the exception for further handling
