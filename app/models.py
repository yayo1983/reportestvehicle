from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    license_plate = Column(String, unique=True, index=True)
    model = Column(String)
    year = Column(Integer)
    current_mileage = Column(Float)
    service_orders = relationship("ServiceOrder", back_populates="vehicle")


class ServiceOrder(Base):
    __tablename__ = "service_orders"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))
    description = Column(String)
    date = Column(DateTime)
    cost = Column(Float)
    vehicle = relationship("Vehicle", back_populates="service_orders")

    
