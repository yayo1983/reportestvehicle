from pydantic import BaseModel
from datetime import datetime
from typing import List

class ServiceOrderBase(BaseModel):
    description: str
    date: datetime
    cost: float

class ServiceOrderCreate(ServiceOrderBase):
    pass

class ServiceOrderRead(ServiceOrderBase):
    id: int
    vehicle_id: int

    class Config:
        from_atributes = True

class VehicleBase(BaseModel):
    license_plate: str
    model: str
    year: int
    current_mileage: float

class VehicleCreate(VehicleBase):
    pass

class VehicleRead(VehicleBase):
    id: int
    service_orders: List[ServiceOrderRead] = []

