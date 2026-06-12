"""
Extracteur de caractéristiques — Extrait 13 caractéristiques d'une URL
pour la détection de phishing.
"""

import re
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

# Timeout pour les requêtes HTTP (en secondes)
TIMEOUT_REQUETE = 5


def _est_adresse_ip(domaine: str) -> bool:
    """Vérifie si le domaine est une adresse IP."""
    try:
        socket.inet_aton(domaine)
        return True
    except socket.error:
        pass
    # Vérifier aussi le format IPv4 avec regex
    patron_ip = re.compile(
        r"^(\d{1,3}\.){3}\d{1,3}$"
    )
    return bool(patron_ip.match(domaine))


def _recuperer_html(url: str) -> tuple:
    """
    Récupère le contenu HTML d'une URL.
    Retourne (html_content, response) ou (None, None) en cas d'erreur.
    """
    try:
        reponse = requests.get(
            url,
            timeout=TIMEOUT_REQUETE,
            allow_redirects=True,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                )
            },
            verify=False  # Ignorer les erreurs SSL pour l'analyse
        )
        return reponse.text, reponse
    except Exception:
        return None, None


def _compter_redirections(url: str) -> int:
    """Compte le nombre de redirections lors de la requête."""
    try:
        reponse = requests.get(
            url,
            timeout=TIMEOUT_REQUETE,
            allow_redirects=True,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36"
                )
            },
            verify=False
        )
        return len(reponse.history)
    except Exception:
        return 0


def _age_domaine(domaine: str) -> int:
    """
    Retourne l'âge du domaine en jours via python-whois.
    Retourne 0 si l'information n'est pas disponible.
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
            return max(age, 0)
    except Exception:
        pass
    return 0


def _verifier_favicon(url: str, soup: BeautifulSoup, domaine_url: str) -> int:
    """
    Vérifie si le favicon provient d'un domaine différent de l'URL.
    Retourne 1 si le domaine du favicon diffère.
    """
    try:
        # Chercher la balise link avec rel="icon" ou rel="shortcut icon"
        icones = soup.find_all("link", rel=lambda x: x and "icon" in x)
        for icone in icones:
            href = icone.get("href", "")
            if href.startswith("http"):
                domaine_favicon = urlparse(href).netloc
                if domaine_favicon and domaine_favicon != domaine_url:
                    return 1
    except Exception:
        pass
    return 0


def _ratio_liens_externes(soup: BeautifulSoup, domaine_url: str) -> float:
    """
    Calcule le ratio de liens externes par rapport au total des liens.
    """
    try:
        liens = soup.find_all("a", href=True)
        if not liens:
            return 0.0

        nb_externes = 0
        for lien in liens:
            href = lien["href"]
            if href.startswith("http"):
                domaine_lien = urlparse(href).netloc
                if domaine_lien and domaine_lien != domaine_url:
                    nb_externes += 1

        return round(nb_externes / len(liens), 4)
    except Exception:
        return 0.0


def extraire_caracteristiques(url: str) -> dict:
    """
    Extrait les 13 caractéristiques d'une URL pour la détection de phishing.

    Args:
        url: L'URL à analyser

    Returns:
        Dictionnaire contenant les 13 caractéristiques extraites
    """
    # Assurer que l'URL a un schéma
    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    url_analyse = urlparse(url)
    domaine = url_analyse.netloc
    url_lower = url.lower()

    # Récupérer le contenu HTML
    html_contenu, reponse = _recuperer_html(url)
    soup = BeautifulSoup(html_contenu, "html.parser") if html_contenu else None

    # 1. Longueur de l'URL
    url_length = len(url)

    # 2. Utilisation de HTTPS
    has_https = 1 if url_analyse.scheme == "https" else 0

    # 3. Présence d'une adresse IP dans le domaine
    has_ip_address = 1 if _est_adresse_ip(domaine.split(":")[0]) else 0

    # 4. Nombre de sous-domaines
    parties_domaine = domaine.split(":")[0].split(".")
    # Retirer le TLD et le domaine principal, le reste sont les sous-domaines
    subdomain_count = max(len(parties_domaine) - 2, 0)

    # 5. Nombre de caractères spéciaux
    caracteres_speciaux = ["@", "%", "//", "--"]
    special_char_count = sum(url.count(c) for c in caracteres_speciaux)
    # Retirer le premier // du schéma
    if "//" in url:
        special_char_count -= 1

    # 6. Âge du domaine en jours
    domain_age_days = _age_domaine(domaine.split(":")[0])

    # 7. Mots-clés suspects dans l'URL
    has_suspicious_keywords = 1 if any(
        mot in url_lower for mot in MOTS_SUSPECTS
    ) else 0

    # 8. Nombre de redirections
    redirect_count = _compter_redirections(url)

    # 9. Favicon provenant d'un domaine différent
    has_favicon_mismatch = 0
    if soup:
        has_favicon_mismatch = _verifier_favicon(url, soup, domaine)

    # 10. Nombre de formulaires dans la page
    html_form_count = 0
    if soup:
        html_form_count = len(soup.find_all("form"))

    # 11. Ratio de liens externes
    external_links_ratio = 0.0
    if soup:
        external_links_ratio = _ratio_liens_externes(soup, domaine)

    # 12. Présence d'un champ mot de passe
    has_password_input = 0
    if soup:
        champs_mdp = soup.find_all("input", {"type": "password"})
        has_password_input = 1 if champs_mdp else 0

    # 13. Titre de page suspect
    page_title_mismatch = 0
    if soup and soup.title and soup.title.string:
        titre = soup.title.string.lower()
        page_title_mismatch = 1 if any(
            mot in titre for mot in MOTS_SUSPECTS
        ) else 0

    return {
        "url_length": url_length,
        "has_https": has_https,
        "has_ip_address": has_ip_address,
        "subdomain_count": subdomain_count,
        "special_char_count": special_char_count,
        "domain_age_days": domain_age_days,
        "has_suspicious_keywords": has_suspicious_keywords,
        "redirect_count": redirect_count,
        "has_favicon_mismatch": has_favicon_mismatch,
        "html_form_count": html_form_count,
        "external_links_ratio": external_links_ratio,
        "has_password_input": has_password_input,
        "page_title_mismatch": page_title_mismatch,
    }
