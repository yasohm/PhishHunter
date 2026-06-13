import os
import json
import re
import math
from urllib.parse import urlparse
from bs4 import BeautifulSoup

# Mots-clés de phishing
MOTS_URGENCE = [
    "urgent", "verify", "suspended", "confirm", "update", "validate", 
    "account", "password", "click here", "limited time", "act now", 
    "dear customer", "winner", "congratulations", "free", "prize", 
    "bank", "paypal", "amazon", "microsoft", "apple", "security alert"
]

# Marques pour la détection de spoofing
MARQUES = [
    "paypal", "amazon", "microsoft", "apple", "google", 
    "facebook", "netflix", "bank", "dhl", "fedex"
]

# Domaines d'emails gratuits
DOMAINES_GRATUITS = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com"]

# Raccourcisseurs d'URL (pour ratio_urls_suspectes)
RACCOURCISSEURS = [
    "bit.ly", "t.co", "tinyurl.com", "rebrand.ly", "is.gd",
    "buff.ly", "goo.gl", "bit.do", "ow.ly"
]

def _calculer_entropie(chaine: str) -> float:
    """Calcule l'entropie de Shannon d'une chaîne."""
    if not chaine:
        return 0.0
    probabilites = [float(chaine.count(c)) / len(chaine) for c in set(chaine)]
    entropie = -sum(p * math.log2(p) for p in probabilites)
    return round(entropie, 4)

def _est_adresse_ip(domaine: str) -> bool:
    """Vérifie si le domaine est une adresse IP."""
    patron_ip = re.compile(r"^(\d{1,3}\.){3}\d{1,3}$")
    return bool(patron_ip.match(domaine))

def extraire_frequences_mots(texte: str, vocab: list) -> dict:
    """
    Extrait les fréquences des mots du vocabulaire dans un texte donné.
    Simule le format du dataset emails.csv.
    """
    mots_texte = re.findall(r'\b\w+\b', texte.lower())
    freq = {}
    for mot in vocab:
        freq[mot] = mots_texte.count(mot)
    return freq

def extraire_caracteristiques_email(sujet: str, corps: str, expediteur: str = "") -> dict:
    """
    Extrait les caractéristiques d'un email pour la détection de phishing.
    """
    # Nettoyage et préparation
    corps_lower = corps.lower()
    sujet_lower = sujet.lower()
    expediteur_lower = expediteur.lower()
    
    # Parser HTML si nécessaire
    soup = BeautifulSoup(corps, "html.parser")
    
    # 1. nb_urls
    urls = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', corps)
    # Extraire aussi des href des tags <a>
    links = soup.find_all('a', href=True)
    for link in links:
        href = link['href']
        if href.startswith(('http', 'www')):
            urls.append(href)
    
    urls = list(set(urls)) # Unique URLs
    nb_urls = len(urls)
    
    # 2. ratio_urls_suspectes
    nb_suspectes = 0
    for url in urls:
        parsed = urlparse(url if url.startswith('http') else 'http://' + url)
        domaine = parsed.netloc.lower()
        if _est_adresse_ip(domaine) or any(r in domaine for r in RACCOURCISSEURS):
            nb_suspectes += 1
    
    ratio_urls_suspectes = nb_suspectes / nb_urls if nb_urls > 0 else 0.0
    
    # 3. has_link_text_mismatch
    has_link_text_mismatch = 0
    for link in links:
        href = link['href']
        text = link.get_text().strip()
        if href.startswith(('http', 'www')) and text.startswith(('http', 'www')):
            # Si le texte ressemble à une URL, elle doit correspondre au href
            parsed_href = urlparse(href if href.startswith('http') else 'http://' + href).netloc.lower()
            parsed_text = urlparse(text if text.startswith('http') else 'http://' + text).netloc.lower()
            if parsed_href != parsed_text and parsed_text != "":
                 has_link_text_mismatch = 1
                 break

    # 4 & 5. nb_mots_urgence & has_urgent_keywords
    nb_mots_urgence = 0
    for mot in MOTS_URGENCE:
        # Recherche insensible à la casse dans le sujet et le corps
        nb_mots_urgence += sujet_lower.count(mot)
        nb_mots_urgence += corps_lower.count(mot)
    
    has_urgent_keywords = 1 if nb_mots_urgence >= 2 else 0
    
    # 6. body_length
    body_length = len(corps)
    
    # 7. subject_entropy
    subject_entropy = _calculer_entropie(sujet)
    
    # 8. has_html_form
    has_html_form = 1 if soup.find("form") else 0
    
    # 10. has_password_field
    has_password_field = 1 if soup.find("input", {"type": "password"}) else 0
    
    # 11. has_brand_spoofing
    has_brand_spoofing = 0
    if sujet_lower:
        sender_domain = expediteur_lower.split('@')[-1] if '@' in expediteur_lower else ""
        for marque in MARQUES:
            if marque in sujet_lower:
                if sender_domain and marque not in sender_domain:
                    has_brand_spoofing = 1
                    break

    # 12. has_free_email_sender
    has_free_email_sender = 0
    if expediteur_lower:
        if any(dom in expediteur_lower for dom in DOMAINES_GRATUITS):
            has_free_email_sender = 1
            
    # 13. special_chars_subject
    # count of !, $, %, @, #, *
    special_chars_subject = sum(sujet.count(c) for c in ['!', '$', '%', '@', '#', '*'])
    
    
    # --- Nouvelles caractéristiques pour le modèle (Bag of Words) ---
    # Charger le vocabulaire utilisé lors de l'entraînement
    chemin_vocab = os.path.join(os.path.dirname(os.path.dirname(__file__)), "model", "email_features.json")
    model_features = {}
    if os.path.exists(chemin_vocab):
        with open(chemin_vocab, "r") as f:
            vocab = json.load(f)
        texte_complet = f"{sujet} {corps}"
        model_features = extraire_frequences_mots(texte_complet, vocab)
    
    return {
        "features": {
            "nb_urls": nb_urls,
            "ratio_urls_suspectes": ratio_urls_suspectes,
            "has_link_text_mismatch": has_link_text_mismatch,
            "has_urgent_keywords": has_urgent_keywords,
            "nb_mots_urgence": nb_mots_urgence,
            "body_length": body_length,
            "subject_entropy": subject_entropy,
            "has_html_form": has_html_form,
            "has_password_field": has_password_field,
            "has_brand_spoofing": has_brand_spoofing,
            "has_free_email_sender": has_free_email_sender,
            "special_chars_subject": special_chars_subject,
        },
        "model_features": model_features,
        "urls_extraites": urls
    }
