from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from typing import List
from database import get_session
from models import Persona, PersonaCreate, PersonaUpdate, PersonaResponse
from repository import PersonaRepository

# Create router for personas
router = APIRouter(prefix="/personas", tags=["personas"])

def get_persona_repository(session: Session = Depends(get_session)) -> PersonaRepository:
    """Dependency to get persona repository"""
    return PersonaRepository(session)

@router.post("/", response_model=PersonaResponse, status_code=status.HTTP_201_CREATED)
def create_persona(
    persona: PersonaCreate,
    repo: PersonaRepository = Depends(get_persona_repository)
) -> PersonaResponse:
    """Create a new persona"""
    try:
        db_persona = repo.create(persona)
        return PersonaResponse.model_validate(db_persona)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating persona: {str(e)}"
        )

@router.get("/", response_model=List[PersonaResponse])
def get_personas(
    skip: int = Query(0, ge=0, description="Number of personas to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of personas to return"),
    repo: PersonaRepository = Depends(get_persona_repository)
) -> List[PersonaResponse]:
    """Get all personas with pagination"""
    personas = repo.get_all(skip=skip, limit=limit)
    return [PersonaResponse.model_validate(persona) for persona in personas]

@router.get("/{persona_id}", response_model=PersonaResponse)
def get_persona(
    persona_id: int,
    repo: PersonaRepository = Depends(get_persona_repository)
) -> PersonaResponse:
    """Get persona by ID"""
    db_persona = repo.get_by_id(persona_id)
    if not db_persona:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Persona with id {persona_id} not found"
        )
    return PersonaResponse.model_validate(db_persona)

@router.put("/{persona_id}", response_model=PersonaResponse)
def update_persona(
    persona_id: int,
    persona_update: PersonaUpdate,
    repo: PersonaRepository = Depends(get_persona_repository)
) -> PersonaResponse:
    """Update persona by ID"""
    db_persona = repo.update(persona_id, persona_update)
    if not db_persona:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Persona with id {persona_id} not found"
        )
    return PersonaResponse.model_validate(db_persona)

@router.delete("/{persona_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_persona(
    persona_id: int,
    repo: PersonaRepository = Depends(get_persona_repository)
) -> None:
    """Delete persona by ID"""
    success = repo.delete(persona_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Persona with id {persona_id} not found"
        )

@router.get("/search/", response_model=List[PersonaResponse])
def search_personas_by_name(
    nombre: str = Query(..., min_length=2, description="Name to search for"),
    repo: PersonaRepository = Depends(get_persona_repository)
) -> List[PersonaResponse]:
    """Search personas by name (partial match)"""
    # This would require additional repository method for search
    # For now, we'll get all and filter in Python (not efficient for large datasets)
    all_personas = repo.get_all(limit=1000)
    filtered_personas = [
        persona for persona in all_personas 
        if nombre.lower() in persona.nombre.lower() or nombre.lower() in persona.apellido.lower()
    ]
    return [PersonaResponse.model_validate(persona) for persona in filtered_personas]
