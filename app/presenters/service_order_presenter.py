from sqlalchemy.orm import Session
from app.models import ServiceOrder
from app.schemas import ServiceOrderCreate, ServiceOrderRead

class ServiceOrderPresenter:

    def __init__(self, db: Session):
        self.db = db

    def create_service_order(self, service_order: ServiceOrderCreate) -> ServiceOrderRead:
        db_service_order = ServiceOrder(**service_order.dict())
        self.db.add(db_service_order)
        self.db.commit()
        self.db.refresh(db_service_order)
        return ServiceOrderRead.from_orm(db_service_order)

    def get_service_orders(self, skip: int = 0, limit: int = 10):
        service_orders = self.db.query(ServiceOrder).offset(skip).limit(limit).all()
        return [ServiceOrderRead.from_orm(order) for order in service_orders]
