"""
Configuration de la base de données — Connexion PostgreSQL asynchrone
avec SQLAlchemy.
"""

import os
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# URL de la base de données depuis l'environnement
# Par défaut, on utilise 'postgres' qui est le nom du service dans docker-compose
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://admin:admin123@localhost:5433/phishguard"
)


# Créer le moteur asynchrone
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_size=10,
    max_overflow=20,
)

# Fabrique de sessions asynchrones
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """Classe de base pour les modèles ORM."""
    pass


async def get_db():
    """Générateur de sessions pour l'injection de dépendances FastAPI."""
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def creer_tables():
    """Crée toutes les tables dans la base de données."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def fermer_connexion():
    """Ferme le moteur de base de données."""
    await engine.dispose()
