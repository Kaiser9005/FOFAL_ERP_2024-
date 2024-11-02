# FOFAL ERP 2024 - Système de Gestion Agricole Intégré

## Vue d'ensemble
FOFAL ERP est un système de gestion intégré spécialement conçu pour FOFAL (Family Land), une entreprise agricole spécialisée dans la culture du palmier à huile (70 ha) et des papayes (10 ha). Le système permet une gestion complète des opérations agricoles, de la production à la commercialisation.

## Architecture Technique
Le système est construit avec une architecture modulaire suivant les principes SOLID :
- Backend : Python avec FastAPI
- Frontend : TypeScript avec React
- Base de données : PostgreSQL
- ORM : SQLAlchemy

## Modules

### 1. Finance (finance)
- Gestion de la trésorerie
- Suivi des transactions
- Rapports financiers OHADA
- Analyse des coûts

### 2. Inventaire (inventory)
- Gestion des stocks
- Suivi des mouvements
- Alertes de réapprovisionnement
- Traçabilité des produits

### 3. Production (production)
- Planification des cultures
- Suivi de la production
- Contrôle qualité
- Gestion des équipements

### 4. Ressources Humaines (hr)
- Gestion du personnel
- Paie et avantages
- Congés et absences
- Formation et développement

### 5. Gestion de Projets (project)
- Suivi des projets agricoles
- Planning et calendrier
- Gestion des ressources
- Rapports d'avancement

### 6. Comptabilité (accounting)
- Grand livre
- Balance
- États financiers
- Conformité OHADA

### 7. Contrôle de Gestion (management_control)
- Tableaux de bord
- Analyse des coûts
- Budgets et prévisions
- KPIs

## Installation

```bash
# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
source venv/bin/activate  # Unix
venv\Scripts\activate     # Windows

# Installer les dépendances
pip install -r requirements.txt
```

## Configuration
1. Copier `.env.example` vers `.env`
2. Configurer les variables d'environnement
3. Initialiser la base de données

## Développement
- Suivre les directives de développement dans `docs/development_guidelines.md`
- Exécuter les tests avant chaque commit
- Maintenir une couverture de tests > 80%

## Tests
```bash
pytest
```

## Documentation
La documentation détaillée est disponible dans le dossier `docs/`

## Licence
Propriétaire - FOFAL © 2024
