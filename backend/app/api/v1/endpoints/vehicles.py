from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas import VehicleSchema
import crud
from typing import List

router = APIRouter()

# List all vehicles
@router.get("/vehicles", response_model=List[VehicleSchema])
def list_vehicles(db: Session = Depends(get_db)):
    return crud.get_all_vehicles(db)
