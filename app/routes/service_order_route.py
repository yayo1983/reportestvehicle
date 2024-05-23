from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from sqlalchemy.exc import NoResultFound
from app.presenters.service_order_presenter import ServiceOrderPresenter
from app.schemas import ServiceOrderCreate, ServiceOrderRead, ServiceOrderUpdate
from typing import List


class ServiceOrderRouter:
    """
    ServiceOrderRouter class manages the routing for service order operations in the FastAPI application.
    It defines the routes and their corresponding handler methods for creating, reading, updating, and 
    deleting service orders.
    """
    def __init__(self):
        """
        Initializes the ServiceOrderRouter instance by creating an APIRouter and setting up the routes.
        """
        self.router = APIRouter()
        self._setup_routes()

    def _setup_routes(self):
        """
        Sets up the routes for the service order operations and links them to their respective handler methods.
        """
        self.router.post("/", response_model=ServiceOrderRead)(
            self.create_service_order
        )
        self.router.get("/", response_model=List[ServiceOrderRead])(
            self.get_service_orders
        )
        self.router.get("/{order_id}", response_model=ServiceOrderRead)(
            self.get_service_order
        )
        self.router.put("/{order_id}", response_model=ServiceOrderRead)(
            self.update_service_order
        )
        self.router.delete("/{order_id}")(self.delete_service_order)

    def create_service_order(
        self, service_order: ServiceOrderCreate, db: Session = Depends(get_db)
    ):
        """
        Handles the creation of a new service order.

        Args:
            service_order (ServiceOrderCreate): The data required to create a new service order.
            db (Session): The database session dependency.

        Returns:
            ServiceOrderRead: The created service order.
        """
        presenter = ServiceOrderPresenter(db)
        return presenter.create_service_order(service_order)

    def get_service_orders(
        self, skip: int = 0, limit: int = 30, db: Session = Depends(get_db)
    ):
        """
        Retrieves a list of service orders with pagination.

        Args:
            skip (int): The number of records to skip (default is 0).
            limit (int): The maximum number of records to return (default is 30).
            db (Session): The database session dependency.

        Returns:
            List[ServiceOrderRead]: A list of service orders.
        """
        presenter = ServiceOrderPresenter(db)
        return presenter.get_service_orders(skip, limit)

    def get_service_order(self, order_id: int, db: Session = Depends(get_db)):
        """
        Retrieves a specific service order by its ID.

        Args:
            order_id (int): The ID of the service order to retrieve.
            db (Session): The database session dependency.

        Returns:
            ServiceOrderRead: The requested service order.

        Raises:
            HTTPException: If the service order is not found.
        """
        presenter = ServiceOrderPresenter(db)
        try:
            return presenter.get_service_order(order_id)
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Service order not found")

    def update_service_order(
        self,
        order_id: int,
        service_order: ServiceOrderUpdate,
        db: Session = Depends(get_db),
    ):
        """
        Updates an existing service order by its ID.

        Args:
            order_id (int): The ID of the service order to update.
            service_order (ServiceOrderUpdate): The new data for the service order.
            db (Session): The database session dependency.

        Returns:
            ServiceOrderRead: The updated service order.

        Raises:
            HTTPException: If the service order is not found.
        """
        presenter = ServiceOrderPresenter(db)
        try:
            return presenter.update_service_order(order_id, service_order)
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Service order not found")

    def delete_service_order(self, order_id: int, db: Session = Depends(get_db)):
        """
        Deletes a service order by its ID.

        Args:
            order_id (int): The ID of the service order to delete.
            db (Session): The database session dependency.

        Returns:
            None: Indicates successful deletion.

        Raises:
            HTTPException: If the service order is not found.
        """
        presenter = ServiceOrderPresenter(db)
        try:
            return presenter.delete_service_order(order_id)
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Service order not found")
