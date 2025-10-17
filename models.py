from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from pydantic import BaseModel

class PersonaBase(SQLModel):
    """Base model for Persona"""
    nombre: str = Field(max_length=100, description="Nombre de la persona")
    apellido: str = Field(max_length=100, description="Apellido de la persona")  
    edad: int = Field(ge=0, le=150, description="Edad de la persona")
    pais_id: Optional[int] = Field(default=None, foreign_key="pais.id", description="ID del país")

class Persona(PersonaBase, table=True):
    """Persona table model"""
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Relationship with pais
    pais: Optional["Pais"] = Relationship(back_populates="personas")

class PersonaCreate(PersonaBase):
    """Model for creating a new persona"""
    pass

class PersonaUpdate(BaseModel):
    """Model for updating persona"""
    nombre: Optional[str] = Field(None, max_length=100, description="Nombre de la persona")
    apellido: Optional[str] = Field(None, max_length=100, description="Apellido de la persona")
    edad: Optional[int] = Field(None, ge=0, le=150, description="Edad de la persona")
    pais_id: Optional[int] = Field(None, description="ID del país")

class PersonaResponse(PersonaBase):
    """Model for persona response"""
    id: int

class PersonaResponseWithPais(PersonaResponse):
    """Model for persona response with pais information"""
    pais: Optional["PaisResponse"] = None


# País models
class PaisBase(SQLModel):
    """Base model for Pais"""
    nombre: str = Field(max_length=100, description="Nombre del país", unique=True)

class Pais(PaisBase, table=True):
    """Pais table model"""
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Relationship with personas
    personas: List["Persona"] = Relationship(back_populates="pais")

class PaisCreate(PaisBase):
    """Model for creating a new pais"""
    pass

class PaisUpdate(BaseModel):
    """Model for updating pais"""
    nombre: Optional[str] = Field(None, max_length=100, description="Nombre del país")

class PaisResponse(PaisBase):
    """Model for pais response"""
    id: int
