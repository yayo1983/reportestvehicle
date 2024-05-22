from fastapi import FastAPI
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

        # Instantiate the service command router
        self.service_vehicle_router = VehicleRouter()
        self.service_order_router = ServiceOrderRouter()

        # Include the router in the FastAPI application
        self._include_routers()

    def _include_routers(self):
        self.app.include_router(
            self.service_vehicle_router.router, 
            prefix="/api/v1/vehicles"
        )
        self.app.include_router(
            self.service_order_router.router, 
            prefix="/service_orders"
        )

        # Swagger documentation will be available at /docs by default
        # ReDoc documentation will be available at /redoc by default

    def run(self):
        import uvicorn
        uvicorn.run(self.app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    my_app = MyApp()
    my_app.run()
