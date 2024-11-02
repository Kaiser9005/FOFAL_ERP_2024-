from sqlalchemy import Column, String, Float, Enum, JSON, ForeignKey, Text, Numeric, Integer, Boolean, Date, DateTime
from sqlalchemy.orm import relationship
from .base import Base
import enum
from datetime import datetime
from typing import Optional
from sqlalchemy.dialects.postgresql import UUID

class TypeCompteOHADA(str, enum.Enum):
    """Types de comptes selon le plan comptable OHADA"""
    ACTIF = "ACTIF"
    PASSIF = "PASSIF"
    CHARGE = "CHARGE"
    PRODUIT = "PRODUIT"

class ClasseCompteOHADA(str, enum.Enum):
    """Classes de comptes selon le plan comptable OHADA"""
    CLASSE_1 = "1"  # Comptes de ressources durables
    CLASSE_2 = "2"  # Comptes d'actif immobilisé
    CLASSE_3 = "3"  # Comptes de stocks
    CLASSE_4 = "4"  # Comptes de tiers
    CLASSE_5 = "5"  # Comptes de trésorerie
    CLASSE_6 = "6"  # Comptes de charges
    CLASSE_7 = "7"  # Comptes de produits

class PlanComptable(Base):
    """Modèle représentant le plan comptable OHADA"""
    __tablename__ = "plan_comptable"

    numero = Column(String(10), unique=True, nullable=False)
    intitule = Column(String(200), nullable=False)
    classe = Column(Enum(ClasseCompteOHADA), nullable=False)
    type = Column(Enum(TypeCompteOHADA), nullable=False)
    niveau = Column(Integer, nullable=False)  # Niveau hiérarchique
    compte_parent_id = Column(UUID(as_uuid=True), ForeignKey("plan_comptable.id"))
    actif = Column(Boolean, default=True)
    
    # Relations
    compte_parent = relationship("PlanComptable", remote_side=[id])
    sous_comptes = relationship("PlanComptable")
    ecritures = relationship("EcritureComptable", back_populates="compte")

class TypePiece(str, enum.Enum):
    """Types de pièces comptables"""
    FACTURE = "FACTURE"
    AVOIR = "AVOIR"
    RECU = "RECU"
    VIREMENT = "VIREMENT"
    JOURNAL = "JOURNAL"
    AUTRE = "AUTRE"

class EcritureComptable(Base):
    """Modèle représentant une écriture comptable"""
    __tablename__ = "ecritures_comptables"

    date = Column(Date, nullable=False)
    numero_piece = Column(String(50), nullable=False)
    type_piece = Column(Enum(TypePiece), nullable=False)
    compte_id = Column(UUID(as_uuid=True), ForeignKey("plan_comptable.id"), nullable=False)
    libelle = Column(String(200), nullable=False)
    debit = Column(Numeric(15, 2), default=0)
    credit = Column(Numeric(15, 2), default=0)
    periode_comptable = Column(String(7), nullable=False)  # Format: YYYY-MM
    reference_transaction = Column(UUID(as_uuid=True), ForeignKey("transactions.id"))
    piece_jointe = Column(String(200))  # Chemin vers le document
    
    # Relations
    compte = relationship("PlanComptable", back_populates="ecritures")
    journal = relationship("JournalComptable", back_populates="ecritures")

class TypeJournal(str, enum.Enum):
    """Types de journaux comptables"""
    ACHATS = "ACHATS"
    VENTES = "VENTES"
    BANQUE = "BANQUE"
    CAISSE = "CAISSE"
    OPERATIONS_DIVERSES = "OPERATIONS_DIVERSES"

class JournalComptable(Base):
    """Modèle représentant un journal comptable"""
    __tablename__ = "journaux_comptables"

    code = Column(String(10), unique=True, nullable=False)
    nom = Column(String(100), nullable=False)
    type = Column(Enum(TypeJournal), nullable=False)
    description = Column(Text)
    actif = Column(Boolean, default=True)
    
    # Relations
    ecritures = relationship("EcritureComptable", back_populates="journal")

class ExerciceComptable(Base):
    """Modèle représentant un exercice comptable"""
    __tablename__ = "exercices_comptables"

    annee = Column(Integer, nullable=False, unique=True)
    date_debut = Column(Date, nullable=False)
    date_fin = Column(Date, nullable=False)
    cloture = Column(Boolean, default=False)
    date_cloture = Column(DateTime)
    cloture_par_id = Column(UUID(as_uuid=True), ForeignKey("employes.id"))
    
    # Relations
    cloture_par = relationship("Employe")
    balances = relationship("Balance", back_populates="exercice")

class Balance(Base):
    """Modèle représentant une balance comptable"""
    __tablename__ = "balances"

    exercice_id = Column(UUID(as_uuid=True), ForeignKey("exercices_comptables.id"), nullable=False)
    compte_id = Column(UUID(as_uuid=True), ForeignKey("plan_comptable.id"), nullable=False)
    periode = Column(String(7), nullable=False)  # Format: YYYY-MM
    debit_ouverture = Column(Numeric(15, 2), default=0)
    credit_ouverture = Column(Numeric(15, 2), default=0)
    debit_mouvement = Column(Numeric(15, 2), default=0)
    credit_mouvement = Column(Numeric(15, 2), default=0)
    debit_cumule = Column(Numeric(15, 2), default=0)
    credit_cumule = Column(Numeric(15, 2), default=0)
    solde_debiteur = Column(Numeric(15, 2), default=0)
    solde_crediteur = Column(Numeric(15, 2), default=0)
    
    # Relations
    exercice = relationship("ExerciceComptable", back_populates="balances")
    compte = relationship("PlanComptable")

class DocumentComptable(Base):
    """Modèle représentant un document comptable"""
    __tablename__ = "documents_comptables"

    type = Column(String(50), nullable=False)  # Bilan, Compte de résultat, etc.
    periode = Column(String(7), nullable=False)  # Format: YYYY-MM
    date_generation = Column(DateTime, default=datetime.utcnow)
    contenu = Column(JSON)  # Structure du document
    fichier = Column(String(200))  # Chemin vers le fichier généré
    genere_par_id = Column(UUID(as_uuid=True), ForeignKey("employes.id"))
    
    # Relations
    genere_par = relationship("Employe")
