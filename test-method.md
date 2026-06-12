# Module Attaquant — Simulation de phishing
Ce module permet de simuler une campagne de phishing réaliste à des fins de test et de démonstration. Il est strictement utilisé dans un environnement contrôlé avec des comptes emails de test.

## 5.1 Outil principal : GoPhish
GoPhish est un framework open-source de simulation de phishing. Il permet de créer des campagnes complètes avec des templates d'emails personnalisés, des landing pages de capture, et un suivi des clics et des soumissions.
    • Création de templates d'emails imitant des marques connues (format HTML)
    • Hébergement d'une fausse page de connexion (landing page) sur un serveur local
    • Envoi d'emails via un serveur SMTP configuré (Mailtrap pour les tests)
    • Tableau de bord GoPhish : suivi des emails ouverts, clics sur les liens, données soumises

### Configuration de l'environnement de test
	• Serveur SMTP de test : Mailtrap.io (capture les emails sans les envoyer réellement)
	• Landing page hébergée localement sur localhost:8080 (simulateur)
	• Comptes email de test créés spécifiquement pour la démonstration
	• Aucun email réel ne sera envoyé à des personnes réelles

## 5.2 Simulateur Python complémentaire
Un script Python custom sera développé pour simuler des emails de phishing avec des paramètres configurables :
    • Choix du template : banque, PayPal, Microsoft, Netflix, etc.
    • Génération d'une URL de phishing factice avec les features caractéristiques
    • Envoi via smtplib vers Mailtrap avec headers complets
    • Logging de chaque email envoyé dans la base de données

# Outil Usage dans le module attaquant
GoPhish v0.12+ -> Framework complet de campagne phishing (emails + landing pages)
Python smtplib -> Script de génération et envoi d'emails de test personnalisés
Mailtrap.io -> Serveur SMTP de test — capture les emails sans envoi réel
Jinja2 -> Templating des emails HTML de phishing
Flask (landing page) -> Hébergement de la fausse page de connexion en local

