from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List
from typing import Optional


class ServiceOrderBase(BaseModel):
    description: str
    date: datetime
    cost: float


class ServiceOrderCreate(ServiceOrderBase):
    vehicle_id: Optional[int] = None

class ServiceOrderUpdate(ServiceOrderBase):
    vehicle_id: Optional[int] = None    

class ServiceOrderRead(ServiceOrderBase):
    id: int
    vehicle_id: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)


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
    model_config = ConfigDict(from_attributes=True)  # Enable validation from ORM attributes
