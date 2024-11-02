from sqlalchemy import Column, String, Float, Date, Enum, JSON, ForeignKey, Text, Numeric
from sqlalchemy.orm import relationship
from .base import Base
import enum
from datetime import date
from typing import Optional

class CultureType(str, enum.Enum):
    """Types de cultures disponibles"""
    PALMIER = "PALMIER"
    PAPAYE = "PAPAYE"
    CACAO = "CACAO"
    BANANE = "BANANE"
    MAIS = "MAIS"

class ParcelleStatus(str, enum.Enum):
    """États possibles d'une parcelle"""
    ACTIVE = "ACTIVE"
    EN_REPOS = "EN_REPOS"
    EN_PREPARATION = "EN_PREPARATION"

class Parcelle(Base):
    """Modèle représentant une parcelle agricole"""
    __tablename__ = "parcelles"

    code = Column(String(50), unique=True, index=True, nullable=False)
    culture_type = Column(Enum(CultureType), nullable=False)
    surface_hectares = Column(Numeric(10, 2), nullable=False)
    date_plantation = Column(Date, nullable=False)
    statut = Column(Enum(ParcelleStatus), default=ParcelleStatus.EN_PREPARATION)
    coordonnees_gps = Column(JSON)
    responsable_id = Column(UUID(as_uuid=True), ForeignKey("employes.id"))
    
    # Relations
    responsable = relationship("Employe", back_populates="parcelles")
    cycles_culture = relationship("CycleCulture", back_populates="parcelle")
    recoltes = relationship("Recolte", back_populates="parcelle")

class CycleCulture(Base):
    """Modèle représentant un cycle de culture"""
    __tablename__ = "cycles_culture"

    parcelle_id = Column(UUID(as_uuid=True), ForeignKey("parcelles.id"), nullable=False)
    date_debut = Column(Date, nullable=False)
    date_fin = Column(Date)
    rendement_prevu = Column(Numeric(10, 2))
    rendement_reel = Column(Numeric(10, 2))
    notes = Column(Text)

    # Relations
    parcelle = relationship("Parcelle", back_populates="cycles_culture")
    activites = relationship("ActiviteCulturale", back_populates="cycle")

class QualiteRecolte(str, enum.Enum):
    """Niveaux de qualité pour les récoltes"""
    A = "A"  # Premium
    B = "B"  # Standard
    C = "C"  # Basse qualité

class Recolte(Base):
    """Modèle représentant une récolte"""
    __tablename__ = "recoltes"

    parcelle_id = Column(UUID(as_uuid=True), ForeignKey("parcelles.id"), nullable=False)
    date_recolte = Column(Date, nullable=False)
    quantite_kg = Column(Numeric(10, 2), nullable=False)
    qualite = Column(Enum(QualiteRecolte), nullable=False)
    equipe_recolte = Column(JSON)  # Liste des IDs des employés
    conditions_meteo = Column(JSON)
    notes = Column(Text)

    # Relations
    parcelle = relationship("Parcelle", back_populates="recoltes")

class TypeActivite(str, enum.Enum):
    """Types d'activités culturales"""
    FERTILISATION = "FERTILISATION"
    TRAITEMENT = "TRAITEMENT"
    TAILLE = "TAILLE"
    DESHERBAGE = "DESHERBAGE"
    IRRIGATION = "IRRIGATION"
    AUTRE = "AUTRE"

class ActiviteCulturale(Base):
    """Modèle représentant une activité culturale"""
    __tablename__ = "activites_culturales"

    cycle_id = Column(UUID(as_uuid=True), ForeignKey("cycles_culture.id"), nullable=False)
    type_activite = Column(Enum(TypeActivite), nullable=False)
    date_realisation = Column(Date, nullable=False)
    produits_utilises = Column(JSON)  # Liste des produits et quantités
    responsable_id = Column(UUID(as_uuid=True), ForeignKey("employes.id"))
    notes = Column(Text)

    # Relations
    cycle = relationship("CycleCulture", back_populates="activites")
    responsable = relationship("Employe", back_populates="activites_realisees")
