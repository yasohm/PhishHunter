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

# Noms des 13 caractéristiques
NOMS_CARACTERISTIQUES = [
    "url_length",
    "has_https",
    "has_ip_address",
    "subdomain_count",
    "special_char_count",
    "domain_age_days",
    "has_suspicious_keywords",
    "redirect_count",
    "has_favicon_mismatch",
    "html_form_count",
    "external_links_ratio",
    "has_password_input",
    "page_title_mismatch",
]


def generer_donnees_synthetiques(nb_echantillons: int = 5000) -> pd.DataFrame:
    """
    Génère un jeu de données synthétique réaliste pour l'entraînement.
    Les sites de phishing ont des caractéristiques distinctes des sites légitimes.
    """
    np.random.seed(42)
    nb_phishing = nb_echantillons // 2
    nb_legitime = nb_echantillons - nb_phishing

    donnees = []

    # --- Générer des échantillons LÉGITIMES ---
    for _ in range(nb_legitime):
        echantillon = {
            "url_length": np.random.randint(15, 60),
            "has_https": np.random.choice([0, 1], p=[0.1, 0.9]),
            "has_ip_address": np.random.choice([0, 1], p=[0.98, 0.02]),
            "subdomain_count": np.random.choice([0, 1, 2], p=[0.5, 0.4, 0.1]),
            "special_char_count": np.random.choice([0, 1], p=[0.85, 0.15]),
            "domain_age_days": np.random.randint(365, 7300),
            "has_suspicious_keywords": np.random.choice([0, 1], p=[0.9, 0.1]),
            "redirect_count": np.random.choice([0, 1, 2], p=[0.7, 0.2, 0.1]),
            "has_favicon_mismatch": np.random.choice([0, 1], p=[0.95, 0.05]),
            "html_form_count": np.random.choice([0, 1, 2], p=[0.4, 0.5, 0.1]),
            "external_links_ratio": round(np.random.uniform(0.0, 0.3), 4),
            "has_password_input": np.random.choice([0, 1], p=[0.7, 0.3]),
            "page_title_mismatch": np.random.choice([0, 1], p=[0.95, 0.05]),
            "is_phishing": 0,
        }
        donnees.append(echantillon)

    # --- Générer des échantillons de PHISHING ---
    for _ in range(nb_phishing):
        echantillon = {
            "url_length": np.random.randint(40, 200),
            "has_https": np.random.choice([0, 1], p=[0.6, 0.4]),
            "has_ip_address": np.random.choice([0, 1], p=[0.6, 0.4]),
            "subdomain_count": np.random.choice([0, 1, 2, 3, 4], p=[0.1, 0.2, 0.3, 0.25, 0.15]),
            "special_char_count": np.random.randint(1, 6),
            "domain_age_days": np.random.randint(0, 180),
            "has_suspicious_keywords": np.random.choice([0, 1], p=[0.2, 0.8]),
            "redirect_count": np.random.choice([0, 1, 2, 3, 4], p=[0.1, 0.2, 0.3, 0.2, 0.2]),
            "has_favicon_mismatch": np.random.choice([0, 1], p=[0.4, 0.6]),
            "html_form_count": np.random.choice([0, 1, 2, 3], p=[0.1, 0.3, 0.4, 0.2]),
            "external_links_ratio": round(np.random.uniform(0.3, 1.0), 4),
            "has_password_input": np.random.choice([0, 1], p=[0.2, 0.8]),
            "page_title_mismatch": np.random.choice([0, 1], p=[0.3, 0.7]),
            "is_phishing": 1,
        }
        donnees.append(echantillon)

    df = pd.DataFrame(donnees)
    # Mélanger les données
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    return df


def entrainer_modele():
    """
    Entraîne le modèle Random Forest et sauvegarde le résultat.
    """
    print("=" * 60)
    print("🛡️  PhishGuard — Entraînement du modèle de détection")
    print("=" * 60)

    # Générer les données synthétiques
    print("\n📊 Génération du jeu de données synthétique (5000 échantillons)...")
    df = generer_donnees_synthetiques(5000)
    print(f"   ✅ {len(df)} échantillons générés")
    print(f"   - Sites légitimes : {len(df[df['is_phishing'] == 0])}")
    print(f"   - Sites de phishing : {len(df[df['is_phishing'] == 1])}")

    # Séparer les caractéristiques et les étiquettes
    X = df[NOMS_CARACTERISTIQUES]
    y = df["is_phishing"]

    # Division en jeux d'entraînement et de test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"\n📦 Division des données :")
    print(f"   - Entraînement : {len(X_train)} échantillons")
    print(f"   - Test : {len(X_test)} échantillons")

    # Entraîner le classifieur Random Forest
    print("\n🔧 Entraînement du modèle Random Forest...")
    modele = RandomForestClassifier(
        n_estimators=200,
        max_depth=15,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1,
    )
    modele.fit(X_train, y_train)
    print("   ✅ Entraînement terminé")

    # Évaluation du modèle
    y_pred = modele.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    print("\n📈 Métriques de performance :")
    print(f"   - Exactitude (Accuracy)  : {accuracy:.4f}")
    print(f"   - Précision (Precision)  : {precision:.4f}")
    print(f"   - Rappel (Recall)        : {recall:.4f}")
    print(f"   - Score F1               : {f1:.4f}")

    print(f"\n📋 Rapport de classification détaillé :")
    print(classification_report(
        y_test, y_pred,
        target_names=["Légitime", "Phishing"]
    ))

    # Importance des caractéristiques
    importances = modele.feature_importances_
    indices = np.argsort(importances)[::-1]
    print("🔍 Importance des caractéristiques :")
    for i, idx in enumerate(indices):
        print(f"   {i + 1}. {NOMS_CARACTERISTIQUES[idx]}: {importances[idx]:.4f}")

    # Sauvegarder le modèle
    joblib.dump(modele, CHEMIN_MODELE)
    print(f"\n💾 Modèle sauvegardé : {CHEMIN_MODELE}")
    print("=" * 60)

    return modele


def charger_modele():
    """Charge le modèle sauvegardé depuis le fichier pkl."""
    if not os.path.exists(CHEMIN_MODELE):
        print("⚠️  Modèle non trouvé. Entraînement en cours...")
        return entrainer_modele()
    return joblib.load(CHEMIN_MODELE)


# Alias anglais pour la compatibilité
load_model = charger_modele


if __name__ == "__main__":
    entrainer_modele()
