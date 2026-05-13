# ============================================================
#  conf/settings.py
#  Configuración centralizada de Flask
#  Lee valores desde .env automáticamente
# ============================================================

import os

class Config:
    """Configuración base (compartida entre todos los entornos)."""
    SECRET_KEY          = os.getenv('SECRET_KEY', 'finca-secret-key-2024')
    SQLALCHEMY_DATABASE_URI      = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """Configuración para desarrollo local."""
    DEBUG = True


class ProductionConfig(Config):
    """Configuración para producción (Coolify/Docker)."""
    DEBUG = False


# ── Mapa de entornos ──────────────────────────────────────
config_map = {
    'development': DevelopmentConfig,
    'production':  ProductionConfig,
}

def get_config():
    env = os.getenv('FLASK_ENV', 'production')
    return config_map.get(env, ProductionConfig)
