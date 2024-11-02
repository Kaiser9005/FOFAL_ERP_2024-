from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# Création du moteur SQLAlchemy
engine = create_engine(settings.SQLALCHEMY_DATABASE_URL)

# Session locale pour les opérations de base de données
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe de base pour les modèles SQLAlchemy
Base = declarative_base()

# Dépendance pour obtenir la session de base de données
def get_db():
    """
    Générateur de contexte pour la session de base de données.
    Assure que la session est fermée après utilisation.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
