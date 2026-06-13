import os
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

import json

# Chemin du modèle et des features
CHEMIN_MODELE_EMAIL = os.path.join(os.path.dirname(__file__), "email_model.pkl")
CHEMIN_FEATURES_EMAIL = os.path.join(os.path.dirname(__file__), "email_features.json")
CHEMIN_DATASET = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/emails.csv"))

# Valeurs par défaut (seront écrasées par le chargement du dataset)
FEATURES_EMAIL = []

def charger_dataset() -> pd.DataFrame:
    """Charge le dataset emails.csv."""
    if not os.path.exists(CHEMIN_DATASET):
        raise FileNotFoundError(f"Dataset non trouvé : {CHEMIN_DATASET}")
    
    print(f"Chargement du dataset : {CHEMIN_DATASET}...")
    df = pd.read_csv(CHEMIN_DATASET)
    return df

def entrainer_modele_email():
    """
    Entraîne le modèle Random Forest pour les emails en utilisant emails.csv.
    """
    print("Entraînement du modèle email PhishGuard avec le dataset CSV...")
    df = charger_dataset()
    
    # Extraire les noms de features (toutes les colonnes sauf index et label)
    # Dans emails.csv : Email No., word1, word2, ..., wordN, Prediction
    features = [col for col in df.columns if col not in ["Email No.", "Prediction"]]
    
    X = df[features]
    y = df["Prediction"]

    print(f"Nombre de caractéristiques : {len(features)}")
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(
        n_estimators=100, 
        max_depth=20, 
        n_jobs=-1, 
        random_state=42
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Précision du modèle email : {acc:.4f}")
    
    # Sauvegarder le modèle
    joblib.dump(model, CHEMIN_MODELE_EMAIL)
    print(f"Modèle email sauvegardé sous : {CHEMIN_MODELE_EMAIL}")
    
    # Sauvegarder les features
    with open(CHEMIN_FEATURES_EMAIL, "w") as f:
        json.dump(features, f)
    print(f"Liste des caractéristiques sauvegardée sous : {CHEMIN_FEATURES_EMAIL}")
    
    return model

def charger_features_email():
    """Charge la liste des caractéristiques email."""
    if os.path.exists(CHEMIN_FEATURES_EMAIL):
        with open(CHEMIN_FEATURES_EMAIL, "r") as f:
            return json.load(f)
    return []

# Mettre à jour FEATURES_EMAIL dynamiquement
FEATURES_EMAIL = charger_features_email()

def charger_modele_email():
    """Charge le modèle email."""
    if not os.path.exists(CHEMIN_MODELE_EMAIL):
        return entrainer_modele_email()
    return joblib.load(CHEMIN_MODELE_EMAIL)

if __name__ == "__main__":
    entrainer_modele_email()
