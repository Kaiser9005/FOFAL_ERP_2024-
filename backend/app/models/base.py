from datetime import datetime
from typing import Any
from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID

@as_declarative()
class Base:
    """
    Classe de base pour tous les modèles SQLAlchemy.
    Fournit des fonctionnalités communes à tous les modèles.
    """
    id: Any
    created_at: datetime
    updated_at: datetime
    
    # Génère automatiquement le nom de la table à partir du nom de la classe
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    # Colonnes communes à tous les modèles
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def dict(self):
        """
        Convertit le modèle en dictionnaire.
        Utile pour la sérialisation.
        """
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }

    def update(self, **kwargs):
        """
        Met à jour les attributs du modèle avec les valeurs fournies.
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
