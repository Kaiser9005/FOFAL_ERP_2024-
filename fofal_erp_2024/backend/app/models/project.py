from sqlalchemy import Column, String, Float, Enum, JSON, ForeignKey, Text, Numeric, Integer, Boolean, Date, DateTime
from sqlalchemy.orm import relationship
from .base import Base
import enum
from datetime import datetime
from typing import Optional
from sqlalchemy.dialects.postgresql import UUID

class StatutProjet(str, enum.Enum):
    """Statuts possibles d'un projet"""
    PLANIFIE = "PLANIFIE"
    EN_COURS = "EN_COURS"
    EN_PAUSE = "EN_PAUSE"
    TERMINE = "TERMINE"
    ANNULE = "ANNULE"

class PrioriteProjet(str, enum.Enum):
    """Niveaux de priorité pour les projets"""
    BASSE = "BASSE"
    MOYENNE = "MOYENNE"
    HAUTE = "HAUTE"
    CRITIQUE = "CRITIQUE"

class TypeProjet(str, enum.Enum):
    """Types de projets agricoles"""
    EXPANSION = "EXPANSION"
    AMELIORATION = "AMELIORATION"
    MAINTENANCE = "MAINTENANCE"
    RECHERCHE = "RECHERCHE"
    FORMATION = "FORMATION"

class Projet(Base):
    """Modèle représentant un projet"""
    __tablename__ = "projets"

    code = Column(String(50), unique=True, nullable=False)
    nom = Column(String(200), nullable=False)
    description = Column(Text)
    type = Column(Enum(TypeProjet), nullable=False)
    priorite = Column(Enum(PrioriteProjet), default=PrioriteProjet.MOYENNE)
    statut = Column(Enum(StatutProjet), default=StatutProjet.PLANIFIE)
    
    date_debut = Column(Date, nullable=False)
    date_fin_prevue = Column(Date, nullable=False)
    date_fin_reelle = Column(Date)
    
    budget_prevu = Column(Numeric(15, 2))
    budget_consomme = Column(Numeric(15, 2), default=0)
    
    responsable_id = Column(UUID(as_uuid=True), ForeignKey("employes.id"), nullable=False)
    parcelle_id = Column(UUID(as_uuid=True), ForeignKey("parcelles.id"))
    
    objectifs = Column(JSON)
    risques = Column(JSON)
    indicateurs = Column(JSON)
    
    # Relations
    responsable = relationship("Employe", back_populates="projets_diriges")
    parcelle = relationship("Parcelle", back_populates="projets")
    taches = relationship("Tache", back_populates="projet")
    ressources = relationship("RessourceProjet", back_populates="projet")
    documents = relationship("DocumentProjet", back_populates="projet")

class StatutTache(str, enum.Enum):
    """Statuts possibles d'une tâche"""
    A_FAIRE = "A_FAIRE"
    EN_COURS = "EN_COURS"
    EN_REVUE = "EN_REVUE"
    TERMINE = "TERMINE"
    BLOQUE = "BLOQUE"

class PrioriteTache(str, enum.Enum):
    """Niveaux de priorité pour les tâches"""
    BASSE = "BASSE"
    MOYENNE = "MOYENNE"
    HAUTE = "HAUTE"
    URGENTE = "URGENTE"

class Tache(Base):
    """Modèle représentant une tâche de projet"""
    __tablename__ = "taches"

    projet_id = Column(UUID(as_uuid=True), ForeignKey("projets.id"), nullable=False)
    titre = Column(String(200), nullable=False)
    description = Column(Text)
    priorite = Column(Enum(PrioriteTache), default=PrioriteTache.MOYENNE)
    statut = Column(Enum(StatutTache), default=StatutTache.A_FAIRE)
    
    date_debut = Column(Date)
    date_fin_prevue = Column(Date)
    date_fin_reelle = Column(Date)
    
    assignee_a_id = Column(UUID(as_uuid=True), ForeignKey("employes.id"))
    tache_parente_id = Column(UUID(as_uuid=True), ForeignKey("taches.id"))
    
    temps_estime = Column(Numeric(5, 2))  # En heures
    temps_passe = Column(Numeric(5, 2), default=0)
    progression = Column(Integer, default=0)  # Pourcentage
    
    # Relations
    projet = relationship("Projet", back_populates="taches")
    assignee = relationship("Employe", back_populates="taches_assignees")
    tache_parente = relationship("Tache", remote_side=[id])
    sous_taches = relationship("Tache")

class TypeRessource(str, enum.Enum):
    """Types de ressources pour les projets"""
    HUMAINE = "HUMAINE"
    MATERIELLE = "MATERIELLE"
    FINANCIERE = "FINANCIERE"

class RessourceProjet(Base):
    """Modèle représentant une ressource allouée à un projet"""
    __tablename__ = "ressources_projet"

    projet_id = Column(UUID(as_uuid=True), ForeignKey("projets.id"), nullable=False)
    type_ressource = Column(Enum(TypeRessource), nullable=False)
    description = Column(String(200), nullable=False)
    
    employe_id = Column(UUID(as_uuid=True), ForeignKey("employes.id"))
    produit_id = Column(UUID(as_uuid=True), ForeignKey("produits.id"))
    
    quantite = Column(Numeric(10, 2))
    unite = Column(String(50))
    cout = Column(Numeric(15, 2))
    
    date_debut = Column(Date)
    date_fin = Column(Date)
    
    # Relations
    projet = relationship("Projet", back_populates="ressources")
    employe = relationship("Employe")
    produit = relationship("Produit")

class TypeDocument(str, enum.Enum):
    """Types de documents de projet"""
    SPECIFICATION = "SPECIFICATION"
    RAPPORT = "RAPPORT"
    PLAN = "PLAN"
    BUDGET = "BUDGET"
    CONTRAT = "CONTRAT"
    AUTRE = "AUTRE"

class DocumentProjet(Base):
    """Modèle représentant un document de projet"""
    __tablename__ = "documents_projet"

    projet_id = Column(UUID(as_uuid=True), ForeignKey("projets.id"), nullable=False)
    type = Column(Enum(TypeDocument), nullable=False)
    titre = Column(String(200), nullable=False)
    description = Column(Text)
    fichier = Column(String(200))  # Chemin vers le fichier
    version = Column(String(20))
    date_creation = Column(DateTime, default=datetime.utcnow)
    cree_par_id = Column(UUID(as_uuid=True), ForeignKey("employes.id"))
    
    # Relations
    projet = relationship("Projet", back_populates="documents")
    cree_par = relationship("Employe")
