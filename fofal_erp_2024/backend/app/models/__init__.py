from .base import Base
from .production import (
    Parcelle, CycleCulture, Recolte, ActiviteCulturale,
    CultureType, ParcelleStatus, QualiteRecolte, TypeActivite
)
from .inventory import (
    Produit, MouvementStock, Entrepot, Stock, Inventaire, LigneInventaire,
    CategoryProduit, UniteMesure, TypeMouvement
)
from .hr import (
    Employe, Contrat, Conge, Presence, Paie,
    DepartementType, StatutEmploye, TypeContrat, TypeConge, StatutConge, TypePresence
)
from .finance import (
    Transaction, Compte, Budget, PrevisionTresorerie, Exercice, IndicateurFinancier,
    TypeTransaction, StatutTransaction, CategorieTransaction, TypeCompte
)
from .accounting import (
    PlanComptable, EcritureComptable, JournalComptable, ExerciceComptable,
    Balance, DocumentComptable, TypeCompteOHADA, ClasseCompteOHADA,
    TypePiece, TypeJournal
)
from .project import (
    Projet, Tache, RessourceProjet, DocumentProjet,
    StatutProjet, PrioriteProjet, TypeProjet, StatutTache,
    PrioriteTache, TypeRessource, TypeDocument
)

# Mise en place des relations entre les modèles
Employe.parcelles = relationship("Parcelle", back_populates="responsable")
Employe.activites_realisees = relationship("ActiviteCulturale", back_populates="responsable")
Employe.entrepots_geres = relationship("Entrepot", back_populates="responsable")
Employe.mouvements_stock = relationship("MouvementStock", back_populates="responsable")
Employe.projets_diriges = relationship("Projet", back_populates="responsable")
Employe.taches_assignees = relationship("Tache", back_populates="assignee")

# Configuration des métadonnées pour la création des tables
metadata = Base.metadata

# Liste de tous les modèles pour faciliter les migrations
__all__ = [
    # Production
    'Parcelle', 'CycleCulture', 'Recolte', 'ActiviteCulturale',
    'CultureType', 'ParcelleStatus', 'QualiteRecolte', 'TypeActivite',
    
    # Inventory
    'Produit', 'MouvementStock', 'Entrepot', 'Stock', 'Inventaire', 'LigneInventaire',
    'CategoryProduit', 'UniteMesure', 'TypeMouvement',
    
    # HR
    'Employe', 'Contrat', 'Conge', 'Presence', 'Paie',
    'DepartementType', 'StatutEmploye', 'TypeContrat', 'TypeConge', 'StatutConge', 'TypePresence',
    
    # Finance
    'Transaction', 'Compte', 'Budget', 'PrevisionTresorerie', 'Exercice', 'IndicateurFinancier',
    'TypeTransaction', 'StatutTransaction', 'CategorieTransaction', 'TypeCompte',
    
    # Accounting
    'PlanComptable', 'EcritureComptable', 'JournalComptable', 'ExerciceComptable',
    'Balance', 'DocumentComptable', 'TypeCompteOHADA', 'ClasseCompteOHADA',
    'TypePiece', 'TypeJournal',
    
    # Project
    'Projet', 'Tache', 'RessourceProjet', 'DocumentProjet',
    'StatutProjet', 'PrioriteProjet', 'TypeProjet', 'StatutTache',
    'PrioriteTache', 'TypeRessource', 'TypeDocument',
]
