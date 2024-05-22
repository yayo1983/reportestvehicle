from fastapi import FastAPI
from app.views import vehicle_view, service_order_view
from app.database import engine
from app.models import Base

app = FastAPI()

# Create all tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(vehicle_view.router, prefix="/api/v1")
app.include_router(service_order_view.router, prefix="/api/v1")
