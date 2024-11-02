from sqlalchemy import Column, String, Float, Enum, JSON, ForeignKey, Text, Numeric, Integer, Boolean, Date, DateTime
from sqlalchemy.orm import relationship
from .base import Base
import enum
from datetime import datetime
from typing import Optional
from sqlalchemy.dialects.postgresql import UUID

class TypeTransaction(str, enum.Enum):
    """Types de transactions financières"""
    RECETTE = "RECETTE"
    DEPENSE = "DEPENSE"
    VIREMENT = "VIREMENT"
    AJUSTEMENT = "AJUSTEMENT"

class StatutTransaction(str, enum.Enum):
    """Statuts possibles d'une transaction"""
    EN_ATTENTE = "EN_ATTENTE"
    VALIDEE = "VALIDEE"
    REJETEE = "REJETEE"
    ANNULEE = "ANNULEE"

class CategorieTransaction(str, enum.Enum):
    """Catégories principales de transactions"""
    VENTE_PRODUITS = "VENTE_PRODUITS"
    ACHAT_INTRANTS = "ACHAT_INTRANTS"
    SALAIRES = "SALAIRES"
    MAINTENANCE = "MAINTENANCE"
    TRANSPORT = "TRANSPORT"
    SERVICES = "SERVICES"
    TAXES = "TAXES"
    AUTRE = "AUTRE"

class Transaction(Base):
    """Modèle représentant une transaction financière"""
    __tablename__ = "transactions"

    date = Column(DateTime, nullable=False, default=datetime.utcnow)
    type = Column(Enum(TypeTransaction), nullable=False)
    categorie = Column(Enum(CategorieTransaction), nullable=False)
    montant = Column(Numeric(15, 2), nullable=False)
    devise = Column(String(3), default="XAF")
    description = Column(Text)
    reference = Column(String(100), unique=True)
    statut = Column(Enum(StatutTransaction), default=StatutTransaction.EN_ATTENTE)
    
    compte_source_id = Column(UUID(as_uuid=True), ForeignKey("comptes.id"))
    compte_destination_id = Column(UUID(as_uuid=True), ForeignKey("comptes.id"))
    
    piece_justificative = Column(String(200))  # Chemin vers le document
    metadata = Column(JSON)  # Données supplémentaires
    
    # Relations
    compte_source = relationship("Compte", foreign_keys=[compte_source_id])
    compte_destination = relationship("Compte", foreign_keys=[compte_destination_id])

class TypeCompte(str, enum.Enum):
    """Types de comptes financiers"""
    BANQUE = "BANQUE"
    CAISSE = "CAISSE"
    EPARGNE = "EPARGNE"
    CREDIT = "CREDIT"

class Compte(Base):
    """Modèle représentant un compte financier"""
    __tablename__ = "comptes"

    numero = Column(String(50), unique=True, nullable=False)
    nom = Column(String(100), nullable=False)
    type = Column(Enum(TypeCompte), nullable=False)
    devise = Column(String(3), default="XAF")
    solde = Column(Numeric(15, 2), default=0)
    banque = Column(String(100))
    iban = Column(String(34))
    swift = Column(String(11))
    actif = Column(Boolean, default=True)
    
    # Relations
    transactions_source = relationship("Transaction", 
                                     foreign_keys=[Transaction.compte_source_id],
                                     back_populates="compte_source")
    transactions_destination = relationship("Transaction", 
                                          foreign_keys=[Transaction.compte_destination_id],
                                          back_populates="compte_destination")

class Budget(Base):
    """Modèle représentant un budget"""
    __tablename__ = "budgets"

    annee = Column(Integer, nullable=False)
    mois = Column(Integer, nullable=False)
    categorie = Column(Enum(CategorieTransaction), nullable=False)
    montant_prevu = Column(Numeric(15, 2), nullable=False)
    montant_realise = Column(Numeric(15, 2), default=0)
    notes = Column(Text)
    
    class Meta:
        unique_together = ('annee', 'mois', 'categorie')

class PrevisionTresorerie(Base):
    """Modèle représentant une prévision de trésorerie"""
    __tablename__ = "previsions_tresorerie"

    date = Column(Date, nullable=False)
    type = Column(Enum(TypeTransaction), nullable=False)
    montant_prevu = Column(Numeric(15, 2), nullable=False)
    montant_realise = Column(Numeric(15, 2))
    description = Column(Text)
    recurrent = Column(Boolean, default=False)
    frequence = Column(String(50))  # Mensuel, Hebdomadaire, etc.

class Exercice(Base):
    """Modèle représentant un exercice financier"""
    __tablename__ = "exercices"

    annee = Column(Integer, nullable=False, unique=True)
    date_debut = Column(Date, nullable=False)
    date_fin = Column(Date, nullable=False)
    cloture = Column(Boolean, default=False)
    date_cloture = Column(DateTime)
    resultat_net = Column(Numeric(15, 2))
    notes = Column(Text)

class IndicateurFinancier(Base):
    """Modèle représentant les indicateurs financiers"""
    __tablename__ = "indicateurs_financiers"

    date = Column(Date, nullable=False)
    chiffre_affaires = Column(Numeric(15, 2))
    benefice_net = Column(Numeric(15, 2))
    tresorerie = Column(Numeric(15, 2))
    dettes = Column(Numeric(15, 2))
    creances = Column(Numeric(15, 2))
    ratio_liquidite = Column(Numeric(5, 2))
    ratio_endettement = Column(Numeric(5, 2))
    marge_brute = Column(Numeric(5, 2))
    notes = Column(Text)
