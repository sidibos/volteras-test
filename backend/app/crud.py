from sqlalchemy.orm import Session
from models import VehicleData, Vehicle
from typing import Optional, List
from datetime import datetime
from schemas import VehicleDataCreate

def get_vehicle_data(
    db: Session,
    vehicle_id: str,
    skip: int = 0,
    limit: int = 100,
    start: Optional[datetime] = None,
    end: Optional[datetime] = None
) -> List[VehicleData]:
    query = db.query(VehicleData).filter(VehicleData.vehicle_id == vehicle_id)

    if start:
        query = query.filter(VehicleData.timestamp >= start)
    if end:
        query = query.filter(VehicleData.timestamp <= end)

    return query.offset(skip).limit(limit).all()

def get_vehicle_data_by_id(db: Session, data_id: int) -> Optional[VehicleData]:
    return db.query(VehicleData).filter(VehicleData.id == data_id).first()

def create_vehicle_data(db: Session, data: VehicleDataCreate):
    # Ensure vehicle exists
    vehicle = db.query(Vehicle).filter_by(vehicle_id=data.vehicle_id).first()
    if not vehicle:
        vehicle = Vehicle(vehicle_id=data.vehicle_id)
        db.add(vehicle)

    record = VehicleData(**data.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def get_all_vehicles(db: Session) -> List[Vehicle]:
    return db.query(Vehicle).all()