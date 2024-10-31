from sqlalchemy import Column, String, JSON, Boolean, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from .base import Base
import enum
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID

class TypeParametre(str, enum.Enum):
    """Types de paramètres système"""
    GENERAL = "GENERAL"
    MODULE = "MODULE"
    UTILISATEUR = "UTILISATEUR"

class ModuleSysteme(str, enum.Enum):
    """Modules du système"""
    PRODUCTION = "PRODUCTION"
    INVENTAIRE = "INVENTAIRE"
    RH = "RH"
    FINANCE = "FINANCE"
    COMPTABILITE = "COMPTABILITE"
    PARAMETRAGE = "PARAMETRAGE"

class Parametre(Base):
    """Modèle pour les paramètres système"""
    __tablename__ = "parametres"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    code = Column(String(50), unique=True, nullable=False)
    libelle = Column(String(200), nullable=False)
    description = Column(Text)
    type_parametre = Column(Enum(TypeParametre), nullable=False)
    module = Column(Enum(ModuleSysteme), nullable=True)
    valeur = Column(JSON, nullable=False)  # Stockage flexible des valeurs
    modifiable = Column(Boolean, default=True)
    visible = Column(Boolean, default=True)
    ordre = Column(Integer, default=0)
    categorie = Column(String(50))  # Pour grouper les paramètres

class ConfigurationModule(Base):
    """Modèle pour la configuration des modules"""
    __tablename__ = "configurations_modules"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    module = Column(Enum(ModuleSysteme), unique=True, nullable=False)
    actif = Column(Boolean, default=True)
    configuration = Column(JSON)  # Configuration spécifique au module
    ordre_affichage = Column(Integer, default=0)
    icone = Column(String(50))
    couleur = Column(String(20))
    roles_autorises = Column(JSON)  # Liste des rôles ayant accès au module