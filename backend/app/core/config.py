from pydantic_settings import BaseSettings
from typing import Optional, Dict, Any
from functools import lru_cache

class Settings(BaseSettings):
    # Informations du projet
    PROJECT_NAME: str = "FOFAL ERP"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Configuration de la base de données
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = "fofal_erp"
    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    @property
    def SQLALCHEMY_DATABASE_URL(self) -> str:
        """Construit l'URL de connexion à la base de données."""
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"

    # Configuration de sécurité
    SECRET_KEY: str = "votre_clé_secrète_ici"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 jours
    
    # Configuration CORS
    BACKEND_CORS_ORIGINS: list = ["http://localhost:3000"]  # Frontend URL

    # Configuration agricole
    AGRICULTURAL_CONFIG: Dict[str, Any] = {
        "palm_oil": {
            "total_hectares": 70,
            "plants_per_hectare": 143,
            "harvest_cycle_days": 10
        },
        "papaya": {
            "total_hectares": 10,
            "plants_per_hectare": 1600,
            "harvest_cycle_days": 7
        }
    }

    # Configuration de la comptabilité
    ACCOUNTING_CONFIG: Dict[str, Any] = {
        "currency": "XAF",
        "fiscal_year_start_month": 1,
        "accounting_standard": "OHADA"
    }

    class Config:
        case_sensitive = True
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    """Retourne une instance mise en cache des paramètres."""
    return Settings()

settings = get_settings()
