"""
Routes API — Points d'entrée pour l'analyse d'URLs, l'historique et les statistiques.
"""

import json
import re
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, field_validator
from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession

from database.db import get_db
from database.models import Scan
from features.extractor import extraire_caracteristiques
from features.email_extractor import extraire_caracteristiques_email
from model.predict import predict
from model.train_email import charger_modele_email, FEATURES_EMAIL

# Créer le routeur API
router = APIRouter(prefix="/api", tags=["Analyse"])


# --- Schémas Pydantic ---

class UrlRequest(BaseModel):
    """Schéma de requête pour l'analyse d'une URL."""
    url: str

    @field_validator("url")
    @classmethod
    def valider_url(cls, v: str) -> str:
        """Valide le format de l'URL."""
        v = v.strip()
        if not v:
            raise ValueError("L'URL ne peut pas être vide")

        # Ajouter le schéma si absent
        if not v.startswith(("http://", "https://")):
            v = "http://" + v

        # Vérification basique du format URL
        patron = re.compile(
            r'^https?://'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
            r'localhost|'
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
            r'(?::\d+)?'
            r'(?:/?|[/?]\S+)$',
            re.IGNORECASE
        )
        if not patron.match(v):
            raise ValueError("Format d'URL invalide")

        return v


class AnalyseResponse(BaseModel):
    """Schéma de réponse pour l'analyse d'une URL."""
    url: str
    is_phishing: bool
    confidence: float
    risk_level: str
    features: dict
    scan_id: int
    created_at: str


class EmailRequest(BaseModel):
    """Schéma de requête pour l'analyse d'un email."""
    sujet: str
    corps: str
    expediteur: str = ""

    @field_validator("sujet", "corps")
    @classmethod
    def valider_non_vide(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Le champ ne peut pas être vide")
        return v


class UrlAnalyseSimple(BaseModel):
    """Analyse simplifiée d'une URL pour l'inclusion dans l'email."""
    url: str
    is_phishing: bool
    confidence: float
    risk_level: str


class EmailAnalyseResponse(BaseModel):
    """Schéma de réponse pour l'analyse d'un email."""
    sujet: str
    expediteur: str
    is_phishing: bool
    confidence: float
    risk_level: str
    features: dict
    urls_extraites: list
    url_analyses: list[UrlAnalyseSimple]
    scan_id: int
    created_at: str


class StatsResponse(BaseModel):
    """Schéma de réponse pour les statistiques."""
    total_scans: int
    phishing_count: int
    safe_count: int
    avg_confidence: float


@router.post("/analyze", response_model=AnalyseResponse)
async def analyser_url(
    requete: UrlRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Analyse une URL pour détecter le phishing.
    Extrait les caractéristiques, effectue la prédiction et sauvegarde le résultat.
    """
    url = requete.url

    try:
        # Étape 1 : Extraire les caractéristiques
        caracteristiques = extraire_caracteristiques(url)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de l'extraction des caractéristiques : {str(e)}"
        )

    try:
        # Étape 2 : Effectuer la prédiction
        resultat = predict(caracteristiques)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la prédiction : {str(e)}"
        )

    try:
        # Étape 3 : Sauvegarder en base de données
        scan = Scan(
            url=url,
            is_phishing=resultat["is_phishing"],
            confidence=resultat["confidence"],
            risk_level=resultat["risk_level"],
            features_json=json.dumps(caracteristiques),
            created_at=datetime.utcnow(),
        )
        db.add(scan)
        await db.flush()
        await db.refresh(scan)

        return AnalyseResponse(
            url=scan.url,
            is_phishing=scan.is_phishing,
            confidence=scan.confidence,
            risk_level=scan.risk_level,
            features=caracteristiques,
            scan_id=scan.id,
            created_at=scan.created_at.isoformat(),
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la sauvegarde : {str(e)}"
        )


@router.post("/analyze-email", response_model=EmailAnalyseResponse)
async def analyser_email(
    requete: EmailRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Analyse un email pour détecter le phishing.
    """
    try:
        # Étape 1 : Extraire les caractéristiques de l'email
        resultat_extraction = extraire_caracteristiques_email(
            requete.sujet, requete.corps, requete.expediteur
        )
        caracteristiques = resultat_extraction["features"]
        model_features = resultat_extraction["model_features"]
        urls_extraites = resultat_extraction["urls_extraites"]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de l'extraction des caractéristiques : {str(e)}"
        )

    try:
        # Étape 2 : Prédiction avec le modèle email (Bag of Words)
        modele_email = charger_modele_email()
        X_email = [model_features.get(f, 0) for f in FEATURES_EMAIL]
        prob_email = modele_email.predict_proba([X_email])[0][1]
        confidence_email = round(float(prob_email * 100), 2)
        is_phishing_email = bool(modele_email.predict([X_email])[0])

        # Étape 3 : Analyse approfondie de chaque URL trouvée
        url_analyses = []
        max_url_confidence = 0.0
        
        for url in urls_extraites:
            try:
                # Utiliser le pipeline d'analyse d'URL existant
                feats_url = extraire_caracteristiques(url)
                res_url = predict(feats_url)
                
                analysis = UrlAnalyseSimple(
                    url=url,
                    is_phishing=res_url["is_phishing"],
                    confidence=res_url["confidence"],
                    risk_level=res_url["risk_level"]
                )
                url_analyses.append(analysis)
                
                if res_url["confidence"] > max_url_confidence:
                    max_url_confidence = res_url["confidence"]
            except Exception:
                # Si une URL échoue (ex: format invalide), on continue
                continue

        # Étape 4 : Verdict combiné
        # Le verdict final est le maximum entre le score de l'email et le score de l'URL la plus dangereuse
        final_confidence = max(confidence_email, max_url_confidence)
        final_is_phishing = is_phishing_email or any(a.is_phishing for a in url_analyses)

        # Déterminer le niveau de risque final
        if final_confidence < 40:
            final_risk_level = "safe"
        elif final_confidence <= 70:
            final_risk_level = "suspicious"
        else:
            final_risk_level = "dangerous"

        resultat = {
            "is_phishing": final_is_phishing,
            "confidence": final_confidence,
            "risk_level": final_risk_level
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la prédiction combinée : {str(e)}"
        )

    try:
        # Étape 5 : Sauvegarder en base de données
        scan = Scan(
            url=f"EMAIL:{requete.sujet[:100]}",
            is_phishing=resultat["is_phishing"],
            confidence=resultat["confidence"],
            risk_level=resultat["risk_level"],
            features_json=json.dumps(caracteristiques),
            created_at=datetime.utcnow(),
        )
        db.add(scan)
        await db.flush()
        await db.refresh(scan)

        return EmailAnalyseResponse(
            sujet=requete.sujet,
            expediteur=requete.expediteur,
            is_phishing=scan.is_phishing,
            confidence=scan.confidence,
            risk_level=scan.risk_level,
            features=caracteristiques,
            urls_extraites=urls_extraites,
            url_analyses=url_analyses,
            scan_id=scan.id,
            created_at=scan.created_at.isoformat(),
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la sauvegarde : {str(e)}"
        )


@router.get("/history")
async def obtenir_historique(
    page: int = Query(default=1, ge=1, description="Numéro de page"),
    limit: int = Query(default=20, ge=1, le=100, description="Nombre de résultats par page"),
    risk_level: Optional[str] = Query(
        default=None,
        description="Filtrer par niveau de risque (safe, suspicious, dangerous)"
    ),
    db: AsyncSession = Depends(get_db),
):
    """
    Récupère l'historique paginé des analyses effectuées.
    """
    try:
        # Construire la requête de base
        requete = select(Scan).order_by(desc(Scan.created_at))

        # Appliquer le filtre de niveau de risque si spécifié
        if risk_level and risk_level in ("safe", "suspicious", "dangerous"):
            requete = requete.where(Scan.risk_level == risk_level)

        # Compter le total
        requete_count = select(func.count(Scan.id))
        if risk_level and risk_level in ("safe", "suspicious", "dangerous"):
            requete_count = requete_count.where(Scan.risk_level == risk_level)

        resultat_count = await db.execute(requete_count)
        total = resultat_count.scalar() or 0

        # Appliquer la pagination
        offset = (page - 1) * limit
        requete = requete.offset(offset).limit(limit)

        resultat = await db.execute(requete)
        scans = resultat.scalars().all()

        return {
            "items": [scan.to_dict() for scan in scans],
            "total": total,
            "page": page,
            "limit": limit,
            "pages": (total + limit - 1) // limit if total > 0 else 0,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la récupération de l'historique : {str(e)}"
        )


@router.get("/stats", response_model=StatsResponse)
async def obtenir_statistiques(
    db: AsyncSession = Depends(get_db),
):
    """
    Récupère les statistiques globales des analyses.
    """
    try:
        # Total des scans
        resultat_total = await db.execute(select(func.count(Scan.id)))
        total_scans = resultat_total.scalar() or 0

        # Nombre de phishing détectés
        resultat_phishing = await db.execute(
            select(func.count(Scan.id)).where(Scan.is_phishing == True)
        )
        phishing_count = resultat_phishing.scalar() or 0

        # Nombre de sites sûrs
        safe_count = total_scans - phishing_count

        # Confiance moyenne
        resultat_avg = await db.execute(select(func.avg(Scan.confidence)))
        avg_confidence = round(float(resultat_avg.scalar() or 0), 2)

        return StatsResponse(
            total_scans=total_scans,
            phishing_count=phishing_count,
            safe_count=safe_count,
            avg_confidence=avg_confidence,
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la récupération des statistiques : {str(e)}"
        )
