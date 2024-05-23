from sqlalchemy.orm import Session
from app.models import Vehicle
from app.schemas import VehicleCreate, VehicleRead
from sqlalchemy.exc import SQLAlchemyError


class VehiclePresenter:
    """
    VehiclePresenter class manages the database operations related to vehicles.
    It provides methods to create and retrieve vehicle records from the database.
    """

    def __init__(self, db: Session):
        """
        Initializes the VehiclePresenter instance with a database session.

        Args:
            db (Session): The database session to be used for operations.
        """
        self.db = db

    def create_vehicle(self, vehicle: VehicleCreate) -> VehicleRead:
        """
        Creates a new vehicle record in the database.

        Args:
            vehicle (VehicleCreate): The data required to create a new vehicle.

        Returns:
            VehicleRead: The created vehicle record.

        Raises:
            SQLAlchemyError: If an error occurs during the database operation.
        """
        try:
            db_vehicle = Vehicle(**vehicle.model_dump())
            self.db.add(db_vehicle)
            self.db.commit()
            self.db.refresh(db_vehicle)
            return db_vehicle
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e  # Re-raise the exception for further handling

    def get_vehicles(self, skip: int = 0, limit: int = 10):
        """
        Retrieves a list of vehicle records from the database with pagination.

        Args:
            skip (int): The number of records to skip (default is 0).
            limit (int): The maximum number of records to return (default is 10).

        Returns:
            List[VehicleRead]: A list of vehicle records.

        Raises:
            SQLAlchemyError: If an error occurs during the database operation.
        """
        try:
            vehicles = self.db.query(Vehicle).offset(skip).limit(limit).all()
            return [vehicle for vehicle in vehicles]
        except SQLAlchemyError as e:
            raise e  # Re-raise the exception for further handling
