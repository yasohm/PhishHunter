import re
import math
import socket
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

# Mots-clés suspects fréquemment utilisés dans les URLs de phishing
MOTS_SUSPECTS = [
    "login", "secure", "verify", "update", "bank",
    "account", "free", "confirm", "signin", "password",
    "credential", "suspend", "alert", "urgent"
]

# Domaines de raccourcissement d'URL connus
RACCOURCISSEURS = [
    "bit.ly", "t.co", "tinyurl.com", "rebrand.ly", "is.gd",
    "buff.ly", "goo.gl", "bit.do", "ow.ly"
]

# Timeout pour les requêtes HTTP (en secondes)
TIMEOUT_REQUETE = 5


def _calculer_entropie(chaine: str) -> float:
    """Calcule l'entropie de Shannon d'une chaîne (complexité)."""
    if not chaine:
        return 0.0
    probabilites = [float(chaine.count(c)) / len(chaine) for c in set(chaine)]
    entropie = -sum(p * math.log2(p) for p in probabilites)
    return round(entropie, 4)


def _est_adresse_ip(domaine: str) -> bool:
    """Vérifie si le domaine est une adresse IP."""
    try:
        socket.inet_aton(domaine)
        return True
    except socket.error:
        pass
    patron_ip = re.compile(r"^(\d{1,3}\.){3}\d{1,3}$")
    return bool(patron_ip.match(domaine))


def _recuperer_html(url: str) -> tuple:
    """Récupère le contenu HTML d'une URL."""
    try:
        reponse = requests.get(
            url,
            timeout=TIMEOUT_REQUETE,
            allow_redirects=True,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) PhishGuard/1.0"},
            verify=False
        )
        return reponse.text, reponse
    except Exception:
        return None, None


def _age_domaine(domaine: str) -> tuple:
    """
    Retourne (âge_en_jours, succès).
    Retourne (-1, 0) si l'information n'est pas disponible pour éviter les faux positifs.
    """
    try:
        import whois
        from datetime import datetime

        info = whois.whois(domaine)
        date_creation = info.creation_date
        if isinstance(date_creation, list):
            date_creation = date_creation[0]
        if date_creation:
            age = (datetime.now() - date_creation).days
            return max(age, 0), 1
    except Exception:
        pass
    return -1, 0


def extraire_caracteristiques(url: str) -> dict:
    """
    Extrait les caractéristiques enrichies d'une URL.
    """
    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    url_analyse = urlparse(url)
    domaine = url_analyse.netloc.split(":")[0]
    url_lower = url.lower()

    # Récupérer le contenu HTML
    html_contenu, reponse = _recuperer_html(url)
    soup = BeautifulSoup(html_contenu, "html.parser") if html_contenu else None

    # Nouvelles caractéristiques (Intelligence++)
    url_entropy = _calculer_entropie(url)
    is_shortened = 1 if any(r in domaine for r in RACCOURCISSEURS) else 0
    digit_count = sum(c.isdigit() for c in url)

    # WHOIS avec gestion robuste des échecs
    domain_age_days, whois_success = _age_domaine(domaine)

    # 1. Longueur de l'URL
    url_length = len(url)

    # 2. Utilisation de HTTPS
    has_https = 1 if url_analyse.scheme == "https" else 0

    # 3. Présence d'une adresse IP
    has_ip_address = 1 if _est_adresse_ip(domaine) else 0

    # 4. Nombre de sous-domaines
    parties_domaine = domaine.split(".")
    subdomain_count = max(len(parties_domaine) - 2, 0)

    # 5. Nombre de caractères spéciaux
    special_char_count = sum(url.count(c) for c in ["@", "%", "//", "--"])
    if "//" in url: special_char_count -= 1

    # 6. Mots-clés suspects
    has_suspicious_keywords = 1 if any(mot in url_lower for mot in MOTS_SUSPECTS) else 0

    # 7. Nombre de redirections
    redirect_count = len(reponse.history) if reponse else 0

    # 8. Favicon mismatch
    has_favicon_mismatch = 0
    if soup:
        icones = soup.find_all("link", rel=lambda x: x and "icon" in x)
        for icone in icones:
            href = icone.get("href", "")
            if href.startswith("http") and urlparse(href).netloc != url_analyse.netloc:
                has_favicon_mismatch = 1
                break

    # 9. HTML Form Count
    html_form_count = len(soup.find_all("form")) if soup else 0

    # 10. Liens externes
    external_links_ratio = 0.0
    if soup:
        liens = soup.find_all("a", href=True)
        if liens:
            nb_ext = sum(1 for l in liens if l["href"].startswith("http") and urlparse(l["href"]).netloc != url_analyse.netloc)
            external_links_ratio = round(nb_ext / len(liens), 4)

    # 11. Password input
    has_password_input = 1 if soup and soup.find_all("input", {"type": "password"}) else 0

    # 12. Titre suspect
    page_title_suspicious = 0
    if soup and soup.title and soup.title.string:
        titre = soup.title.string.lower()
        page_title_suspicious = 1 if any(mot in titre for mot in MOTS_SUSPECTS) else 0

    return {
        "url_length": url_length,
        "has_https": has_https,
        "has_ip_address": has_ip_address,
        "subdomain_count": subdomain_count,
        "special_char_count": special_char_count,
        "domain_age_days": domain_age_days,
        "whois_success": whois_success,
        "has_suspicious_keywords": has_suspicious_keywords,
        "redirect_count": redirect_count,
        "has_favicon_mismatch": has_favicon_mismatch,
        "html_form_count": html_form_count,
        "external_links_ratio": external_links_ratio,
        "has_password_input": has_password_input,
        "page_title_suspicious": page_title_suspicious,
        "url_entropy": url_entropy,
        "is_shortened": is_shortened,
        "digit_count": digit_count
    }
