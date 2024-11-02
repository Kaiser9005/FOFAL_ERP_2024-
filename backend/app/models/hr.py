from sqlalchemy import Column, String, Float, Enum, JSON, ForeignKey, Text, Numeric, Integer, Boolean, Date, DateTime
from sqlalchemy.orm import relationship
from .base import Base
import enum
from datetime import datetime, date
from typing import Optional
from sqlalchemy.dialects.postgresql import UUID

class DepartementType(str, enum.Enum):
    """Types de départements dans l'entreprise"""
    PRODUCTION = "PRODUCTION"
    MAINTENANCE = "MAINTENANCE"
    ADMINISTRATION = "ADMINISTRATION"
    FINANCE = "FINANCE"
    LOGISTIQUE = "LOGISTIQUE"
    QUALITE = "QUALITE"
    RH = "RH"

class StatutEmploye(str, enum.Enum):
    """Statuts possibles d'un employé"""
    ACTIF = "ACTIF"
    INACTIF = "INACTIF"
    CONGE = "CONGE"
    SUSPENDU = "SUSPENDU"

class TypeContrat(str, enum.Enum):
    """Types de contrats de travail"""
    CDI = "CDI"
    CDD = "CDD"
    STAGE = "STAGE"
    TEMPORAIRE = "TEMPORAIRE"

class Employe(Base):
    """Modèle représentant un employé"""
    __tablename__ = "employes"

    matricule = Column(String(50), unique=True, index=True, nullable=False)
    nom = Column(String(100), nullable=False)
    prenom = Column(String(100), nullable=False)
    date_naissance = Column(Date, nullable=False)
    lieu_naissance = Column(String(100))
    sexe = Column(String(1))
    adresse = Column(String(200))
    telephone = Column(String(20))
    email = Column(String(100))
    
    # Informations professionnelles
    departement = Column(Enum(DepartementType), nullable=False)
    poste = Column(String(100), nullable=False)
    date_embauche = Column(Date, nullable=False)
    type_contrat = Column(Enum(TypeContrat), nullable=False)
    statut = Column(Enum(StatutEmploye), default=StatutEmploye.ACTIF)
    superieur_id = Column(UUID(as_uuid=True), ForeignKey("employes.id"))
    
    # Informations de paie
    salaire_base = Column(Numeric(10, 2), nullable=False)
    compte_bancaire = Column(JSON)  # Informations bancaires
    
    # Relations
    superieur = relationship("Employe", remote_side=[id])
    subordonnees = relationship("Employe")
    contrats = relationship("Contrat", back_populates="employe")
    paies = relationship("Paie", back_populates="employe")
    conges = relationship("Conge", back_populates="employe")
    presences = relationship("Presence", back_populates="employe")

class Contrat(Base):
    """Modèle représentant un contrat de travail"""
    __tablename__ = "contrats"

    employe_id = Column(UUID(as_uuid=True), ForeignKey("employes.id"), nullable=False)
    type_contrat = Column(Enum(TypeContrat), nullable=False)
    date_debut = Column(Date, nullable=False)
    date_fin = Column(Date)
    poste = Column(String(100), nullable=False)
    salaire_base = Column(Numeric(10, 2), nullable=False)
    avantages = Column(JSON)  # Liste des avantages
    conditions = Column(Text)  # Conditions particulières
    statut = Column(String(50))  # Actif, Terminé, etc.

    # Relations
    employe = relationship("Employe", back_populates="contrats")

class TypeConge(str, enum.Enum):
    """Types de congés"""
    ANNUEL = "ANNUEL"
    MALADIE = "MALADIE"
    MATERNITE = "MATERNITE"
    SPECIAL = "SPECIAL"
    SANS_SOLDE = "SANS_SOLDE"

class StatutConge(str, enum.Enum):
    """Statuts possibles d'une demande de congé"""
    EN_ATTENTE = "EN_ATTENTE"
    APPROUVE = "APPROUVE"
    REFUSE = "REFUSE"
    ANNULE = "ANNULE"

class Conge(Base):
    """Modèle représentant une demande de congé"""
    __tablename__ = "conges"

    employe_id = Column(UUID(as_uuid=True), ForeignKey("employes.id"), nullable=False)
    type_conge = Column(Enum(TypeConge), nullable=False)
    date_debut = Column(Date, nullable=False)
    date_fin = Column(Date, nullable=False)
    nb_jours = Column(Integer, nullable=False)
    motif = Column(Text)
    statut = Column(Enum(StatutConge), default=StatutConge.EN_ATTENTE)
    approuve_par_id = Column(UUID(as_uuid=True), ForeignKey("employes.id"))
    date_approbation = Column(DateTime)
    commentaire = Column(Text)

    # Relations
    employe = relationship("Employe", back_populates="conges", foreign_keys=[employe_id])
    approuve_par = relationship("Employe", foreign_keys=[approuve_par_id])

class TypePresence(str, enum.Enum):
    """Types de présence"""
    PRESENT = "PRESENT"
    ABSENT = "ABSENT"
    RETARD = "RETARD"
    CONGE = "CONGE"
    MISSION = "MISSION"

class Presence(Base):
    """Modèle représentant la présence d'un employé"""
    __tablename__ = "presences"

    employe_id = Column(UUID(as_uuid=True), ForeignKey("employes.id"), nullable=False)
    date = Column(Date, nullable=False)
    type_presence = Column(Enum(TypePresence), nullable=False)
    heure_arrivee = Column(DateTime)
    heure_depart = Column(DateTime)
    heures_travaillees = Column(Numeric(4, 2))
    justification = Column(Text)

    # Relations
    employe = relationship("Employe", back_populates="presences")

class Paie(Base):
    """Modèle représentant une fiche de paie"""
    __tablename__ = "paies"

    employe_id = Column(UUID(as_uuid=True), ForeignKey("employes.id"), nullable=False)
    periode = Column(String(7), nullable=False)  # Format: YYYY-MM
    salaire_base = Column(Numeric(10, 2), nullable=False)
    heures_supp = Column(Numeric(10, 2), default=0)
    primes = Column(JSON)  # Différentes primes
    deductions = Column(JSON)  # Différentes déductions
    cotisations = Column(JSON)  # Cotisations sociales
    impositions = Column(JSON)  # Impositions
    net_a_payer = Column(Numeric(10, 2), nullable=False)
    date_paiement = Column(DateTime)
    methode_paiement = Column(String(50))
    reference_paiement = Column(String(100))

    # Relations
    employe = relationship("Employe", back_populates="paies")
