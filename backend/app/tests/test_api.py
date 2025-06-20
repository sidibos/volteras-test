import pytest
from fastapi.testclient import TestClient
from main import app
from database import SessionLocal, Base, engine
from models import Vehicle, VehicleData
from datetime import datetime, UTC

client = TestClient(app)

# Use a test DB if needed
@pytest.fixture(autouse=True)
def setup_and_teardown_db():
    # Setup: Recreate tables
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    test_vehicle_id = "123e4567-e89b-12d3-a456-426614174000"
    
    vehicle = Vehicle(vehicle_id=test_vehicle_id)
    db.add(vehicle)
    db.add(VehicleData(
        vehicle_id=test_vehicle_id,
        timestamp=datetime.now(UTC),
        speed=80,
        odometer=12345.6,
        soc=75.0,
        elevation=300.0,
        shift_state="D"
    ))
    db.commit()
    db.close()
    yield

def test_get_vehicle_data():
    response = client.get("/api/v1/vehicle_data/?vehicle_id=123e4567-e89b-12d3-a456-426614174000")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json()[0]["vehicle_id"] == "123e4567-e89b-12d3-a456-426614174000"

def test_get_vehicle_data_by_id():
    # First get an ID from the list
    response = client.get("/api/v1/vehicle_data/?vehicle_id=123e4567-e89b-12d3-a456-426614174000")
    data_id = response.json()[0]["id"]

    detail_resp = client.get(f"/api/v1/vehicle_data/{data_id}")
    assert detail_resp.status_code == 200
    assert detail_resp.json()["id"] == data_id

def test_post_vehicle_data():
    payload = {
        "vehicle_id": "new-vehicle-001",
        "timestamp": datetime.now(UTC).isoformat(),
        "speed": 50,
        "odometer": 5000,
        "soc": 80,
        "elevation": 150,
        "shift_state": "D"
    }
    response = client.post("/api/v1/vehicle_data/", json=payload)
    assert response.status_code == 201
    assert response.json()["vehicle_id"] == "new-vehicle-001"

def test_list_vehicles():
    response = client.get("/api/v1/vehicles")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert "vehicle_id" in response.json()[0]
