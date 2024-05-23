from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routes.service_order_route import ServiceOrderRouter
from app.routes.vehicle_route import VehicleRouter


class MyApp:
    """
    MyApp class encapsulates the setup and configuration of the FastAPI application.
    """
    def __init__(self):
        """
        Initializes the MyApp instance by creating database tables, setting up the FastAPI app,
        configuring CORS, and including routers for various routes.
        """
        # Create all tables
        Base.metadata.create_all(bind=engine)

        # Initialize FastAPI application
        self.app = FastAPI(
            title="Transportista Backend API",
            description="API para administrar los procesos de mantenimiento de vehículos.",
            version="1.0.0",
        )

        # Set up CORS middleware
        self._setup_cors()

        # Instantiate the service command router
        self.service_vehicle_router = VehicleRouter()
        self.service_order_router = ServiceOrderRouter()

        # Include the router in the FastAPI application
        self._include_routers()

    def _include_routers(self):
        """
        Includes the service vehicle and service order routers in the FastAPI application
        with specific prefixes.
        """
        self.app.include_router(
            self.service_vehicle_router.router, prefix="/api/v1/vehicles"
        )
        self.app.include_router(
            self.service_order_router.router, prefix="/api/v1/service_orders"
        )

    def _setup_cors(self):
        """
        Configures Cross-Origin Resource Sharing (CORS) middleware for the FastAPI application.
        This allows the application to handle requests from different origins, which is useful 
        for frontend-backend communication during development.

        Note:
            - In this setup, all origins, headers, and methods are allowed, which is convenient for development
            but should be restricted in a production environment for security reasons.
        """
        # Allow all origins, headers, and methods (be careful with this in production)
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Allows all origins
            allow_credentials=True,
            allow_methods=["*"],  # Allows all methods
            allow_headers=["*"],  # Allows all headers
        )

        # Swagger documentation will be available at /docs by default
        # ReDoc documentation will be available at /redoc by default

my_app = MyApp()
app = my_app.app
