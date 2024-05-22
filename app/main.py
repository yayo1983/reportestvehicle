from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from routes.service_order_route import ServiceOrderRouter
from routes.vehicle_route import VehicleRouter


class MyApp:
    def __init__(self):
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
        self.app.include_router(
            self.service_vehicle_router.router, prefix="/api/v1/vehicles"
        )
        self.app.include_router(
            self.service_order_router.router, prefix="/api/v1/service_orders"
        )

    def _setup_cors(self):
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

    def run(self):
        import uvicorn

        uvicorn.run(self.app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    my_app = MyApp()
    my_app.run()
