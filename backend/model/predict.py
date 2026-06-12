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
    import pandas as pd
    modele = _obtenir_modele()

    # Préparer le vecteur de caractéristiques dans le bon ordre sous forme de DataFrame
    df_predict = pd.DataFrame([features], columns=NOMS_CARACTERISTIQUES)
    df_predict = df_predict.fillna(0) # Sécurité (normalement pas besoin car Features extractor est complet)

    # Obtenir la prédiction et les probabilités
    prediction = modele.predict(df_predict)[0]
    probabilites = modele.predict_proba(df_predict)[0]

    # La confiance est la probabilité de la classe phishing (index 1)
    confiance = round(float(probabilites[1]) * 100, 2)

    # --- Boost heuristique ---
    # Si les signaux structurels crient "phishing" mais que le modèle ML est trop confiant
    # en "safe", on applique un plancher de confiance pour éviter les faux négatifs.
    signaux_phishing = 0
    if features.get("Abnormal_URL") == -1:
        signaux_phishing += 3  # Signal fort
    elif features.get("Abnormal_URL") == 0:
        signaux_phishing += 1
    if features.get("URL_Length") == -1:
        signaux_phishing += 1
    if features.get("having_Sub_Domain") == -1:
        signaux_phishing += 1
    elif features.get("having_Sub_Domain") == 0:
        signaux_phishing += 0.5
    if features.get("SSLfinal_State") == -1:
        signaux_phishing += 1
    if features.get("Prefix_Suffix") == -1:
        signaux_phishing += 1

    # Appliquer le boost si les heuristiques sont fortement suspectes
    if signaux_phishing >= 4 and confiance < 75:
        confiance = max(confiance, 75.0)
        prediction = 1
    elif signaux_phishing >= 3 and confiance < 55:
        confiance = max(confiance, 55.0)
        prediction = 1

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
