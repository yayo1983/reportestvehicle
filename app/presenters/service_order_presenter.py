from sqlalchemy.orm import Session
from app.models import ServiceOrder
from app.schemas import ServiceOrderCreate, ServiceOrderRead


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
