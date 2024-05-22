from fastapi import FastAPI
from app.routes import vehicle_route, service_order_route
from app.database import Base, engine

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Transportista Backend API",
    description="API para administrar los procesos de mantenimiento de vehículos.",
    version="1.0.0"
)

app.include_router(vehicle_route.router, prefix="/api/v1/vehicles", tags=["vehicles"])
app.include_router(service_order_route.router, prefix="/api/v1/service_orders", tags=["service_orders"])

# La documentación de Swagger estará disponible en /docs por defecto
# La documentación de ReDoc estará disponible en /redoc por defecto
