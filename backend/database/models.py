"""
Modèles ORM — Définition des tables de la base de données.
"""

import json
from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Float,
    Text,
    DateTime,
)
from database.db import Base


class Scan(Base):
    """Modèle ORM pour la table des analyses (scans)."""

    __tablename__ = "scans"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    url = Column(String(2048), nullable=False)
    is_phishing = Column(Boolean, nullable=False, default=False)
    confidence = Column(Float, nullable=False, default=0.0)
    risk_level = Column(String(20), nullable=False, default="safe")
    features_json = Column(Text, nullable=False, default="{}")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self) -> dict:
        """Convertit l'objet en dictionnaire pour la sérialisation JSON."""
        return {
            "id": self.id,
            "url": self.url,
            "is_phishing": self.is_phishing,
            "confidence": self.confidence,
            "risk_level": self.risk_level,
            "features": json.loads(self.features_json) if self.features_json else {},
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return (
            f"<Scan(id={self.id}, url='{self.url[:50]}...', "
            f"risk_level='{self.risk_level}', confidence={self.confidence})>"
        )
