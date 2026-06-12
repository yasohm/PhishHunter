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
from scipy.io import arff
import joblib

# Chemin du modèle sauvegardé
CHEMIN_MODELE = os.path.join(os.path.dirname(__file__), "phishing_model.pkl")
# Chemin du jeu de données ARFF
CHEMIN_DATASET = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../Training Dataset.arff"))

# Noms des caractéristiques du dataset ARFF (UCI Phishing Websites)
NOMS_CARACTERISTIQUES = [
    "having_IP_Address",
    "URL_Length",
    "Shortining_Service",
    "having_At_Symbol",
    "double_slash_redirecting",
    "Prefix_Suffix",
    "having_Sub_Domain",
    "SSLfinal_State",
    "Domain_registeration_length",
    "Favicon",
    "port",
    "HTTPS_token",
    "Request_URL",
    "URL_of_Anchor",
    "Links_in_tags",
    "SFH",
    "Submitting_to_email",
    "Abnormal_URL",
    "Redirect",
    "on_mouseover",
    "RightClick",
    "popUpWidnow",
    "Iframe",
    "age_of_domain",
    "DNSRecord",
    "web_traffic",
    "Page_Rank",
    "Google_Index",
    "Links_pointing_to_page",
    "Statistical_report"
]


def charger_dataset_arff(chemin: str) -> pd.DataFrame:
    """
    Charge le dataset ARFF et le convertit en DataFrame pandas.
    """
    if not os.path.exists(chemin):
        print(f"Dataset non trouvé à {chemin}")
        return None

    print(f"Chargement du dataset réel : {chemin}")
    data, meta = arff.loadarff(chemin)
    df = pd.DataFrame(data)

    # Conversion des types bytes en entiers
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].apply(lambda x: int(x.decode()) if isinstance(x, bytes) else x)

    # Renommer 'Result' en 'is_phishing'
    # Dans le dataset UCI, Result = -1 (phishing), 1 (légitime)
    # On convertit en 0 (légitime) et 1 (phishing)
    df['is_phishing'] = df['Result'].map({-1: 1, 1: 0, 0: 0}) 
    
    return df


def generer_donnees_synthetiques(nb_echantillons: int = 5000) -> pd.DataFrame:
    """
    Génère un jeu de données synthétique compatible avec le nouveau format si besoin.
    Note: On utilise principalement le dataset réel maintenant.
    """
    # ... (On garde une version simplifiée pour le fallback)
    donnees = []
    for _ in range(nb_echantillons):
        is_phishing = np.random.choice([0, 1])
        echantillon = {nom: np.random.choice([-1, 0, 1]) for nom in NOMS_CARACTERISTIQUES}
        echantillon["is_phishing"] = is_phishing
        donnees.append(echantillon)
    
    return pd.DataFrame(donnees)


def entrainer_modele():
    """
    Orchestre le chargement, l'entraînement et la sauvegarde.
    """
    print("=" * 60)
    print("PhishGuard - Entrainement du modele (Dataset Réel)")
    print("=" * 60)

    # Tenter de charger le dataset réel
    df = charger_dataset_arff(CHEMIN_DATASET)
    
    if df is None:
        print("\nGeneration du jeu de données synthetique de secours...")
        df = generer_donnees_synthetiques(5000)
    else:
        print(f"    {len(df)} echantillons charges")

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

    from sklearn.ensemble import GradientBoostingClassifier
    from sklearn.model_selection import cross_val_score

    print("\nCalcul de la performance par validation croisee (5-fold)...")
    modele_cv = GradientBoostingClassifier(
        n_estimators=300, learning_rate=0.1, max_depth=5, random_state=42
    )
    scores = cross_val_score(modele_cv, X, y, cv=5, n_jobs=-1)
    print(f"    - Accuracy moyenne (CV): {scores.mean():.4f} (+/- {scores.std() * 2:.4f})")

    print("\nEntrainement du modele final Gradient Boosting...")
    modele = GradientBoostingClassifier(
        n_estimators=300, learning_rate=0.1, max_depth=5, random_state=42
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
