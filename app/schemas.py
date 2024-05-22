from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class ServiceOrderBase(BaseModel):
    description: str
    date: datetime
    cost: float

class ServiceOrderCreate(ServiceOrderBase):
    pass

class ServiceOrder(ServiceOrderBase):
    id: int
    vehicle_id: int

    class Config:
        from_attributes = True

class VehicleBase(BaseModel):
    license_plate: str
    model: str
    year: int
    current_mileage: float

class VehicleCreate(VehicleBase):
    pass

class Vehicle(VehicleBase):
    id: int
    service_orders: List[ServiceOrder] = []

    class Config:
        from_attributes = True
