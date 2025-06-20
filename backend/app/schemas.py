from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class VehicleDataSchema(BaseModel):
    id: int
    vehicle_id: str
    timestamp: datetime
    speed: Optional[float]
    odometer: float
    soc: float
    elevation: float
    shift_state: Optional[str]

    model_config = {
        "from_attributes": True
    }

class VehicleSchema(BaseModel):
    vehicle_id: str

    model_config = {
        "from_attributes": True
    }


class VehicleDataCreate(BaseModel):
    vehicle_id: str
    timestamp: datetime
    speed: Optional[int] = None
    odometer: float
    soc: float
    elevation: float
    shift_state: Optional[str] = None 

class VehicleDataUploadResponse(BaseModel):
    message: str
    vehicle_id: str
    records_uploaded: int

    model_config = {
        "from_attributes": True
    }    

class VehicleSchema(BaseModel):
    vehicle_id: str

    model_config = {
        "from_attributes": True
    }    