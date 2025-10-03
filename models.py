from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import BaseModel

class PersonaBase(SQLModel):
    """Base model for Persona"""
    nombre: str = Field(max_length=100, description="Nombre de la persona")
    apellido: str = Field(max_length=100, description="Apellido de la persona")  
    edad: int = Field(ge=0, le=150, description="Edad de la persona")

class Persona(PersonaBase, table=True):
    """Persona table model"""
    id: Optional[int] = Field(default=None, primary_key=True)

class PersonaCreate(PersonaBase):
    """Model for creating a new persona"""
    pass

class PersonaUpdate(BaseModel):
    """Model for updating persona"""
    nombre: Optional[str] = Field(None, max_length=100, description="Nombre de la persona")
    apellido: Optional[str] = Field(None, max_length=100, description="Apellido de la persona")
    edad: Optional[int] = Field(None, ge=0, le=150, description="Edad de la persona")

class PersonaResponse(PersonaBase):
    """Model for persona response"""
    id: int
