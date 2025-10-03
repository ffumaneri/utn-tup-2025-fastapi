from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from contextlib import asynccontextmanager

from database import create_db_and_tables
from objects import objects_router
from personas import router as personas_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    create_db_and_tables()
    yield
    # Shutdown (if needed)

app = FastAPI(
    title="FastAPI CRUD App", 
    description="API with Personas CRUD", 
    version="1.0.0",
    lifespan=lifespan
)

# Include personas router
app.include_router(personas_router)
app.include_router(objects_router)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
