FROM python:3.11-slim

# Répertoire de travail
WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copier et installer les dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier les datasets (besoin pour l'entraînement au démarrage)
COPY ["data/Training Dataset.arff", "data/emails.csv", "/app/data/"]

# Copier le code source
COPY . .

# Entraîner les modèles au build
RUN python -c "from model.train import entrainer_modele; from model.train_email import entrainer_modele_email; entrainer_modele(); entrainer_modele_email()"

# Exposer le port
EXPOSE 8000

# Commande de démarrage
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
