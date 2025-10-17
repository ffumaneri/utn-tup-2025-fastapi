from abc import ABC, abstractmethod
from typing import List, Optional
from sqlmodel import Session, select
from models import Persona, PersonaCreate, PersonaUpdate, Pais, PaisCreate, PaisUpdate

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


class PaisRepositoryInterface(ABC):
    """Interface for Pais repository"""
    
    @abstractmethod
    def create(self, pais: PaisCreate) -> Pais:
        pass
    
    @abstractmethod
    def get_by_id(self, pais_id: int) -> Optional[Pais]:
        pass
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Pais]:
        pass
    
    @abstractmethod
    def update(self, pais_id: int, pais_update: PaisUpdate) -> Optional[Pais]:
        pass
    
    @abstractmethod
    def delete(self, pais_id: int) -> bool:
        pass


class PaisRepository(PaisRepositoryInterface):
    """Repository for Pais entity using SQLModel"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def create(self, pais: PaisCreate) -> Pais:
        """Create a new pais"""
        db_pais = Pais.model_validate(pais)
        self.session.add(db_pais)
        self.session.commit()
        self.session.refresh(db_pais)
        return db_pais
    
    def get_by_id(self, pais_id: int) -> Optional[Pais]:
        """Get pais by ID"""
        statement = select(Pais).where(Pais.id == pais_id)
        return self.session.exec(statement).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Pais]:
        """Get all paises with pagination"""
        statement = select(Pais).offset(skip).limit(limit)
        return self.session.exec(statement).all()
    
    def update(self, pais_id: int, pais_update: PaisUpdate) -> Optional[Pais]:
        """Update pais by ID"""
        db_pais = self.get_by_id(pais_id)
        if not db_pais:
            return None
        
        # Update only provided fields
        pais_data = pais_update.model_dump(exclude_unset=True)
        for key, value in pais_data.items():
            setattr(db_pais, key, value)
        
        self.session.add(db_pais)
        self.session.commit()
        self.session.refresh(db_pais)
        return db_pais
    
    def delete(self, pais_id: int) -> bool:
        """Delete pais by ID"""
        db_pais = self.get_by_id(pais_id)
        if not db_pais:
            return False
        
        self.session.delete(db_pais)
        self.session.commit()
        return True
