from fastapi import FastAPI
from .routers import vehicles, service_orders
from app.database import engine, Base


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(vehicles.router, prefix="/api/v1")
app.include_router(service_orders.router, prefix="/api/v1")
