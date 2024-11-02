"""
Configuration principale de FOFAL ERP
"""
import os
from pathlib import Path
from typing import Dict, Any

from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()

# Chemins de base
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"
MEDIA_DIR = BASE_DIR / "media"
LOGS_DIR = BASE_DIR / "logs"

# Création des répertoires nécessaires
for directory in [STATIC_DIR, MEDIA_DIR, LOGS_DIR]:
    directory.mkdir(exist_ok=True)

# Configuration de la base de données
DATABASE_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "database": os.getenv("DB_NAME", "fofal_erp"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", ""),
}

# Configuration de l'application
APP_CONFIG: Dict[str, Any] = {
    "title": "FOFAL ERP",
    "description": "Système de Gestion Agricole Intégré pour FOFAL",
    "version": "1.0.0",
    "debug": os.getenv("DEBUG", "False").lower() == "true",
}

# Configuration de sécurité
SECURITY_CONFIG = {
    "secret_key": os.getenv("SECRET_KEY", "your-secret-key-here"),
    "algorithm": "HS256",
    "access_token_expire_minutes": 60 * 24,  # 24 heures
}

# Configuration des cultures
AGRICULTURAL_CONFIG = {
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
ACCOUNTING_CONFIG = {
    "currency": "XAF",  # Franc CFA
    "fiscal_year_start_month": 1,  # Janvier
    "accounting_standard": "OHADA"
}

# Configuration des rapports
REPORTING_CONFIG = {
    "default_language": "fr",
    "available_languages": ["fr", "en"],
    "report_formats": ["pdf", "xlsx", "docx"],
    "company_logo_path": str(STATIC_DIR / "logo.png")
}

# Configuration des notifications
NOTIFICATION_CONFIG = {
    "email_enabled": True,
    "sms_enabled": False,
    "notification_types": {
        "stock_alert": True,
        "payment_due": True,
        "harvest_reminder": True,
        "maintenance_alert": True
    }
}

# Configuration du système de fichiers
STORAGE_CONFIG = {
    "max_file_size_mb": 10,
    "allowed_extensions": [".pdf", ".jpg", ".png", ".xlsx", ".docx"],
    "storage_path": str(MEDIA_DIR)
}

# Configuration des logs
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "log_file": str(LOGS_DIR / "fofal_erp.log"),
    "max_size_mb": 10,
    "backup_count": 5
}
