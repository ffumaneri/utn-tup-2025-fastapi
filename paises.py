from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from typing import List
from database import get_session
from models import Pais, PaisCreate, PaisUpdate, PaisResponse
from repository import PaisRepository

# Create router for paises
router = APIRouter(prefix="/paises", tags=["paises"])

def get_pais_repository(session: Session = Depends(get_session)) -> PaisRepository:
    """Dependency to get pais repository"""
    return PaisRepository(session)

@router.post("/", response_model=PaisResponse, status_code=status.HTTP_201_CREATED)
def create_pais(
    pais: PaisCreate,
    repo: PaisRepository = Depends(get_pais_repository)
) -> PaisResponse:
    """Create a new pais"""
    try:
        db_pais = repo.create(pais)
        return PaisResponse.model_validate(db_pais)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating pais: {str(e)}"
        )

@router.get("/", response_model=List[PaisResponse])
def get_paises(
    skip: int = Query(0, ge=0, description="Number of paises to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of paises to return"),
    repo: PaisRepository = Depends(get_pais_repository)
) -> List[PaisResponse]:
    """Get all paises with pagination"""
    paises = repo.get_all(skip=skip, limit=limit)
    return [PaisResponse.model_validate(pais) for pais in paises]

@router.get("/{pais_id}", response_model=PaisResponse)
def get_pais(
    pais_id: int,
    repo: PaisRepository = Depends(get_pais_repository)
) -> PaisResponse:
    """Get pais by ID"""
    db_pais = repo.get_by_id(pais_id)
    if not db_pais:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pais with id {pais_id} not found"
        )
    return PaisResponse.model_validate(db_pais)

@router.put("/{pais_id}", response_model=PaisResponse)
def update_pais(
    pais_id: int,
    pais_update: PaisUpdate,
    repo: PaisRepository = Depends(get_pais_repository)
) -> PaisResponse:
    """Update pais by ID"""
    db_pais = repo.update(pais_id, pais_update)
    if not db_pais:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pais with id {pais_id} not found"
        )
    return PaisResponse.model_validate(db_pais)

@router.delete("/{pais_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pais(
    pais_id: int,
    repo: PaisRepository = Depends(get_pais_repository)
) -> None:
    """Delete pais by ID"""
    success = repo.delete(pais_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pais with id {pais_id} not found"
        )

@router.get("/search/", response_model=List[PaisResponse])
def search_paises_by_name(
    nombre: str = Query(..., min_length=2, description="Name to search for"),
    repo: PaisRepository = Depends(get_pais_repository)
) -> List[PaisResponse]:
    """Search paises by name (partial match)"""
    # This would require additional repository method for search
    # For now, we'll get all and filter in Python (not efficient for large datasets)
    all_paises = repo.get_all(limit=1000)
    filtered_paises = [
        pais for pais in all_paises 
        if nombre.lower() in pais.nombre.lower()
    ]
    return [PaisResponse.model_validate(pais) for pais in filtered_paises]
