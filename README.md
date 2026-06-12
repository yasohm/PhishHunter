# PhishGuard  — Détecteur de Phishing IA

PhishGuard est une application full-stack moderne qui utilise l'Intelligence Artificielle pour détecter les sites web de phishing en temps réel. L'application analyse 13 caractéristiques clés d'une URL et de son contenu HTML pour évaluer le niveau de risque.

## Fonctionnalités

- **Analyse en temps réel** : Extraction de caractéristiques (HTTPS, âge du domaine, mots-clés suspects, formulaires HTML, etc.).
- **Moteur d'IA** : Classifieur Random Forest entraîné sur des milliers d'exemples.
- **Score de Danger** : Visualisation claire du niveau de confiance et de risque (Sûre, Suspecte, Dangereuse).
- **Historique complet** : Suivi de toutes les analyses passées avec pagination et filtres.
- **Design Moderne** : Interface responsive, sombre et élégante construite avec React et Tailwind CSS.

## Structure du Projet

- `backend/` : API FastAPI (Python) avec SQLAlchemy et Scikit-Learn.
- `frontend/` : Application React (Vite + Tailwind CSS).
- `docker-compose.yml` : Orchestration des conteneurs (API, Web, PostgreSQL).

## Prérequis

- [Docker](https://www.docker.com/) et Docker Compose
- [Node.js](https://nodejs.org/) (optionnel, pour développement local)
- [Python 3.11+](https://www.python.org/) (optionnel, pour développement local)

## Installation et Démarrage

### 1. Cloner le dépôt
```bash
git clone <url-du-depot>
cd phishguard
```

### 2. Lancer avec Docker
```bash
docker-compose up --build
```
Cela démarrera la base de données, le backend et le frontend.

### 3. Entraîner le modèle (Optionnel si non utilisé avec Docker)
Si vous lancez le projet localement sans Docker :
```bash
cd backend
pip install -r requirements.txt
python model/train.py
```

### 4. Accès
- **Frontend** : [http://localhost:5173](http://localhost:5173)
- **Backend API Docs** : [http://localhost:8000/docs](http://localhost:8000/docs)

## Technologies Utilisées

- **Backend** : FastAPI, SQLAlchemy, PostgreSQL, Scikit-Learn, Pandas, BeautifulSoup4.
- **Frontend** : React, Vite, Tailwind CSS, Axios, Lucide React (pour les icônes).
- **DevOps** : Docker, Docker Compose.

---
by ohm
