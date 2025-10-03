from abc import ABC, abstractmethod
from typing import List, Optional
from sqlmodel import Session, select
from models import Persona, PersonaCreate, PersonaUpdate

class PersonaRepositoryInterface(ABC):
    """Interface for Persona repository"""
    
    @abstractmethod
    def create(self, persona: PersonaCreate) -> Persona:
        pass
    
    @abstractmethod
    def get_by_id(self, persona_id: int) -> Optional[Persona]:
        pass
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Persona]:
        pass
    
    @abstractmethod
    def update(self, persona_id: int, persona_update: PersonaUpdate) -> Optional[Persona]:
        pass
    
    @abstractmethod
    def delete(self, persona_id: int) -> bool:
        pass

class PersonaRepository(PersonaRepositoryInterface):
    """Repository for Persona entity using SQLModel"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def create(self, persona: PersonaCreate) -> Persona:
        """Create a new persona"""
        db_persona = Persona.model_validate(persona)
        self.session.add(db_persona)
        self.session.commit()
        self.session.refresh(db_persona)
        return db_persona
    
    def get_by_id(self, persona_id: int) -> Optional[Persona]:
        """Get persona by ID"""
        statement = select(Persona).where(Persona.id == persona_id)
        return self.session.exec(statement).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Persona]:
        """Get all personas with pagination"""
        statement = select(Persona).offset(skip).limit(limit)
        return self.session.exec(statement).all()
    
    def update(self, persona_id: int, persona_update: PersonaUpdate) -> Optional[Persona]:
        """Update persona by ID"""
        db_persona = self.get_by_id(persona_id)
        if not db_persona:
            return None
        
        # Update only provided fields
        persona_data = persona_update.model_dump(exclude_unset=True)
        for key, value in persona_data.items():
            setattr(db_persona, key, value)
        
        self.session.add(db_persona)
        self.session.commit()
        self.session.refresh(db_persona)
        return db_persona
    
    def delete(self, persona_id: int) -> bool:
        """Delete persona by ID"""
        db_persona = self.get_by_id(persona_id)
        if not db_persona:
            return False
        
        self.session.delete(db_persona)
        self.session.commit()
        return True
