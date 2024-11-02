from sqlalchemy import Column, String, Float, Enum, JSON, ForeignKey, Text, Numeric, Integer
from sqlalchemy.orm import relationship
from .base import Base
import enum
from datetime import datetime
from typing import Optional
from sqlalchemy.dialects.postgresql import UUID

class CategoryProduit(str, enum.Enum):
    """Catégories de produits dans l'inventaire"""
    INTRANT = "INTRANT"          # Engrais, pesticides, etc.
    EQUIPEMENT = "EQUIPEMENT"    # Outils, machines
    RECOLTE = "RECOLTE"         # Produits récoltés
    EMBALLAGE = "EMBALLAGE"     # Matériel d'emballage
    PIECE_RECHANGE = "PIECE_RECHANGE"  # Pièces de rechange pour équipements

class UniteMesure(str, enum.Enum):
    """Unités de mesure pour les produits"""
    KG = "KG"
    LITRE = "LITRE"
    UNITE = "UNITE"
    TONNE = "TONNE"
    METRE = "METRE"
    METRE_CARRE = "METRE_CARRE"
    HECTARE = "HECTARE"

class Produit(Base):
    """Modèle représentant un produit dans l'inventaire"""
    __tablename__ = "produits"

    code = Column(String(50), unique=True, index=True, nullable=False)
    nom = Column(String(100), nullable=False)
    categorie = Column(Enum(CategoryProduit), nullable=False)
    description = Column(Text)
    unite_mesure = Column(Enum(UniteMesure), nullable=False)
    seuil_alerte = Column(Numeric(10, 2))
    prix_unitaire = Column(Numeric(10, 2))
    specifications = Column(JSON)  # Caractéristiques techniques
    
    # Relations
    mouvements = relationship("MouvementStock", back_populates="produit")
    stocks = relationship("Stock", back_populates="produit")

class TypeMouvement(str, enum.Enum):
    """Types de mouvements de stock"""
    ENTREE = "ENTREE"
    SORTIE = "SORTIE"
    AJUSTEMENT = "AJUSTEMENT"
    PERTE = "PERTE"
    TRANSFERT = "TRANSFERT"

class MouvementStock(Base):
    """Modèle représentant un mouvement de stock"""
    __tablename__ = "mouvements_stock"

    produit_id = Column(UUID(as_uuid=True), ForeignKey("produits.id"), nullable=False)
    type_mouvement = Column(Enum(TypeMouvement), nullable=False)
    quantite = Column(Numeric(10, 2), nullable=False)
    date_mouvement = Column(DateTime, default=datetime.utcnow, nullable=False)
    entrepot_source_id = Column(UUID(as_uuid=True), ForeignKey("entrepots.id"))
    entrepot_destination_id = Column(UUID(as_uuid=True), ForeignKey("entrepots.id"))
    responsable_id = Column(UUID(as_uuid=True), ForeignKey("employes.id"))
    reference_document = Column(String(100))  # Bon de livraison, commande, etc.
    notes = Column(Text)
    cout_unitaire = Column(Numeric(10, 2))  # Pour valorisation du stock

    # Relations
    produit = relationship("Produit", back_populates="mouvements")
    entrepot_source = relationship("Entrepot", foreign_keys=[entrepot_source_id])
    entrepot_destination = relationship("Entrepot", foreign_keys=[entrepot_destination_id])
    responsable = relationship("Employe", back_populates="mouvements_stock")

class Entrepot(Base):
    """Modèle représentant un entrepôt"""
    __tablename__ = "entrepots"

    nom = Column(String(100), nullable=False)
    code = Column(String(50), unique=True, index=True, nullable=False)
    localisation = Column(String(200))
    capacite_max = Column(Numeric(10, 2))  # en m³ ou kg selon le type
    responsable_id = Column(UUID(as_uuid=True), ForeignKey("employes.id"))
    type_stockage = Column(String(50))  # Froid, sec, etc.
    conditions_stockage = Column(JSON)  # Température, humidité, etc.

    # Relations
    stocks = relationship("Stock", back_populates="entrepot")
    responsable = relationship("Employe", back_populates="entrepots_geres")

class Stock(Base):
    """Modèle représentant le stock actuel d'un produit dans un entrepôt"""
    __tablename__ = "stocks"

    produit_id = Column(UUID(as_uuid=True), ForeignKey("produits.id"), nullable=False)
    entrepot_id = Column(UUID(as_uuid=True), ForeignKey("entrepots.id"), nullable=False)
    quantite = Column(Numeric(10, 2), nullable=False, default=0)
    valeur_unitaire = Column(Numeric(10, 2))  # Prix moyen pondéré
    date_derniere_maj = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    emplacement = Column(String(50))  # Position dans l'entrepôt
    lot = Column(String(50))  # Numéro de lot pour traçabilité

    # Relations
    produit = relationship("Produit", back_populates="stocks")
    entrepot = relationship("Entrepot", back_populates="stocks")

class Inventaire(Base):
    """Modèle représentant un inventaire physique"""
    __tablename__ = "inventaires"

    date_inventaire = Column(DateTime, nullable=False)
    entrepot_id = Column(UUID(as_uuid=True), ForeignKey("entrepots.id"), nullable=False)
    responsable_id = Column(UUID(as_uuid=True), ForeignKey("employes.id"))
    statut = Column(String(50))  # En cours, Terminé, Validé
    notes = Column(Text)
    ecarts = Column(JSON)  # Liste des écarts constatés

    # Relations
    entrepot = relationship("Entrepot")
    responsable = relationship("Employe")
    lignes = relationship("LigneInventaire", back_populates="inventaire")

class LigneInventaire(Base):
    """Modèle représentant une ligne d'inventaire"""
    __tablename__ = "lignes_inventaire"

    inventaire_id = Column(UUID(as_uuid=True), ForeignKey("inventaires.id"), nullable=False)
    produit_id = Column(UUID(as_uuid=True), ForeignKey("produits.id"), nullable=False)
    quantite_theorique = Column(Numeric(10, 2))
    quantite_physique = Column(Numeric(10, 2))
    ecart = Column(Numeric(10, 2))
    justification = Column(Text)

    # Relations
    inventaire = relationship("Inventaire", back_populates="lignes")
    produit = relationship("Produit")
