"""
Script d'entraînement du modèle ML — Génère un jeu de données synthétique
et entraîne un classifieur Random Forest pour la détection de phishing.
"""

import os
import sys
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
)
import joblib

# Chemin du modèle sauvegardé
CHEMIN_MODELE = os.path.join(os.path.dirname(__file__), "phishing_model.pkl")

# Noms des caractéristiques enrichies
NOMS_CARACTERISTIQUES = [
    "url_length",
    "has_https",
    "has_ip_address",
    "subdomain_count",
    "special_char_count",
    "domain_age_days",
    "whois_success",
    "has_suspicious_keywords",
    "redirect_count",
    "has_favicon_mismatch",
    "html_form_count",
    "external_links_ratio",
    "has_password_input",
    "page_title_suspicious",
    "url_entropy",
    "is_shortened",
    "digit_count",
]


def generer_donnees_synthetiques(nb_echantillons: int = 5000) -> pd.DataFrame:
    """
    Génère un jeu de données synthétique plus intelligent et nuancé.
    """
    np.random.seed(42)
    nb_phishing = nb_echantillons // 2
    nb_legitime = nb_echantillons - nb_phishing

    donnees = []

    # --- Générer des échantillons LÉGITIMES ---
    for _ in range(nb_legitime):
        url_len = np.random.randint(15, 60)
        # 10% de chance d'échec WHOIS même sur du légitime
        whois_suc = np.random.choice([0, 1], p=[0.1, 0.9])
        dom_age = np.random.randint(365, 7300) if whois_suc else -1
        
        echantillon = {
            "url_length": url_len,
            "has_https": np.random.choice([0, 1], p=[0.05, 0.95]),
            "has_ip_address": 0,
            "subdomain_count": np.random.choice([0, 1, 2], p=[0.6, 0.3, 0.1]),
            "special_char_count": np.random.choice([0, 1, 2], p=[0.8, 0.15, 0.05]),
            "domain_age_days": dom_age,
            "whois_success": whois_suc,
            "has_suspicious_keywords": np.random.choice([0, 1], p=[0.95, 0.05]),
            "redirect_count": np.random.choice([0, 1], p=[0.9, 0.1]),
            "has_favicon_mismatch": 0,
            "html_form_count": np.random.choice([0, 1, 2], p=[0.5, 0.4, 0.1]),
            "external_links_ratio": round(np.random.uniform(0.0, 0.2), 4),
            "has_password_input": np.random.choice([0, 1], p=[0.8, 0.2]),
            "page_title_suspicious": 0,
            "url_entropy": round(np.random.uniform(3.0, 4.2), 4),
            "is_shortened": 0,
            "digit_count": np.random.randint(0, 5),
            "is_phishing": 0,
        }
        donnees.append(echantillon)

    # --- Générer des échantillons de PHISHING ---
    for _ in range(nb_phishing):
        url_len = np.random.randint(40, 180)
        whois_suc = np.random.choice([0, 1], p=[0.3, 0.7])
        # Un site de phishing a soit un âge court, soit WHOIS échoue
        dom_age = np.random.randint(0, 90) if whois_suc else -1

        echantillon = {
            "url_length": url_len,
            "has_https": np.random.choice([0, 1], p=[0.4, 0.6]),
            "has_ip_address": np.random.choice([0, 1], p=[0.7, 0.3]),
            "subdomain_count": np.random.randint(1, 4),
            "special_char_count": np.random.randint(1, 5),
            "domain_age_days": dom_age,
            "whois_success": whois_suc,
            "has_suspicious_keywords": np.random.choice([0, 1], p=[0.1, 0.9]),
            "redirect_count": np.random.randint(1, 4),
            "has_favicon_mismatch": np.random.choice([0, 1], p=[0.4, 0.6]),
            "html_form_count": np.random.randint(1, 4),
            "external_links_ratio": round(np.random.uniform(0.4, 0.9), 4),
            "has_password_input": np.random.choice([0, 1], p=[0.2, 0.8]),
            "page_title_suspicious": np.random.choice([0, 1], p=[0.3, 0.7]),
            "url_entropy": round(np.random.uniform(4.0, 5.5), 4),
            "is_shortened": np.random.choice([0, 1], p=[0.7, 0.3]),
            "digit_count": np.random.randint(5, 20),
            "is_phishing": 1,
        }
        donnees.append(echantillon)

    df = pd.DataFrame(donnees)
    # Mélanger les données
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    return df


def entrainer_modele():
    """
    Orchestre la génération de données, l'entraînement et la sauvegarde.
    """
    print("=" * 60)
    print("PhishGuard - Entrainement du modele de detection")
    print("=" * 60)

    print("\nGeneration du jeu de données synthetique (5000 echantillons)...")
    df = generer_donnees_synthetiques(5000)
    print(f"    5000 echantillons generes")
    print(f"    - Sites legitimes : {len(df[df['is_phishing'] == 0])}")
    print(f"    - Sites de phishing : {len(df[df['is_phishing'] == 1])}")

    X = df[NOMS_CARACTERISTIQUES]
    y = df["is_phishing"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print("\nDivision des donnees :")
    print(f"    - Entrainement : {len(X_train)} echantillons")
    print(f"    - Test : {len(X_test)} echantillons")

    print("\nEntrainement du modele Random Forest...")
    modele = RandomForestClassifier(
        n_estimators=200, max_depth=15, n_jobs=-1, random_state=42
    )
    modele.fit(X_train, y_train)
    print("    Entrainement termine")

    y_pred = modele.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print("\nMetriques de performance :")
    print(f"    - Exactitude (Accuracy)  : {accuracy:.4f}")
    print(f"    - Precision (Precision)  : {precision_score(y_test, y_pred):.4f}")
    print(f"    - Rappel (Recall)        : {recall_score(y_test, y_pred):.4f}")
    print(f"    - Score F1               : {f1_score(y_test, y_pred):.4f}")

    print("\nRapport de classification detaille :")
    print(classification_report(y_test, y_pred, target_names=["Legitime", "Phishing"]))

    print("\nImportance des caracteristiques :")
    importances = pd.Series(modele.feature_importances_, index=NOMS_CARACTERISTIQUES)
    for i, (nom, val) in enumerate(importances.sort_values(ascending=False).items()):
        print(f"    {i+1}. {nom}: {val:.4f}")

    # Sauvegarder le modèle
    joblib.dump(modele, CHEMIN_MODELE)
    print(f"\nModele sauvegarde : {CHEMIN_MODELE}")
    print("=" * 60)

    return modele


def charger_modele():
    """Charge le modèle sauvegardé depuis le fichier pkl."""
    if not os.path.exists(CHEMIN_MODELE):
        print("Modèle non trouvé. Entraînement en cours...")
        return entrainer_modele()
    return joblib.load(CHEMIN_MODELE)


# Alias anglais pour la compatibilité
load_model = charger_modele


if __name__ == "__main__":
    entrainer_modele()
