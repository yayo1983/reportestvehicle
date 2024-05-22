from fastapi import FastAPI
from app.database import Base, engine
from app.routes.service_order_route import ServiceOrderRouter
from app.routes.vehicle_route import VehicleRouter


# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Transportista Backend API",
    description="API para administrar los procesos de mantenimiento de vehículos.",
    version="1.0.0",
)

# Instantiate the service command router
service_vehicle_router = VehicleRouter()
service_order_router = ServiceOrderRouter()
# Include the router in the FastAPI application
app.include_router(service_vehicle_router.router, prefix="/api/v1/vehicles")
app.include_router(service_order_router.router, prefix="/service_orders")

# Swagger documentation will be available at /docs por defecto
# ReDoc documentation will be available at /redoc por defecto
