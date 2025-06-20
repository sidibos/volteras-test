from fastapi import APIRouter, UploadFile, File, Depends, Query, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse, Response
import json
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from database import get_db
from schemas import VehicleDataCreate, VehicleDataSchema, VehicleDataUploadResponse
import uuid
import io
import crud
import pandas as pd
from models import Vehicle, VehicleData


router = APIRouter()

# List vehicle data with optional filters
@router.get("/vehicle_data/", response_model=List[VehicleDataSchema])
async def list_vehicle_data(
    vehicle_id: str = Query(None, description="Filter by vehicle ID"),
    skip: int = 0,
    limit: int = 100,
    start: Optional[datetime] = Query(None),
    end: Optional[datetime] = Query(None),
    db: Session = Depends(get_db)
):
    return crud.get_vehicle_data(db, vehicle_id, skip, limit, start, end)


# Get vehicle data by ID
@router.get("/vehicle_data/{data_id}/", response_model=VehicleDataSchema)
async def get_vehicle_data_by_id(data_id: int, db: Session = Depends(get_db)):
    data = crud.get_vehicle_data_by_id(db, data_id)
    if not data:
        raise HTTPException(status_code=404, detail="Vehicle data not found")
    return data

# Create new vehicle data record
@router.post("/vehicle_data/", response_model=VehicleDataSchema, status_code=201)
def create_vehicle_data(data: VehicleDataCreate, db: Session = Depends(get_db)):
    try:
        record = crud.create_vehicle_data(db, data)
        return record
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

# Upload vehicle data from CSV file
@router.post("/vehicle_data/upload/", response_model=VehicleDataUploadResponse, status_code=201)
async def upload_vehicle_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Check CSV file
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only .csv files are accepted")
    
    vehicle_id = file.filename.replace(".csv", "")
    try:
        uuid.UUID(vehicle_id)  # Validate it's a UUID
    except ValueError:
        raise HTTPException(status_code=400, detail="Filename must be a valid UUID (vehicle_id.csv)")

    # Read and parse CSV into DataFrame
    df = pd.read_csv(file.file)
    if 'timestamp' not in df.columns:
        raise HTTPException(status_code=400, detail="Missing 'timestamp' column")

    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Add Vehicle if not exists
    if not db.query(Vehicle).filter_by(vehicle_id=vehicle_id).first():
        db.add(Vehicle(vehicle_id=vehicle_id))

    for _, row in df.iterrows():
        db.add(VehicleData(
            vehicle_id=vehicle_id,
            timestamp=row['timestamp'],
            speed=None if pd.isna(row.get('speed')) else int(row['speed']),
            odometer=row['odometer'],
            soc=row['soc'],
            elevation=row['elevation'],
            shift_state=row['shift_state'] if pd.notna(row['shift_state']) else None
        ))

    db.commit()
    return {"message": "Data uploaded successfully", "vehicle_id": vehicle_id, "records_uploaded": len(df)}


# Get count of vehicle data records for a specific vehicle
@router.get("/vehicle_data/count")
def get_vehicle_data_count(vehicle_id: str, db: Session = Depends(get_db))-> int:
    return db.query(VehicleData).filter(VehicleData.vehicle_id == vehicle_id).count()


# Export vehicle data to CSV, JSON, or Excel
@router.get("/vehicle_data/export")
def export_vehicle_data(
    vehicle_id: str,
    format: str = "csv",  # options: csv, json, excel
    start: Optional[datetime] = Query(None),
    end: Optional[datetime] = Query(None),
    db: Session = Depends(get_db)
):
    # get vehicle data for the given vehicle_id
    query = db.query(VehicleData).filter(VehicleData.vehicle_id == vehicle_id)
    if start:
        # filter by start datetime
        query = query.filter(VehicleData.timestamp >= start)
    if end:
        # filter by end datetime
        query = query.filter(VehicleData.timestamp <= end)

    results = query.all()
    if not results:
        return JSONResponse(content={"message": "No data found"}, status_code=404)

    # Convert to DataFrame
    df = pd.DataFrame([{
        "timestamp": r.timestamp,
        "speed": r.speed,
        "odometer": r.odometer,
        "soc": r.soc,
        "elevation": r.elevation,
        "shift_state": r.shift_state
    } for r in results])

    # Generate timestamp string (safe for filenames)
    timestamp_str = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    filename_prefix = vehicle_id[:10] # Use first 18 characters of UUID for filename safety
    filename_base = f"{filename_prefix}_vehicle_data_{timestamp_str}"

    # download as JSON, CSV, or Excel
    if format == "json":
        df["timestamp"] = df["timestamp"].apply(lambda ts: ts.isoformat() if pd.notna(ts) else None)
        json_data = json.dumps(df.to_dict(orient="records"))

        return Response(
            content=json_data,
            media_type="application/json",
            headers={
                "Content-Disposition": f"attachment; filename={filename_base}.json"
            }
        )
    elif format == "csv":
        stream = io.StringIO()
        df.to_csv(stream, index=False)
        return StreamingResponse(
            iter([stream.getvalue()]),
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename={filename_base}.csv"
            }
        )
    elif format == "excel":
        stream = io.BytesIO()
        with pd.ExcelWriter(stream, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False)
        stream.seek(0)
        return StreamingResponse(
            stream,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": f"attachment; filename={filename_base}.xlsx"
            }
        )
    else:
        return JSONResponse(content={"message": "Unsupported format"}, status_code=400)