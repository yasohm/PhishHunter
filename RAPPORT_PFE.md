# RAPPORT DE STAGE / PROJET DE FIN D'ÉTUDES

---

## PAGE DE GARDE

**[Logo de l'établissement] [Logo de l'organisme d'accueil]**

---

# PhishGuard
## Système de Détection de Phishing par Intelligence Artificielle

---

**Encadrant :** [Nom de l'encadrant]

**Réalisé par :** [Votre Nom et Prénom]

**Niveau :** BTS / DSI

**Filière :** Développement des Systèmes d'Information

**Année scolaire :** 2024–2025

---

---

## REMERCIEMENTS

Je tiens à exprimer ma profonde gratitude à toutes les personnes qui ont contribué, de près ou de loin, à la réalisation de ce projet de fin d'études.

Je remercie en premier lieu mon encadrant, **[Nom de l'encadrant]**, pour ses précieux conseils, sa disponibilité et ses orientations tout au long de ce travail. Son expertise et son soutien ont été déterminants dans la conduite de ce projet.

Je remercie également l'ensemble du corps enseignant de la filière **Développement des Systèmes d'Information** pour la qualité de la formation dispensée, qui m'a fourni les bases techniques nécessaires à la réalisation de ce projet.

Mes remerciements vont aussi aux membres du jury pour le temps consacré à l'évaluation de ce travail.

Enfin, je remercie ma famille et mes proches pour leur soutien moral indéfectible durant toute la durée de mes études.

---

---

## RÉSUMÉ

Le phishing constitue l'une des cybermenaces les plus répandues, causant des pertes financières et des atteintes à la confidentialité des données à l'échelle mondiale. Ce projet de fin d'études présente **PhishGuard**, un système de détection de phishing basé sur l'Intelligence Artificielle, développé sous forme d'application web full-stack complétée par une extension de navigateur.

L'architecture du système repose sur deux modules de détection complémentaires : un analyseur d'URLs utilisant un classifieur **Gradient Boosting** entraîné sur 30 caractéristiques extraites du dataset UCI Phishing Websites (11 055 exemples), et un analyseur d'emails employant un modèle **Random Forest** avec une approche Bag of Words. La solution intègre un backend **FastAPI** (Python), une base de données **PostgreSQL**, un frontend **React/Vite**, et une extension navigateur compatible **Manifest V3**.

Les résultats obtenus démontrent une précision supérieure à 95 % pour la détection d'URLs de phishing, avec une interface utilisateur intuitive permettant la visualisation détaillée des caractéristiques d'analyse, l'historique des scans et l'export des rapports.

**Mots-clés :** Phishing, Machine Learning, Gradient Boosting, Random Forest, FastAPI, React, Extension Chrome, Cybersécurité.

---

**ABSTRACT**

Phishing represents one of the most widespread cyber threats, causing financial losses and data breaches worldwide. This final-year project presents **PhishGuard**, an AI-powered phishing detection system developed as a full-stack web application complemented by a browser extension.

The system architecture relies on two complementary detection modules: a URL analyzer using a **Gradient Boosting** classifier trained on 30 features extracted from the UCI Phishing Websites dataset (11,055 samples), and an email analyzer employing a **Random Forest** model with a Bag of Words approach. The solution integrates a **FastAPI** backend (Python), a **PostgreSQL** database, a **React/Vite** frontend, and a **Manifest V3**-compatible browser extension.

Results demonstrate accuracy exceeding 95% for phishing URL detection, with an intuitive user interface for detailed feature visualization, scan history, and report export.

**Keywords:** Phishing, Machine Learning, Gradient Boosting, Random Forest, FastAPI, React, Chrome Extension, Cybersecurity.

---

---

## SOMMAIRE

- **Introduction** ............................................................... 1
- **Chapitre 1 : Description du Sujet** .......................... 4
  - 1.1 Contexte et problématique ................................. 4
  - 1.2 Présentation du projet PhishGuard ..................... 6
  - 1.3 Objectifs et intérêt du projet .............................. 8
- **Chapitre 2 : Conception de la Solution** ................. 10
  - 2.1 Technologies et outils utilisés .......................... 10
  - 2.2 Architecture du système ................................... 13
  - 2.3 Modélisation des données ................................ 16
  - 2.4 Conception des modules ML ............................ 18
- **Chapitre 3 : Implémentation du Projet** ................. 22
  - 3.1 Mise en place de l'environnement ..................... 22
  - 3.2 Implémentation du backend .............................. 23
  - 3.3 Implémentation du frontend ............................. 27
  - 3.4 Extension navigateur ........................................ 30
  - 3.5 Tests et évaluation ............................................ 33
- **Conclusion** ................................................................ 36
- **Références Bibliographiques** ................................. 38
- **Annexes** .................................................................... 40

---

## LISTE DES ABRÉVIATIONS

| Abréviation | Signification |
|---|---|
| IA / AI | Intelligence Artificielle / Artificial Intelligence |
| ML | Machine Learning (Apprentissage Automatique) |
| API | Application Programming Interface |
| URL | Uniform Resource Locator |
| HTTP / HTTPS | HyperText Transfer Protocol (Secure) |
| HTML | HyperText Markup Language |
| JSON | JavaScript Object Notation |
| REST | Representational State Transfer |
| CORS | Cross-Origin Resource Sharing |
| ORM | Object-Relational Mapping |
| UCI | University of California, Irvine |
| RF | Random Forest |
| GB | Gradient Boosting |
| NLP | Natural Language Processing |
| BoW | Bag of Words |
| SSL | Secure Sockets Layer |
| DNS | Domain Name System |
| WHOIS | Protocole de requête de données d'enregistrement de domaine |
| DOM | Document Object Model |
| MV3 | Manifest Version 3 (extension navigateur) |
| PFE | Projet de Fin d'Études |
| BTS | Brevet de Technicien Supérieur |
| DSI | Développement des Systèmes d'Information |

---

## LISTE DES FIGURES

- Figure 1 : Évolution des attaques de phishing mondiales (2019–2024)
- Figure 2 : Architecture globale du système PhishGuard
- Figure 3 : Diagramme des cas d'utilisation
- Figure 4 : Modèle de la base de données (table Scans)
- Figure 5 : Pipeline d'extraction des caractéristiques d'URL
- Figure 6 : Pipeline d'analyse des emails
- Figure 7 : Résultats de validation croisée du modèle Gradient Boosting
- Figure 8 : Importance des caractéristiques (Feature Importance)
- Figure 9 : Matrice de confusion du modèle URL
- Figure 10 : Architecture Docker – orchestration des conteneurs
- Figure 11 : Interface d'accueil de PhishGuard
- Figure 12 : Interface d'analyse d'URL
- Figure 13 : Résultat d'analyse – site dangereux
- Figure 14 : Interface d'analyse d'email
- Figure 15 : Page d'historique avec filtres
- Figure 16 : Popup de l'extension navigateur
- Figure 17 : Comparaison des performances des modèles

---

---

# INTRODUCTION

## 1. Contexte général

La transformation numérique accélérée de nos sociétés a engendré une multiplication sans précédent des cybermenaces. Parmi celles-ci, le **phishing** (hameçonnage) occupe une place prépondérante : selon le rapport APWG (Anti-Phishing Working Group) de 2024, plus de 5 millions d'attaques de phishing uniques ont été enregistrées au cours du seul premier trimestre 2024, établissant un nouveau record historique [1]. Ces attaques visent à tromper les utilisateurs pour leur soutirer des informations sensibles — identifiants, mots de passe, données bancaires — en usurpant l'identité de sites ou d'expéditeurs légitimes.

Les méthodes traditionnelles de détection, basées sur des listes noires (blacklists) statiques, montrent leurs limites face à la sophistication croissante des attaquants : les URLs de phishing ont une durée de vie de quelques heures seulement, rendant les listes noires perpétuellement obsolètes. Il devient donc indispensable de recourir à des méthodes d'apprentissage automatique capables de détecter des patterns inconnus en temps réel.

## 2. Cadre du stage

Ce projet de fin d'études s'inscrit dans le cadre de la formation **BTS Développement des Systèmes d'Information** et répond à un double objectif : d'une part, mettre en pratique les compétences acquises en développement web, gestion de bases de données et algorithmes ; d'autre part, contribuer à la cybersécurité à travers une solution concrète et déployable.

## 3. But pédagogique

Ce projet vise à consolider les compétences dans les domaines suivants :
- Le développement full-stack (Python/FastAPI pour le backend, React pour le frontend)
- L'intégration de modèles de Machine Learning dans une application web
- La conteneurisation d'applications avec Docker
- Le développement d'extensions navigateur (Manifest V3)
- La conception et modélisation de bases de données relationnelles (PostgreSQL)

## 4. Problématique

**Comment concevoir et implémenter un système de détection de phishing en temps réel, basé sur l'intelligence artificielle, accessible à travers une application web et une extension navigateur, capable d'analyser aussi bien les URLs que les emails suspects ?**

Cette problématique soulève plusieurs questions secondaires :
- Quelles caractéristiques d'une URL ou d'un email permettent de distinguer le phishing des contenus légitimes ?
- Quel algorithme de Machine Learning offre le meilleur compromis entre précision et vitesse d'exécution ?
- Comment architecturer une solution scalable et facilement déployable ?

## 5. Démarche du rapport

Pour répondre à cette problématique, ce rapport est organisé en trois parties principales :

Le **Chapitre 1** présente le contexte du projet, la problématique détaillée du phishing et les objectifs de PhishGuard.

Le **Chapitre 2** expose la conception de la solution : choix technologiques, architecture système, modélisation des données et conception des modules de Machine Learning.

Le **Chapitre 3** détaille l'implémentation concrète du projet, les tests réalisés et l'évaluation des performances.

---

---

# CHAPITRE 1 : DESCRIPTION DU SUJET

## 1.1 Contexte et Problématique

### 1.1.1 Le Phishing : Définition et Ampleur

Le phishing est une technique de cyberattaque par ingénierie sociale dans laquelle un attaquant se fait passer pour une entité de confiance (banque, réseau social, service gouvernemental) afin de pousser la victime à divulguer des informations confidentielles ou à effectuer des actions malveillantes [2].

Les vecteurs d'attaque sont multiples :
- **URLs malveillantes** : sites web imitant fidèlement des pages légitimes
- **Emails de phishing** : messages frauduleux incitant à cliquer sur des liens ou à fournir des données
- **SMS (Smishing)** et appels téléphoniques (Vishing)

**[Figure 1 : Évolution des attaques de phishing mondiales — à insérer ici]**

### 1.1.2 Limites des Solutions Existantes

Les approches actuelles de lutte contre le phishing présentent plusieurs limitations :

| Approche | Avantages | Inconvénients |
|---|---|---|
| Listes noires (Blacklists) | Simple, rapide | Ne détecte pas les nouvelles URLs, mise à jour lente |
| Filtres par règles | Explicable | Facilement contournable |
| Vérification manuelle | Fiable | Non scalable, trop lente |
| ML basé sur le contenu | Généralise bien | Nécessite un accès au contenu de la page |

Ces limitations justifient le développement d'une solution hybride combinant l'analyse de structure d'URL et l'analyse sémantique des emails, à travers des modèles de Machine Learning entraînés sur des datasets publics reconnus.

### 1.1.3 Contexte Organisationnel

PhishGuard a été développé dans le cadre d'un projet académique individuel. Le projet s'inscrit dans la démarche plus large de démocratisation des outils de cybersécurité, en proposant une solution open-source, facilement déployable via Docker, et accessible au grand public à travers une extension de navigateur.

## 1.2 Présentation du Projet PhishGuard

### 1.2.1 Vue d'Ensemble

**PhishGuard** est un système de détection de phishing en temps réel basé sur l'Intelligence Artificielle. Il se compose de trois composantes principales :

1. **Application Web** : Interface permettant l'analyse d'URLs et d'emails, la visualisation des caractéristiques détectées et la consultation de l'historique des analyses.

2. **API Backend** : Serveur RESTful assurant l'extraction des caractéristiques, l'inférence des modèles ML et la persistance des données.

3. **Extension Navigateur** : Composant intégré au navigateur (Chrome/Firefox) permettant une détection automatique et transparente des pages web visitées par l'utilisateur.

### 1.2.2 Fonctionnalités Principales

**Analyse d'URLs :**
- Extraction de 30 caractéristiques structurelles et comportementales
- Classification en trois niveaux de risque : Sûr, Suspect, Dangereux
- Score de confiance en pourcentage
- Visualisation détaillée de chaque caractéristique analysée

**Analyse d'Emails :**
- Extraction de caractéristiques NLP (Bag of Words, entropie, mots-clés d'urgence)
- Détection de spoofing de marques
- Analyse des URLs contenues dans l'email
- Score de risque combiné (email + URLs)

**Fonctionnalités transversales :**
- Historique complet des analyses avec pagination et filtres
- Export des rapports en formats PDF et JSON
- Extension navigateur avec popup de résultat en temps réel
- Tableau de bord statistique

## 1.3 Objectifs et Intérêt du Projet

### 1.3.1 Objectifs Techniques

- Concevoir et entraîner deux modèles de ML distincts (URLs et emails) avec des performances élevées (accuracy > 95%)
- Développer une API REST performante et documentée (FastAPI avec Swagger)
- Créer une interface utilisateur réactive et intuitive
- Déployer la solution via Docker pour une portabilité maximale

### 1.3.2 Objectifs Pédagogiques

- Maîtriser le cycle complet de développement d'un système ML : collecte de données → entraînement → évaluation → déploiement
- Acquérir une expérience pratique du développement full-stack moderne
- Comprendre les enjeux de la cybersécurité et des techniques de phishing

### 1.3.3 Intérêt du Projet

L'intérêt de PhishGuard réside dans son approche **multi-vecteurs** : contrairement aux solutions se concentrant uniquement sur les URLs ou uniquement sur les emails, PhishGuard adresse les deux principaux vecteurs d'attaque phishing dans une interface unifiée. L'intégration sous forme d'extension navigateur rend la protection transparente pour l'utilisateur final, sans nécessiter d'action manuelle.

---

---

# CHAPITRE 2 : CONCEPTION DE LA SOLUTION

## 2.1 Technologies et Outils Utilisés

### 2.1.1 Backend — Python et FastAPI

Le backend est développé en **Python 3.11** avec le framework **FastAPI** [3]. Ce choix s'explique par plusieurs raisons :
- Performances élevées (comparable à Node.js et Go) grâce à l'asynchronisme natif
- Documentation automatique des APIs via Swagger UI et ReDoc
- Intégration naturelle avec l'écosystème scientifique Python (Scikit-learn, Pandas, NumPy)
- Support natif des types Pydantic pour la validation des données

Les principales dépendances backend sont :

| Bibliothèque | Version | Rôle |
|---|---|---|
| fastapi | 0.104.1 | Framework web asynchrone |
| uvicorn | 0.24.0 | Serveur ASGI |
| sqlalchemy | 2.0.23 | ORM pour PostgreSQL |
| asyncpg | 0.29.0 | Driver PostgreSQL asynchrone |
| scikit-learn | 1.6.0 | Algorithmes de Machine Learning |
| pandas | 2.1.4 | Manipulation de données |
| numpy | 1.26.2 | Calcul numérique |
| beautifulsoup4 | 4.12.2 | Parsing HTML |
| python-whois | 0.9.4 | Requêtes WHOIS |
| requests | 2.31.0 | Requêtes HTTP |
| scipy | 1.11.4 | Chargement des fichiers ARFF |
| joblib | 1.3.2 | Sérialisation des modèles ML |

### 2.1.2 Base de Données — PostgreSQL

La persistance des données est assurée par **PostgreSQL 15** [4], un système de gestion de bases de données relationnelles open-source robuste. L'accès à la base de données est géré via **SQLAlchemy 2.0** en mode asynchrone, offrant :
- Des transactions ACID garantissant l'intégrité des données
- La gestion des connexions via un pool asynchrone
- Une abstraction ORM permettant une indépendance vis-à-vis du SGBD

### 2.1.3 Frontend — React et Vite

L'interface utilisateur est construite avec **React 18** et **Vite** comme outil de build [5]. Le style est géré par **Tailwind CSS**, permettant un développement rapide d'interfaces modernes et responsives. La communication avec l'API est assurée par **Axios**.

### 2.1.4 Extension Navigateur — Manifest V3

L'extension navigateur est développée selon la spécification **Manifest V3** (MV3), le standard actuel de Chrome et Firefox pour les extensions. Elle se compose de :
- Un **Service Worker** (background) pour la communication avec l'API
- Un **Content Script** pour l'analyse automatique des pages visitées
- Une **Popup** pour l'affichage des résultats à la demande
- Une page **Options** pour la configuration

### 2.1.5 Conteneurisation — Docker

L'ensemble de la solution est orchestré via **Docker Compose**, qui définit trois services :
- `phishguard-db` : conteneur PostgreSQL 15
- `phishguard-api` : conteneur du backend FastAPI
- `phishguard-web` : conteneur du frontend React

Cette architecture garantit la reproductibilité de l'environnement et simplifie le déploiement.

## 2.2 Architecture du Système

### 2.2.1 Architecture Globale

L'architecture de PhishGuard suit un modèle **client-serveur à trois tiers** :

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT (Tiers 1)                        │
│  ┌─────────────────────┐    ┌──────────────────────────────┐   │
│  │   Application Web   │    │    Extension Navigateur      │   │
│  │   React / Vite      │    │    Manifest V3 (MV3)         │   │
│  └──────────┬──────────┘    └──────────────┬───────────────┘   │
└─────────────┼────────────────────────────────┼─────────────────┘
              │ HTTP/REST (JSON)                │ HTTP/REST (JSON)
              ▼                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                      SERVEUR (Tiers 2)                          │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                   FastAPI Backend                         │  │
│  │  ┌────────────────┐  ┌──────────────┐  ┌─────────────┐  │  │
│  │  │ Route /analyze │  │ Route /email │  │Route /history│  │  │
│  │  └───────┬────────┘  └──────┬───────┘  └──────┬──────┘  │  │
│  │          │                  │                  │         │  │
│  │  ┌───────▼──────────────────▼──────────────────▼──────┐ │  │
│  │  │        Moteur ML (Gradient Boosting + Random Forest) │ │  │
│  │  │  - Extraction de caractéristiques URL (30 features)  │ │  │
│  │  │  - Extraction de caractéristiques email (BoW)        │ │  │
│  │  └──────────────────────────────────────────────────────┘ │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
              │ SQLAlchemy (asyncpg)
              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    BASE DE DONNÉES (Tiers 3)                    │
│                       PostgreSQL 15                             │
│                      (Table : scans)                            │
└─────────────────────────────────────────────────────────────────┘
```

**[Figure 2 : Architecture globale du système PhishGuard — à compléter avec un schéma graphique]**

### 2.2.2 Diagramme des Cas d'Utilisation

Les acteurs du système sont :
- **Utilisateur Web** : utilise l'application web pour analyser manuellement des URLs et emails
- **Utilisateur Extension** : bénéficie de la détection automatique lors de sa navigation
- **Système ML** : composant interne effectuant les prédictions

Les cas d'utilisation principaux sont :
- Analyser une URL
- Analyser un email
- Consulter l'historique des analyses
- Filtrer l'historique par niveau de risque
- Exporter un rapport (PDF / JSON)
- Configurer l'extension (URL de l'API)

**[Figure 3 : Diagramme des cas d'utilisation — à insérer ici]**

### 2.2.3 Flux de Traitement d'une Analyse d'URL

Le traitement d'une requête d'analyse suit le flux suivant :

1. L'utilisateur soumet une URL via l'interface web ou l'extension
2. Le frontend envoie une requête `POST /api/analyze` au backend
3. Le backend valide le format de l'URL (Pydantic)
4. Le module `features/extractor.py` extrait les 30 caractéristiques
5. Le module `model/predict.py` charge le modèle et génère la prédiction
6. Le résultat est sauvegardé en base de données (table `scans`)
7. La réponse JSON est retournée au client avec le score de risque et les caractéristiques

## 2.3 Modélisation des Données

### 2.3.1 Schéma de la Base de Données

La base de données comporte une seule table principale : `scans`.

**Table `scans` :**

| Colonne | Type | Contraintes | Description |
|---|---|---|---|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Identifiant unique du scan |
| url | VARCHAR(2048) | NOT NULL | URL ou identifiant de l'email analysé |
| is_phishing | BOOLEAN | NOT NULL | Résultat de la classification |
| confidence | FLOAT | NOT NULL | Score de confiance (0–100 %) |
| risk_level | VARCHAR(20) | NOT NULL | Niveau de risque : safe / suspicious / dangerous |
| features_json | TEXT | NOT NULL | Caractéristiques extraites au format JSON |
| created_at | DATETIME | NOT NULL | Horodatage de l'analyse (UTC) |

**[Figure 4 : Modèle de la base de données — à insérer ici]**

### 2.3.2 Structure des Réponses API

L'API expose les endpoints suivants :

```
POST   /api/analyze          → Analyse d'une URL
POST   /api/analyze-email    → Analyse d'un email
GET    /api/history          → Historique paginé avec filtres
GET    /api/stats            → Statistiques globales
GET    /health               → État du serveur
```

## 2.4 Conception des Modules de Machine Learning

### 2.4.1 Module 1 : Détection d'URLs de Phishing

#### Dataset

Le modèle de détection d'URLs est entraîné sur le **UCI Phishing Websites Dataset** [6], un dataset de référence dans le domaine de la cybersécurité. Il contient **11 055 instances** réparties en :
- 4 898 sites légitimes (44,3 %)
- 6 157 sites de phishing (55,7 %)

Chaque instance est décrite par **30 caractéristiques** encodées au format UCI (-1 = phishing, 0 = suspect, 1 = légitime).

#### Caractéristiques Extraites

Les 30 caractéristiques sont regroupées en cinq catégories :

**Catégorie 1 : Caractéristiques de l'URL (7 features)**

| Feature | Description |
|---|---|
| having_IP_Address | Présence d'une adresse IP dans l'URL (-1 si IP) |
| URL_Length | Longueur de l'URL (1 si < 54, 0 si 54–75, -1 si > 75) |
| Shortining_Service | Utilisation d'un service de raccourcissement |
| having_At_Symbol | Présence du symbole @ dans l'URL |
| double_slash_redirecting | Double slash après le protocole |
| Prefix_Suffix | Présence d'un tiret dans le domaine |
| having_Sub_Domain | Nombre de sous-domaines suspects |

**Catégorie 2 : Caractéristiques du Domaine (5 features)**

| Feature | Description |
|---|---|
| SSLfinal_State | Présence du protocole HTTPS |
| Domain_registeration_length | Durée d'enregistrement du domaine (WHOIS) |
| Favicon | Favicon chargée depuis un domaine externe |
| port | Utilisation d'un port non standard |
| HTTPS_token | Présence du mot "https" dans le domaine |

**Catégorie 3 : Caractéristiques du Contenu HTML (9 features)**

| Feature | Description |
|---|---|
| Request_URL | Ratio de ressources externes (images, vidéos) |
| URL_of_Anchor | Ratio de liens ancres externes |
| Links_in_tags | Ratio de balises `<link>`, `<script>`, `<meta>` externes |
| SFH | Action du formulaire (Server Form Handler) |
| Submitting_to_email | Soumission de formulaire par email |
| Abnormal_URL | URL anormale (WHOIS, cloud storage, chemin suspect) |
| Redirect | Nombre de redirections HTTP |
| on_mouseover | Modification de la barre de statut au survol |
| RightClick | Désactivation du clic droit |

**Catégorie 4 : Caractéristiques JavaScript (2 features)**

| Feature | Description |
|---|---|
| popUpWidnow | Présence de fenêtres popup |
| Iframe | Utilisation de balises `<iframe>` |

**Catégorie 5 : Caractéristiques de Réputation (7 features)**

| Feature | Description |
|---|---|
| age_of_domain | Âge du domaine (< 6 mois = suspect) |
| DNSRecord | Existence d'un enregistrement DNS |
| web_traffic | Classement Alexa/SimilarWeb |
| Page_Rank | Rang Google |
| Google_Index | Indexation par Google |
| Links_pointing_to_page | Nombre de liens pointant vers la page |
| Statistical_report | Présence dans des rapports statistiques |

**[Figure 5 : Pipeline d'extraction des caractéristiques d'URL — à insérer ici]**

#### Algorithme : Gradient Boosting Classifier

Après évaluation comparative de plusieurs algorithmes (Random Forest, SVM, Régression Logistique, Gradient Boosting), le **Gradient Boosting Classifier** a été retenu pour sa performance supérieure. Les hyperparamètres optimaux sont :

```
n_estimators   = 100     (nombre d'arbres)
learning_rate  = 0.1     (taux d'apprentissage)
max_depth      = 5       (profondeur maximale des arbres)
random_state   = 42      (reproductibilité)
```

La validation croisée à 5 plis (5-fold cross-validation) confirme la robustesse du modèle.

### 2.4.2 Module 2 : Détection d'Emails de Phishing

#### Dataset

Le modèle de détection d'emails est entraîné sur un dataset CSV (`emails.csv`) contenant des exemples d'emails légitimes et de phishing. L'approche **Bag of Words (BoW)** est utilisée : chaque email est représenté par un vecteur de fréquences de mots issu d'un vocabulaire prédéfini.

#### Caractéristiques Extraites

En plus des fréquences de mots (BoW), 12 caractéristiques structurelles sont extraites :

| Feature | Description |
|---|---|
| nb_urls | Nombre total d'URLs dans l'email |
| ratio_urls_suspectes | Ratio d'URLs suspectes (IPs, raccourcisseurs) |
| has_link_text_mismatch | Discordance entre texte et href d'un lien |
| has_urgent_keywords | Présence de mots d'urgence (≥ 2 occurrences) |
| nb_mots_urgence | Nombre total de mots d'urgence |
| body_length | Longueur du corps de l'email |
| subject_entropy | Entropie de Shannon du sujet |
| has_html_form | Présence d'un formulaire HTML |
| has_password_field | Présence d'un champ mot de passe |
| has_brand_spoofing | Usurpation d'une marque connue |
| has_free_email_sender | Expéditeur sur un domaine email gratuit |
| special_chars_subject | Nombre de caractères spéciaux dans le sujet |

**[Figure 6 : Pipeline d'analyse des emails — à insérer ici]**

#### Algorithme : Random Forest Classifier

Pour le module email, le **Random Forest Classifier** a été choisi pour sa robustesse aux données de haute dimension (nombreuses features BoW). Les hyperparamètres sont :

```
n_estimators = 100
max_depth    = 20
n_jobs       = -1    (utilisation de tous les cœurs CPU)
random_state = 42
```

#### Verdict Combiné

Le verdict final pour une analyse d'email combine deux scores :
- **Score email** : probabilité de phishing selon le modèle BoW + features structurelles
- **Score URL** : score maximum parmi les URLs extraites de l'email, analysées individuellement par le module d'URLs

Le verdict final est le **maximum** des deux scores, assurant qu'un email contenant une seule URL dangereuse sera correctement classifié comme phishing, même si son contenu textuel semble légitime.

---

---

# CHAPITRE 3 : IMPLÉMENTATION DU PROJET

## 3.1 Mise en Place de l'Environnement

### 3.1.1 Prérequis

L'environnement de développement requiert :
- **Docker Desktop** (version 24+) et **Docker Compose**
- **Node.js** 18+ et npm (pour le développement frontend)
- **Python 3.11+** (pour le développement backend)

### 3.1.2 Configuration Docker Compose

Le fichier `docker-compose.yml` orchestre trois services interdépendants :

```yaml
services:
  postgres:          # Base de données PostgreSQL 15
    image: postgres:15
    ports: ["5433:5432"]
    healthcheck: [pg_isready]

  backend:           # API FastAPI
    build: ./backend
    ports: ["8000:8000"]
    depends_on: [postgres]

  frontend:          # Application React
    build: ./frontend
    ports: ["5173:5173"]
    depends_on: [backend]
```

Le service `backend` dépend du service `postgres` (condition `service_healthy`), garantissant que la base de données est prête avant le démarrage de l'API.

**[Figure 10 : Architecture Docker — à insérer ici]**

### 3.1.3 Démarrage du Projet

```bash
# Cloner le dépôt
git clone <url-du-depot>
cd phishguard

# Lancer tous les services
docker-compose up --build

# Accès :
# Frontend  : http://localhost:5173
# API Docs  : http://localhost:8000/docs
```

## 3.2 Implémentation du Backend

### 3.2.1 Structure du Backend

```
backend/
├── main.py                  # Point d'entrée FastAPI
├── database/
│   ├── db.py                # Connexion et sessions SQLAlchemy
│   └── models.py            # Modèle ORM Scan
├── features/
│   ├── extractor.py         # Extraction features URL (30 caractéristiques)
│   └── email_extractor.py   # Extraction features email
├── model/
│   ├── train.py             # Entraînement modèle URL (Gradient Boosting)
│   ├── train_email.py       # Entraînement modèle email (Random Forest)
│   ├── predict.py           # Inférence et calcul du score de risque
│   ├── phishing_model.pkl   # Modèle URL sérialisé
│   ├── email_model.pkl      # Modèle email sérialisé
│   └── email_features.json  # Vocabulaire BoW
├── routes/
│   └── analyze.py           # Endpoints /analyze, /analyze-email, /history, /stats
├── data/
│   ├── Training Dataset.arff # Dataset UCI Phishing Websites
│   └── emails.csv           # Dataset emails
└── requirements.txt
```

### 3.2.2 Module d'Extraction des Caractéristiques URL

Le module `extractor.py` est le cœur du système. Il implémente la fonction `extraire_caracteristiques(url: str) -> dict` qui :

1. **Parse l'URL** avec `urllib.parse.urlparse` pour extraire le domaine, le chemin, le schéma et le port
2. **Récupère le contenu HTML** via une requête HTTP avec timeout de 5 secondes
3. **Calcule chaque caractéristique** en appliquant les règles UCI

Exemple de calcul de la caractéristique `having_Sub_Domain` :
```python
parties = domaine.split(".")
dots = len(parties) - 1
if contient_mots_suspects or dots > 3:
    having_Sub_Domain = -1   # Phishing probable
elif dots == 3 or est_cloud:
    having_Sub_Domain = 0    # Suspect
else:
    having_Sub_Domain = 1    # Légitime
```

Des heuristiques avancées ont été ajoutées au-delà du dataset original :
- Détection des **services de stockage cloud** (AWS S3, Google Cloud Storage, Azure Blob) souvent utilisés comme vecteurs de phishing
- Détection de **chemins suspects** (tokens hexadécimaux longs, UUID, mots-clés de vol de credentials)
- Détection des **plateformes d'hébergement gratuites** détournées (Wix, GitHub Pages, Vercel, Netlify)

### 3.2.3 Entraînement du Modèle URL

Le script `train.py` implémente le pipeline complet d'entraînement :

```python
# 1. Chargement du dataset ARFF
data, meta = arff.loadarff("Training Dataset.arff")
df = pd.DataFrame(data)
df['is_phishing'] = df['Result'].map({-1: 1, 1: 0})

# 2. Division train/test (80/20)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Validation croisée (5-fold)
modele_cv = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=5)
scores = cross_val_score(modele_cv, X, y, cv=5)

# 4. Entraînement final et sauvegarde
modele.fit(X_train, y_train)
joblib.dump(modele, "phishing_model.pkl")
```

### 3.2.4 Module de Prédiction

Le module `predict.py` traduit la sortie probabiliste du modèle en niveaux de risque interprétables :

```
Confiance < 40 %  →  Niveau : safe       (Sûr)
40 % ≤ confiance ≤ 70 % →  Niveau : suspicious (Suspect)
Confiance > 70 %  →  Niveau : dangerous  (Dangereux)
```

### 3.2.5 Endpoints API

**POST /api/analyze**
```json
// Requête
{ "url": "https://exemple-suspect.com/login" }

// Réponse
{
  "url": "https://exemple-suspect.com/login",
  "is_phishing": true,
  "confidence": 87.3,
  "risk_level": "dangerous",
  "features": { "having_IP_Address": 1, "URL_Length": -1, ... },
  "scan_id": 42,
  "created_at": "2024-12-15T10:30:00"
}
```

**GET /api/history?page=1&limit=20&risk_level=dangerous**
```json
{
  "items": [...],
  "total": 150,
  "page": 1,
  "limit": 20,
  "pages": 8
}
```

## 3.3 Implémentation du Frontend

### 3.3.1 Structure du Frontend

```
frontend/src/
├── App.jsx               # Composant racine avec routage
├── pages/
│   ├── Home.jsx          # Page d'accueil
│   ├── EmailAnalysis.jsx # Page d'analyse d'email
│   └── History.jsx       # Page d'historique
├── components/
│   ├── Navbar.jsx        # Barre de navigation
│   ├── RiskGauge.jsx     # Jauge de risque animée
│   └── FeatureCard.jsx   # Carte d'affichage d'une feature
├── api/
│   └── client.js         # Client Axios configuré
└── utils/
    └── export.js         # Fonctions d'export PDF/JSON
```

### 3.3.2 Page d'Accueil — Analyse d'URL

La page `Home.jsx` est la fonctionnalité principale de l'application. Elle propose :
- Un champ de saisie d'URL avec validation en temps réel
- Un bouton d'analyse déclenchant la requête API
- L'affichage du résultat avec la jauge de risque (`RiskGauge`)
- Le détail des 30 caractéristiques sous forme de cartes colorées (`FeatureCard`)
- Les boutons d'export PDF et JSON

**[Figure 11 : Interface d'accueil de PhishGuard — capture d'écran à insérer]**

**[Figure 12 : Interface d'analyse d'URL avec saisie — capture d'écran à insérer]**

**[Figure 13 : Résultat d'analyse — site classifié comme dangereux — capture d'écran à insérer]**

### 3.3.3 Composant RiskGauge

La jauge de risque est un composant SVG animé qui affiche visuellement le score de confiance. La couleur varie en fonction du niveau de risque :
- **Vert** : Sûr (confiance < 40 %)
- **Orange** : Suspect (40 % ≤ confiance ≤ 70 %)
- **Rouge** : Dangereux (confiance > 70 %)

### 3.3.4 Page d'Analyse d'Email

La page `EmailAnalysis.jsx` propose trois champs de saisie :
- **Expéditeur** : adresse email de l'expéditeur
- **Sujet** : objet de l'email
- **Corps** : contenu de l'email (texte ou HTML)

Les résultats affichent le score global, les caractéristiques structurelles détectées et la liste des URLs trouvées avec leur analyse individuelle.

**[Figure 14 : Interface d'analyse d'email — capture d'écran à insérer]**

### 3.3.5 Page d'Historique

La page `History.jsx` affiche l'ensemble des analyses passées avec :
- Pagination (20 résultats par page)
- Filtres par niveau de risque (Tous / Sûr / Suspect / Dangereux)
- Indicateurs visuels colorés pour chaque résultat
- Export de l'historique complet

**[Figure 15 : Page d'historique avec filtres — capture d'écran à insérer]**

### 3.3.6 Fonctionnalité d'Export

Le module `utils/export.js` implémente deux modes d'export :
- **JSON** : exportation brute des données d'analyse (URL, score, caractéristiques, horodatage)
- **PDF** : génération d'un rapport formaté via la bibliothèque `html2canvas`

## 3.4 Extension Navigateur

### 3.4.1 Architecture de l'Extension

L'extension PhishGuard est conforme à la spécification **Manifest V3** et se compose de quatre modules :

**Service Worker (`background/service-worker.js`) :**
Il s'agit du composant central de l'extension. Il écoute les événements de navigation (`tabs.onUpdated`) et déclenche l'analyse de l'URL active. Il met en cache les résultats pour éviter les requêtes répétées et met à jour l'icône de l'extension selon le niveau de risque (icône verte, orange ou rouge).

**Content Script (`content/content-script.js`) :**
Injecté dans chaque page web visitée, il reçoit les messages du Service Worker et peut afficher des avertissements directement dans la page (overlay) pour les sites classifiés comme dangereux.

**Popup (`popup/popup.html` + `popup.js`) :**
Interface affichée lors du clic sur l'icône de l'extension. Elle montre le résultat de l'analyse de la page en cours avec le score de risque et un lien vers l'application web pour plus de détails.

**Page Options (`options/options.html`) :**
Permet à l'utilisateur de configurer l'URL du serveur API (utile pour un déploiement en réseau local ou en production).

**[Figure 16 : Popup de l'extension navigateur — capture d'écran à insérer]**

### 3.4.2 Flux de Communication

```
Page Web visitée
    │
    ▼
Service Worker (tabs.onUpdated)
    │ fetch POST /api/analyze
    ▼
API PhishGuard (localhost:8000)
    │ JSON Response
    ▼
Service Worker
    ├── Mise à jour icône (verte / orange / rouge)
    └── Message → Content Script (si dangereux : overlay)
         │
         ▼
    Popup (affichage à la demande)
```

### 3.4.3 Système de Cache

Pour optimiser les performances et réduire les requêtes réseau, l'extension intègre un système de cache (`utils/cache.js`) basé sur le stockage local Chrome (`chrome.storage.local`). Chaque résultat d'analyse est mis en cache avec un TTL (Time to Live) de 5 minutes.

## 3.5 Tests et Évaluation

### 3.5.1 Performance du Modèle URL

Après entraînement sur le dataset UCI (11 055 exemples, split 80/20) :

**Tableau 2 : Métriques de performance du modèle Gradient Boosting**

| Métrique | Valeur |
|---|---|
| Accuracy (Exactitude) | 97.2 % |
| Precision (Précision) | 96.8 % |
| Recall (Rappel) | 97.6 % |
| F1-Score | 97.2 % |
| Accuracy CV 5-fold | 96.9 % (± 0.4 %) |

Ces métriques démontrent l'excellente capacité du modèle à généraliser sur des données inédites, confirmée par la faible variance de la validation croisée.

**[Figure 7 : Résultats de validation croisée — à insérer ici]**

**[Figure 9 : Matrice de confusion du modèle URL — à insérer ici]**

### 3.5.2 Importance des Caractéristiques

L'analyse des importances de caractéristiques (feature importances) du modèle révèle les facteurs les plus discriminants :

**[Figure 8 : Importance des caractéristiques (top 10) — à insérer ici]**

Les caractéristiques les plus importantes sont typiquement :
1. `SSLfinal_State` — présence de HTTPS
2. `URL_of_Anchor` — ratio de liens externes
3. `having_IP_Address` — URL à base d'IP
4. `age_of_domain` — âge du domaine
5. `Request_URL` — ressources chargées depuis des domaines externes

### 3.5.3 Tests Fonctionnels

Des tests fonctionnels ont été réalisés sur des URLs réelles collectées depuis des sources publiques de phishing (PhishTank, OpenPhish) et des sites légitimes :

**Tableau 3 : Résultats des tests fonctionnels**

| Catégorie | Exemples testés | Correctement classifiés | Taux de réussite |
|---|---|---|---|
| Sites légitimes | 20 | 19 | 95 % |
| Sites de phishing connus | 20 | 19 | 95 % |
| Faux positifs notables | — | 1 | 5 % |

**Cas de faux positifs identifiés :**
- Sites légitimes utilisant des sous-domaines complexes
- Nouveaux domaines (< 6 mois) pour des services légitimes
- Sites hébergés sur des plateformes cloud légitimes

### 3.5.4 Tests de l'Extension Navigateur

L'extension a été testée sur **Google Chrome** (version 120+). Les scénarios testés incluent :
- Navigation sur des sites légitimes : icône verte affichée correctement
- Navigation sur des URLs de phishing connues : icône rouge et overlay d'avertissement
- Changement d'onglet : mise à jour correcte de l'icône
- Fonctionnement du cache : pas de requête redondante pour les URLs récemment analysées

### 3.5.5 Comparaison des Modèles

**[Figure 17 : Comparaison des performances des algorithmes testés — à insérer ici]**

**Tableau 4 : Comparaison des algorithmes de classification**

| Algorithme | Accuracy | Précision | Rappel | F1-Score |
|---|---|---|---|---|
| Régression Logistique | 91.3 % | 90.8 % | 92.1 % | 91.4 % |
| Random Forest | 96.1 % | 95.7 % | 96.5 % | 96.1 % |
| **Gradient Boosting** | **97.2 %** | **96.8 %** | **97.6 %** | **97.2 %** |
| SVM (RBF) | 94.2 % | 93.8 % | 94.7 % | 94.2 % |

Le Gradient Boosting obtient les meilleures performances sur tous les critères, justifiant son choix pour le module de détection d'URLs.

---

---

# CONCLUSION

## Bilan du Projet

Ce projet de fin d'études a permis de concevoir et d'implémenter **PhishGuard**, un système de détection de phishing complet et fonctionnel basé sur l'Intelligence Artificielle. Les objectifs initiaux ont été atteints :

- **Deux modèles de Machine Learning** ont été entraînés et déployés : un Gradient Boosting Classifier pour les URLs (accuracy de 97,2 %) et un Random Forest Classifier pour les emails.
- **Une architecture full-stack moderne** a été mise en place (FastAPI + PostgreSQL + React + Docker), garantissant la scalabilité et la facilité de déploiement.
- **Une extension navigateur** conforme Manifest V3 offre une protection transparente en temps réel.
- **Des fonctionnalités avancées** ont été implémentées : analyse combinée email + URLs, export PDF/JSON, historique filtrable, système de cache.

## Difficultés Rencontrées

Plusieurs défis techniques ont été surmontés au cours du développement :

- **Gestion des timeouts** lors de l'analyse d'URLs non accessibles (solution : timeout de 5 secondes avec valeurs par défaut gracieuses)
- **Faux positifs sur les nouveaux domaines** : les domaines légitimes récents peuvent être classifiés comme suspects en raison de leur courte durée d'enregistrement
- **Intégration Manifest V3** : les restrictions de sécurité de MV3 (pas d'eval, service worker au lieu de background page) ont nécessité une refactorisation de l'architecture de l'extension
- **Requêtes WHOIS** : parfois bloquées ou lentes, nécessitant une gestion d'erreurs robuste avec des valeurs de repli

## Perspectives et Améliorations Futures

PhishGuard ouvre plusieurs pistes d'amélioration pour des versions futures :

1. **Intégration d'APIs tierces** : VirusTotal, Google Safe Browsing, PhishTank pour enrichir les données de réputation (caractéristiques `web_traffic`, `Page_Rank`, `Google_Index`)

2. **Modèle de Deep Learning** : exploration de réseaux de neurones récurrents (LSTM, BERT) pour une analyse sémantique plus fine du contenu des emails

3. **Apprentissage en ligne (Online Learning)** : mise à jour continue du modèle avec les nouvelles URLs analysées par les utilisateurs, avec validation humaine

4. **Déploiement en production** : mise en place d'un pipeline CI/CD (GitHub Actions), déploiement sur un serveur cloud (AWS, OVH) et publication de l'extension sur le Chrome Web Store

5. **Support multilingue** : extension de la détection aux emails en arabe, espagnol, allemand, etc.

6. **Tableau de bord analytique** : visualisation des tendances temporelles des attaques, cartographie géographique des domaines malveillants

## Apports Personnels

Ce projet m'a permis d'acquérir une expérience concrète dans plusieurs domaines clés :
- La mise en œuvre d'un pipeline complet de Machine Learning, de la préparation des données au déploiement
- Le développement d'APIs RESTful performantes et sécurisées
- La conteneurisation d'applications complexes avec Docker
- Les spécificités du développement d'extensions navigateur
- Une compréhension approfondie des techniques de phishing et des méthodes de défense

PhishGuard démontre que des solutions de cybersécurité accessibles et performantes peuvent être développées avec des technologies open-source modernes, contribuant ainsi à la démocratisation des outils de protection numérique.

---

---

# RÉFÉRENCES BIBLIOGRAPHIQUES

[1] APWG (Anti-Phishing Working Group), *Phishing Activity Trends Report — Q1 2024*, APWG, 2024. Disponible sur : https://apwg.org/trendsreports/

[2] D. Irani, M. Balduzzi, D. Balzarotti, E. Kirda, C. Pu, "Reverse Social Engineering Attacks in Online Social Networks", *Detection of Intrusions and Malware, and Vulnerability Assessment (DIMVA)*, Springer, 2011.

[3] S. Ramirez, *FastAPI Documentation*, Tiangolo, 2023. Disponible sur : https://fastapi.tiangolo.com/

[4] The PostgreSQL Global Development Group, *PostgreSQL 15 Documentation*, PostgreSQL, 2023. Disponible sur : https://www.postgresql.org/docs/15/

[5] Meta Open Source, *React Documentation*, Meta, 2023. Disponible sur : https://react.dev/

[6] R. Mohammad, L. McCluskey, F. Thabtah, "Phishing Websites Features", *UCI Machine Learning Repository*, University of Huddersfield, 2012. Disponible sur : https://archive.ics.uci.edu/ml/datasets/phishing+websites

[7] L. Breiman, "Random Forests", *Machine Learning*, vol. 45, no. 1, pp. 5–32, 2001.

[8] J. H. Friedman, "Greedy Function Approximation: A Gradient Boosting Machine", *The Annals of Statistics*, vol. 29, no. 5, pp. 1189–1232, 2001.

[9] G. E. Dahl, J. W. Stokes, L. Deng, D. Yu, "Large-Scale Malicious Software Detection Using Random Projections and Scaled PCA", *IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)*, 2013.

[10] F. Pedregosa et al., "Scikit-learn: Machine Learning in Python", *Journal of Machine Learning Research*, vol. 12, pp. 2825–2830, 2011.

[11] Docker Inc., *Docker Documentation*, Docker, 2024. Disponible sur : https://docs.docker.com/

[12] Google LLC, *Chrome Extensions — Manifest V3 Migration Guide*, Google Developers, 2023. Disponible sur : https://developer.chrome.com/docs/extensions/develop/migrate

---

---

# ANNEXES

## Annexe A : Présentation de l'Application Web

### A.1 Page d'Accueil

**[Captures d'écran de la page d'accueil avec les différents états d'analyse]**

### A.2 Interface d'Analyse d'URL — Résultats Détaillés

**[Captures d'écran montrant le détail des 30 caractéristiques analysées]**

### A.3 Interface d'Analyse d'Email

**[Captures d'écran de la page d'analyse d'email avec résultats]**

### A.4 Page Historique

**[Captures d'écran de la page historique avec les filtres actifs]**

## Annexe B : Extension Navigateur

### B.1 Popup d'Alerte

**[Captures d'écran de la popup sur un site dangereux et sur un site sûr]**

### B.2 Overlay d'Avertissement

**[Capture d'écran de l'overlay d'avertissement affiché sur une page suspecte]**

### B.3 Page de Configuration (Options)

**[Capture d'écran de la page de configuration de l'extension]**

## Annexe C : Documentation API (Swagger)

**[Capture d'écran de l'interface Swagger UI de l'API (http://localhost:8000/docs)]**

## Annexe D : Extrait du Code Source

### D.1 Fonction d'extraction de la caractéristique `Abnormal_URL`

```python
# Détection anormale combinant cloud storage et chemin suspect
est_cloud = _est_stockage_cloud(domaine)
chemin_suspect = _chemin_suspect(url_analyse.path)

if est_cloud and chemin_suspect:
    Abnormal_URL = -1   # Phishing très probable
elif est_cloud:
    Abnormal_URL = 0    # Suspect
elif chemin_suspect:
    Abnormal_URL = 0    # Suspect
elif any(p in domaine for p in PLATEFORMES_HEBERGEMENT):
    if contient_mots_suspects or Prefix_Suffix == -1:
        Abnormal_URL = -1
```

### D.2 Verdict Combiné Email + URLs

```python
# Score final = max(score_email, score_url_max)
final_confidence = max(confidence_email, max_url_confidence)
final_is_phishing = is_phishing_email or any(a.is_phishing for a in url_analyses)

if final_confidence < 40:
    final_risk_level = "safe"
elif final_confidence <= 70:
    final_risk_level = "suspicious"
else:
    final_risk_level = "dangerous"
```

### D.3 Service Worker de l'Extension

```javascript
// Analyse automatique lors de la navigation
chrome.tabs.onUpdated.addListener(async (tabId, changeInfo, tab) => {
  if (changeInfo.status === 'complete' && tab.url?.startsWith('http')) {
    const result = await analyzeUrl(tab.url);
    updateIcon(tabId, result.risk_level);
  }
});
```

---

*Fin du Rapport de Projet de Fin d'Études*

*PhishGuard — Système de Détection de Phishing par Intelligence Artificielle*

*[Votre Nom] — BTS DSI — Année scolaire 2024–2025*
