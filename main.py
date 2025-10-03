from fastapi import FastAPI, Query, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional, Dict, Any
from contextlib import asynccontextmanager
from pydantic import BaseModel
from database import create_db_and_tables
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

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Pydantic models for request/response validation
class ObjectData(BaseModel):
    """Model for object data which can contain any key-value pairs"""
    pass

    class Config:
        extra = "allow"  # Allow additional fields

class CreateObjectRequest(BaseModel):
    name: str
    data: Optional[Dict[str, Any]] = None

class ObjectResponse(BaseModel):
    id: str
    name: str
    data: Optional[Dict[str, Any]] = None

# Global array with objects data
objects_data = [
    {
        "id": "1",
        "name": "Google Pixel 6 Pro",
        "data": {
            "color": "Cloudy White",
            "capacity": "128 GB"
        }
    },
    {
        "id": "2",
        "name": "Apple iPhone 12 Mini, 256GB, Blue",
        "data": None
    },
    {
        "id": "3",
        "name": "Apple iPhone 12 Pro Max",
        "data": {
            "color": "Cloudy White",
            "capacity GB": 512
        }
    },
    {
        "id": "4",
        "name": "Apple iPhone 11, 64GB",
        "data": {
            "price": 389.99,
            "color": "Purple"
        }
    },
    {
        "id": "5",
        "name": "Samsung Galaxy Z Fold2",
        "data": {
            "price": 689.99,
            "color": "Brown"
        }
    },
    {
        "id": "6",
        "name": "Apple AirPods",
        "data": {
            "generation": "3rd",
            "price": 120
        }
    },
    {
        "id": "7",
        "name": "Apple MacBook Pro 16",
        "data": {
            "year": 2019,
            "price": 1849.99,
            "CPU model": "Intel Core i9",
            "Hard disk size": "1 TB"
        }
    },
    {
        "id": "8",
        "name": "Apple Watch Series 8",
        "data": {
            "Strap Colour": "Elderberry",
            "Case Size": "41mm"
        }
    },
    {
        "id": "9",
        "name": "Beats Studio3 Wireless",
        "data": {
            "Color": "Red",
            "Description": "High-performance wireless noise cancelling headphones"
        }
    },
    {
        "id": "10",
        "name": "Apple iPad Mini 5th Gen",
        "data": {
            "Capacity": "64 GB",
            "Screen size": 7.9
        }
    },
    {
        "id": "11",
        "name": "Apple iPad Mini 5th Gen",
        "data": {
            "Capacity": "254 GB",
            "Screen size": 7.9
        }
    },
    {
        "id": "12",
        "name": "Apple iPad Air",
        "data": {
            "Generation": "4th",
            "Price": "419.99",
            "Capacity": "64 GB"
        }
    },
    {
        "id": "13",
        "name": "Apple iPad Air",
        "data": {
            "Generation": "4th",
            "Price": "519.99",
            "Capacity": "256 GB"
        }
    }
]

@app.get("/objects")
def get_objects(id: List[str] = Query(None)):
    """Get objects from the global array, optionally filtered by IDs"""
    if id is None:
        # Return all objects if no ID filter is provided
        return objects_data
    
    # Filter objects by the provided IDs
    filtered_objects = [obj for obj in objects_data if obj["id"] in id]
    return filtered_objects

@app.get("/objects/{object_id}")
def get_object_by_id(object_id: str):
    """Get a single object by its ID"""
    for obj in objects_data:
        if obj["id"] == object_id:
            return obj
    
    # If object not found, raise 404 error
    raise HTTPException(status_code=404, detail=f"Object with id '{object_id}' not found")

@app.post("/objects", status_code=status.HTTP_201_CREATED)
def add_object(new_object: CreateObjectRequest):
    """Add a new object to the collection"""
    # Generate new ID (find the highest existing ID and add 1)
    existing_ids = [int(obj["id"]) for obj in objects_data if obj["id"].isdigit()]
    new_id = str(max(existing_ids) + 1) if existing_ids else "1"
    
    # Create the new object
    created_object = {
        "id": new_id,
        "name": new_object.name,
        "data": new_object.data
    }
    
    # Add to the global array
    objects_data.append(created_object)
    
    return created_object

@app.delete("/objects/{object_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_object(object_id: str):
    """Delete an object by its ID"""
    for i, obj in enumerate(objects_data):
        if obj["id"] == object_id:
            objects_data.pop(i)
            return
    
    # If object not found, raise 404 error
    raise HTTPException(status_code=404, detail=f"Object with id '{object_id}' not found")