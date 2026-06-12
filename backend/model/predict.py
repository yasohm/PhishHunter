"""
Module de prédiction — Charge le modèle ML et effectue des prédictions
sur les caractéristiques extraites d'une URL.
"""

import numpy as np
from model.train import load_model, NOMS_CARACTERISTIQUES

# Charger le modèle au démarrage du module
_modele = None


def _obtenir_modele():
    """Charge le modèle de manière paresseuse (lazy loading)."""
    global _modele
    if _modele is None:
        _modele = load_model()
    return _modele


def predict(features: dict) -> dict:
    """
    Effectue une prédiction de phishing à partir des caractéristiques extraites.

    Args:
        features: Dictionnaire contenant les 13 caractéristiques

    Returns:
        Dictionnaire avec:
        - is_phishing: bool — True si le site est détecté comme phishing
        - confidence: float — Score de confiance (0-100)
        - risk_level: str — "safe", "suspicious", ou "dangerous"
    """
    modele = _obtenir_modele()

    # Préparer le vecteur de caractéristiques dans le bon ordre
    vecteur = np.array([[
        features.get(nom, 0) for nom in NOMS_CARACTERISTIQUES
    ]])

    # Obtenir la prédiction et les probabilités
    prediction = modele.predict(vecteur)[0]
    probabilites = modele.predict_proba(vecteur)[0]

    # La confiance est la probabilité de la classe phishing (index 1)
    confiance = round(float(probabilites[1]) * 100, 2)

    # Déterminer le niveau de risque
    if confiance < 40:
        niveau_risque = "safe"
    elif confiance <= 70:
        niveau_risque = "suspicious"
    else:
        niveau_risque = "dangerous"

    return {
        "is_phishing": bool(prediction == 1),
        "confidence": confiance,
        "risk_level": niveau_risque,
    }
