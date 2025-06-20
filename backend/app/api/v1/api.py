from fastapi import APIRouter
from .endpoints import vehicle_data, vehicles

api_router_v1 = APIRouter()
api_router_v1.include_router(vehicle_data.router, prefix="", tags=["vehicle_data"])
api_router_v1.include_router(vehicles.router, tags=["vehicles"])