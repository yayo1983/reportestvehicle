from fastapi import FastAPI
from app.routers import vehicle_router, service_order_router

app = FastAPI(
    title="Transportista Backend API",
    description="API para administrar los procesos de mantenimiento de vehículos.",
    version="1.0.0"
)

app.include_router(vehicle_router.router, prefix="/api/v1/vehicles", tags=["vehicles"])
app.include_router(service_order_router.router, prefix="/api/v1/service_orders", tags=["service_orders"])

# Swagger documentation will be available in /docs by default
# ReDoc documentation will be available in /redoc by default
