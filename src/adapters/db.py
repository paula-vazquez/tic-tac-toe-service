# src/adapters/db.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from config.settings import settings

# 1) Motor de conexión
engine = create_engine(
    settings.DB_URL,
    echo=True,                # imprime SQL en consola para debug
    future=True               # SQLAlchemy 2.0 style
)

# 2) Sesión factory
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)

# 3) Base de clases para declarative models
Base = declarative_base()
