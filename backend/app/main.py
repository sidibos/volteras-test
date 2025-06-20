from fastapi import FastAPI
from database import Base, engine
from api.v1.api import api_router_v1
from fastapi.middleware.cors import CORSMiddleware
import os

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Vehicle Data API",
    version="1.0.0"
)

# Mount versioned router
app.include_router(api_router_v1, prefix="/api/v1")

# Allow frontend (React) to talk to backend
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # or ["*"] for all origins
    allow_credentials=True,
    allow_methods=["*"],              # GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],              # Authorization, Content-Type, etc.
)
