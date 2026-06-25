"""
PhishHunter — Point d'entrée principal de l'application FastAPI.
Serveur de détection de phishing basé sur le Machine Learning.
"""

import os
import warnings
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from database.db import creer_tables, fermer_connexion
from routes.analyze import router as analyse_router

# Charger les variables d'environnement
load_dotenv()

# Supprimer les avertissements SSL pour les analyses
warnings.filterwarnings("ignore", message="Unverified HTTPS request")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestion du cycle de vie de l'application."""
    # Démarrage : créer les tables si elles n'existent pas
    print("PhishHunter - Demarrage du serveur...")
    try:
        await creer_tables()
        print("Tables de base de données créées/vérifiées")
    except Exception as e:
        print(f"Erreur lors de la création des tables : {e}")
        print("Le serveur continuera sans base de données.")

    yield

    # Arrêt : fermer la connexion à la base de données
    await fermer_connexion()
    print("PhishHunter - Serveur arrete")


# Créer l'application FastAPI
app = FastAPI(
    title="PhishHunter API",
    description="API de détection de sites de phishing basée sur le Machine Learning",
    version="1.0.0",
    lifespan=lifespan,
)

# Configuration CORS — Autoriser le frontend
origines_autorisees = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://localhost:3000",
]

# Allow browser extensions (Chrome + Firefox)
origines_regex = [
    r"chrome-extension://.*",
    r"moz-extension://.*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origines_autorisees,
    allow_origin_regex="|".join(origines_regex),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure les routes API
app.include_router(analyse_router)


@app.get("/")
async def racine():
    """Point d'entrée racine — Informations sur l'API."""
    return {
        "nom": "PhishHunter API",
        "version": "1.0.0",
        "description": "API de détection de sites de phishing",
        "endpoints": {
            "analyser": "POST /api/analyze",
            "historique": "GET /api/history",
            "statistiques": "GET /api/stats",
        },
    }


@app.get("/health")
async def sante():
    """Vérification de l'état de santé du serveur."""
    return {"status": "ok", "service": "PhishHunter API"}
