from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Vehicle(Base):
    __tablename__ = "vehicles"
    
    vehicle_id = Column(String(36), primary_key=True, index=True)  # UUID as string
    data = relationship("VehicleData", back_populates="vehicle")


class VehicleData(Base):
    __tablename__ = "vehicle_data"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    vehicle_id = Column(String(36), ForeignKey("vehicles.vehicle_id"), index=True)
    timestamp = Column(DateTime, index=True)
    speed = Column(Integer, nullable=True)
    odometer = Column(Float)
    soc = Column(Integer)
    elevation = Column(Integer)
    shift_state = Column(String(1), nullable=True)
    vehicle = relationship("Vehicle", back_populates="data")
