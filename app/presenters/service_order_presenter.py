from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound, SQLAlchemyError
from app.models import ServiceOrder
from app.schemas import ServiceOrderCreate, ServiceOrderRead, ServiceOrderUpdate


class ServiceOrderPresenter:
    """
    ServiceOrderPresenter class manages the database operations related to service orders.
    It provides methods to create, retrieve, update, and delete service order records.
    """

    def __init__(self, db: Session):
        """
        Initializes the ServiceOrderPresenter instance with a database session.

        Args:
            db (Session): The database session to be used for operations.
        """
        self.db = db

    def create_service_order(
        self, service_order: ServiceOrderCreate
    ) -> ServiceOrderRead:
        """
        Creates a new service order record in the database.

        Args:
            service_order (ServiceOrderCreate): The data required to create a new service order.

        Returns:
            ServiceOrderRead: The created service order record.

        Raises:
            SQLAlchemyError: If an error occurs during the database operation.
        """
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
        """
        Retrieves a list of service order records from the database with pagination.

        Args:
            skip (int): The number of records to skip (default is 0).
            limit (int): The maximum number of records to return (default is 10).

        Returns:
            List[ServiceOrderRead]: A list of service order records.

        Raises:
            SQLAlchemyError: If an error occurs during the database operation.
        """
        try:
            service_orders = self.db.query(ServiceOrder).offset(skip).limit(limit).all()
            return [order for order in service_orders]
        except SQLAlchemyError as e:
            raise e  # Re-raise the exception for further handling

    def get_service_order(self, order_id: int) -> ServiceOrderRead:
        """
        Retrieves a specific service order by its ID.

        Args:
            order_id (int): The ID of the service order to retrieve.

        Returns:
            ServiceOrderRead: The requested service order.

        Raises:
            NoResultFound: If the service order is not found.
            SQLAlchemyError: If an error occurs during the database operation.
        """
        try:
            db_service_order = (
                self.db.query(ServiceOrder).filter(ServiceOrder.id == order_id).first()
            )
            if not db_service_order:
                raise NoResultFound(f"Service order with id {order_id} not found")
            return db_service_order
        except SQLAlchemyError as e:
            raise e  # Re-raise the exception for further handling

    def update_service_order(
        self, order_id: int, service_order: ServiceOrderUpdate
    ) -> ServiceOrderRead:
        """
        Updates an existing service order by its ID.

        Args:
            order_id (int): The ID of the service order to update.
            service_order (ServiceOrderUpdate): The new data for the service order.

        Returns:
            ServiceOrderRead: The updated service order.

        Raises:
            NoResultFound: If the service order is not found.
            SQLAlchemyError: If an error occurs during the database operation.
        """
        try:
            db_service_order = (
                self.db.query(ServiceOrder).filter(ServiceOrder.id == order_id).first()
            )
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
        """
        Deletes a service order by its ID.

        Args:
            order_id (int): The ID of the service order to delete.

        Returns:
            dict: A message indicating successful deletion.

        Raises:
            NoResultFound: If the service order is not found.
            SQLAlchemyError: If an error occurs during the database operation.
        """
        try:
            db_service_order = (
                self.db.query(ServiceOrder).filter(ServiceOrder.id == order_id).first()
            )
            if not db_service_order:
                raise NoResultFound(f"Service order with id {order_id} not found")
            self.db.delete(db_service_order)
            self.db.commit()
            return {"message": "Service order deleted successfully"}
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e  # Re-raise the exception for further handling
