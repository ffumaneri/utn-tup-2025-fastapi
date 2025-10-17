from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from typing import List
from database import get_session
from models import PersonaCreate, PersonaUpdate, PersonaResponse, PersonaResponseWithPais, PaisResponse
from repository import PersonaRepository, PaisRepository

# Create router for personas
router = APIRouter(prefix="/personas", tags=["personas"])

def get_persona_repository(session: Session = Depends(get_session)) -> PersonaRepository:
    """Dependency to get persona repository"""
    return PersonaRepository(session)

def get_pais_repository(session: Session = Depends(get_session)) -> PaisRepository:
    """Dependency to get pais repository"""
    return PaisRepository(session)

@router.post("/", response_model=PersonaResponse, status_code=status.HTTP_201_CREATED)
def create_persona(
    persona: PersonaCreate,
    repo: PersonaRepository = Depends(get_persona_repository),
    pais_repo: PaisRepository = Depends(get_pais_repository)
) -> PersonaResponse:
    """Create a new persona"""
    try:
        # Validate that pais exists if provided
        if persona.pais_id is not None:
            db_pais = pais_repo.get_by_id(persona.pais_id)
            if not db_pais:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Pais with id {persona.pais_id} not found"
                )
        
        db_persona = repo.create(persona)
        return PersonaResponse.model_validate(db_persona)
    except HTTPException:
        raise
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
    repo: PersonaRepository = Depends(get_persona_repository),
    pais_repo: PaisRepository = Depends(get_pais_repository)
) -> PersonaResponse:
    """Update persona by ID"""
    try:
        # Validate that pais exists if provided
        if persona_update.pais_id is not None:
            db_pais = pais_repo.get_by_id(persona_update.pais_id)
            if not db_pais:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Pais with id {persona_update.pais_id} not found"
                )
        
        db_persona = repo.update(persona_id, persona_update)
        if not db_persona:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Persona with id {persona_id} not found"
            )
        return PersonaResponse.model_validate(db_persona)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error updating persona: {str(e)}"
        )

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

@router.get("/with-pais/", response_model=List[PersonaResponseWithPais])
def get_personas_with_pais(
    skip: int = Query(0, ge=0, description="Number of personas to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of personas to return"),
    repo: PersonaRepository = Depends(get_persona_repository),
    pais_repo: PaisRepository = Depends(get_pais_repository)
) -> List[PersonaResponseWithPais]:
    """Get all personas with their pais information included"""
    personas = repo.get_all(skip=skip, limit=limit)
    result = []
    
    for persona in personas:
        persona_dict = PersonaResponseWithPais.model_validate(persona).model_dump()
        
        # Load pais information if pais_id exists
        if persona.pais_id:
            db_pais = pais_repo.get_by_id(persona.pais_id)
            if db_pais:
                persona_dict['pais'] = PaisResponse.model_validate(db_pais).model_dump()
        
        result.append(PersonaResponseWithPais.model_validate(persona_dict))
    
    return result

@router.get("/{persona_id}/with-pais", response_model=PersonaResponseWithPais)
def get_persona_with_pais(
    persona_id: int,
    repo: PersonaRepository = Depends(get_persona_repository),
    pais_repo: PaisRepository = Depends(get_pais_repository)
) -> PersonaResponseWithPais:
    """Get persona by ID with pais information included"""
    db_persona = repo.get_by_id(persona_id)
    if not db_persona:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Persona with id {persona_id} not found"
        )
    
    persona_dict = PersonaResponseWithPais.model_validate(db_persona).model_dump()
    
    # Load pais information if pais_id exists
    if db_persona.pais_id:
        db_pais = pais_repo.get_by_id(db_persona.pais_id)
        if db_pais:
            persona_dict['pais'] = PaisResponse.model_validate(db_pais).model_dump()
    
    return PersonaResponseWithPais.model_validate(persona_dict)

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
