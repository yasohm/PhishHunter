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

# Plateformes de création de sites web fréquemment détournées pour le phishing
PLATEFORMES_HEBERGEMENT = [
    "wixsite.com", "wixstudio.com", "sites.google.com", "weebly.com",
    "blogspot.com", "000webhostapp.com", "firebaseapp.com", "github.io",
    "web.app", "vercel.app", "netlify.app", "pages.dev"
]

# Plateformes de stockage cloud souvent utilisées pour héberger du phishing
STOCKAGE_CLOUD = [
    "contabostorage.com", "s3.amazonaws.com", "s3-", ".amazonaws.com",
    "storage.googleapis.com", "blob.core.windows.net",
    "digitaloceanspaces.com", "r2.cloudflarestorage.com",
    "objectstorage.", "cellar-c2.services.clever-cloud.com",
    "storage.yandexcloud.net", "obs.otc.t-systems.com",
    "supabase.co/storage", "firebasestorage.googleapis.com"
]

# Mots-clés liés au vol de credentials dans les chemins d'URL
MOTS_CREDENTIAL = [
    "login", "signin", "sign-in", "verify", "secure", "account",
    "password", "excel", "onedrive", "sharepoint", "office365",
    "microsoft", "outlook", "document", "docusign", "wetransfer",
    "dropbox", "invoice", "payment", "billing", "wallet",
    "metamask", "blockchain", "recover", "suspend", "confirm"
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


def _chemin_suspect(chemin: str) -> bool:
    """Détecte les patterns suspects dans le chemin de l'URL."""
    if not chemin or chemin == "/":
        return False
    chemin_lower = chemin.lower()

    # Tokens hexadécimaux longs (24+ chars) — courants dans les buckets phishing jetables
    if re.search(r'[0-9a-f]{24,}', chemin_lower):
        return True

    # Mots-clés de vol de credentials dans le chemin
    if any(mot in chemin_lower for mot in MOTS_CREDENTIAL):
        return True

    # UUID patterns dans le chemin (ex: /be6dfdc1-dc04-432f-81e1-265debc2fa11/)
    if re.search(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', chemin_lower):
        return True

    return False


def _est_stockage_cloud(domaine: str) -> bool:
    """Vérifie si le domaine est un service de stockage cloud."""
    return any(s in domaine for s in STOCKAGE_CLOUD)



def _recuperer_html(url: str) -> tuple:
    """Récupère le contenu HTML d'une URL."""
    try:
        reponse = requests.get(
            url,
            timeout=TIMEOUT_REQUETE,
            allow_redirects=True,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) PhishHunter/1.0"},
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
    Extrait les caractéristiques d'une URL et les mappe au format UCI (-1, 0, 1).
    """
    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    url_analyse = urlparse(url)
    domaine = url_analyse.netloc.split(":")[0]
    url_lower = url.lower()

    # Récupérer le contenu HTML
    html_contenu, reponse = _recuperer_html(url)
    soup = BeautifulSoup(html_contenu, "html.parser") if html_contenu else None

    # --- 1. having_IP_Address ---
    having_IP_Address = -1 if _est_adresse_ip(domaine) else 1

    # --- 2. URL_Length ---
    if len(url) < 54:
        URL_Length = 1
    elif 54 <= len(url) <= 75:
        URL_Length = 0
    else:
        URL_Length = -1

    # --- 3. Shortining_Service ---
    Shortining_Service = -1 if any(r in domaine for r in RACCOURCISSEURS) else 1

    # --- 4. having_At_Symbol ---
    having_At_Symbol = -1 if "@" in url else 1

    # --- 5. double_slash_redirecting ---
    # On cherche // après le protocole (index 7 pour http://, 8 pour https://)
    double_slash_redirecting = -1 if url.rfind("//") > 7 else 1

    # --- 6. Prefix_Suffix ---
    Prefix_Suffix = -1 if "-" in domaine else 1

    # --- 7. having_Sub_Domain ---
    parties = domaine.split(".")
    # Détection de mots-clés suspects dans le sous-domaine
    # Exemple: paypal.secure-login.wixstudio.com
    sous_domaine = ".".join(parties[:-2]) if len(parties) > 2 else ""
    contient_mots_suspects = any(mot in sous_domaine.lower() for mot in MOTS_SUSPECTS)
    est_cloud = _est_stockage_cloud(domaine)

    # UCI: Dots < 3 -> 1, Dots = 3 -> 0, Dots > 3 -> -1
    dots = len(parties) - 1
    if contient_mots_suspects or dots > 3:
        having_Sub_Domain = -1
    elif dots == 3 or est_cloud:
        having_Sub_Domain = 0  # Cloud storage = suspect au minimum
    else:
        having_Sub_Domain = 1

    # --- 8. SSLfinal_State ---
    if url_analyse.scheme == "https":
        SSLfinal_State = 1 # On simplifie, idéalement vérifier le certificat
    else:
        SSLfinal_State = -1

    # --- 9. Domain_registeration_length ---
    # --- 24. age_of_domain ---
    domain_age, whois_success = _age_domaine(domaine)
    if whois_success:
        age_of_domain = 1 if domain_age >= 180 else -1
        Domain_registeration_length = 1 if domain_age >= 365 else -1
    else:
        age_of_domain = -1
        Domain_registeration_length = -1

    # --- 10. Favicon ---
    Favicon = 1
    if soup:
        icones = soup.find_all("link", rel=lambda x: x and "icon" in x)
        for icone in icones:
            href = icone.get("href", "")
            if href.startswith("http") and urlparse(href).netloc != url_analyse.netloc:
                Favicon = -1
                break

    # --- 11. port ---
    # UCI: Port standard (80, 443) -> 1, Non-standard -> -1
    port_url = url_analyse.port
    if port_url is None:
        port = 1
    elif port_url in [80, 443]:
        port = 1
    else:
        port = -1

    # --- 12. HTTPS_token ---
    HTTPS_token = -1 if "https" in domaine else 1

    # --- 13. Request_URL ---
    Request_URL = 1
    if soup:
        liens_objets = soup.find_all(['img', 'video', 'audio'], src=True)
        if liens_objets:
            nb_ext = sum(1 for l in liens_objets if urlparse(l['src']).netloc != url_analyse.netloc and urlparse(l['src']).netloc != "")
            ratio = nb_ext / len(liens_objets)
            Request_URL = 1 if ratio < 0.22 else (-1 if ratio > 0.61 else 0)

    # --- 14. URL_of_Anchor ---
    URL_of_Anchor = 1
    if soup:
        liens = soup.find_all("a", href=True)
        if liens:
            nb_ext = sum(1 for l in liens if urlparse(l['href']).netloc != url_analyse.netloc and urlparse(l['href']).netloc != "")
            ratio = nb_ext / len(liens)
            URL_of_Anchor = 1 if ratio < 0.31 else (-1 if ratio > 0.67 else 0)

    # --- 15. Links_in_tags ---
    Links_in_tags = 1
    if soup:
        tags = soup.find_all(['link', 'script', 'meta'])
        nb_ext = 0
        for t in tags:
            src = t.get('src') or t.get('href')
            if src and urlparse(src).netloc != url_analyse.netloc and urlparse(src).netloc != "":
                nb_ext += 1
        if tags:
            ratio = nb_ext / len(tags)
            Links_in_tags = 1 if ratio < 0.17 else (-1 if ratio > 0.81 else 0)

    # --- 16. SFH (Server Form Handler) ---
    SFH = 1
    if soup:
        formulaires = soup.find_all("form", action=True)
        for f in formulaires:
            action = f["action"].lower()
            if action == "" or action == "about:blank":
                SFH = -1
                break
            # Si le domaine d'action du formulaire est différent du domaine actuel
            if action.startswith("http"):
                if urlparse(action).netloc != url_analyse.netloc:
                    SFH = 0 # Suspect
                    break

    # --- 17. Submitting_to_email ---
    Submitting_to_email = 1
    if html_contenu:
        html_lower_content = html_contenu.lower()
        if "mailto:" in html_lower_content or "mail()" in html_lower_content:
            Submitting_to_email = -1

    # --- 18. Abnormal_URL ---
    Abnormal_URL = 1
    est_cloud = _est_stockage_cloud(domaine)
    chemin_suspect = _chemin_suspect(url_analyse.path)

    # 1. Stockage cloud + chemin suspect = phishing très probable
    if est_cloud and chemin_suspect:
        Abnormal_URL = -1
    # 2. Stockage cloud seul = suspect
    elif est_cloud:
        Abnormal_URL = 0
    # 3. Chemin suspect seul = suspect
    elif chemin_suspect:
        Abnormal_URL = 0
    # 4. Vérification des plateformes d'hébergement gratuites
    elif any(p in domaine for p in PLATEFORMES_HEBERGEMENT):
        if contient_mots_suspects or Prefix_Suffix == -1:
            Abnormal_URL = -1
    
    # 5. Vérification WHOIS vs Domaine
    if whois_success and Abnormal_URL == 1:
        try:
            import whois
            w = whois.whois(domaine)
            nom_registre = str(w.get('org', '') or w.get('name', '')).lower()
            if nom_registre and nom_registre != "none" and not any(p in domaine for p in nom_registre.split()):
                pass 
        except Exception:
            pass

    # --- 19. Redirect ---
    Redirect = 0
    if reponse and len(reponse.history) > 1:
        Redirect = 1

    # --- 20. on_mouseover ---
    on_mouseover = 1
    if html_contenu and "window.status" in html_contenu:
        on_mouseover = -1

    # --- 21. RightClick ---
    RightClick = 1
    if html_contenu and "event.button==2" in html_contenu:
        RightClick = -1

    # --- 22. popUpWidnow ---
    popUpWidnow = 1
    if html_contenu:
        if "window.open(" in html_contenu or "prompt(" in html_contenu:
            popUpWidnow = -1
    
    # --- 23. Iframe ---
    Iframe = 1
    if soup and soup.find_all("iframe"):
        Iframe = -1

    # --- 25. DNSRecord ---
    DNSRecord = 1 if whois_success else -1

    # Autres (difficiles à obtenir dynamiquement sans APIs tierces)
    web_traffic = 0
    Page_Rank = 0
    Google_Index = 0
    Links_pointing_to_page = 0
    Statistical_report = 0

    return {
        "having_IP_Address": having_IP_Address,
        "URL_Length": URL_Length,
        "Shortining_Service": Shortining_Service,
        "having_At_Symbol": having_At_Symbol,
        "double_slash_redirecting": double_slash_redirecting,
        "Prefix_Suffix": Prefix_Suffix,
        "having_Sub_Domain": having_Sub_Domain,
        "SSLfinal_State": SSLfinal_State,
        "Domain_registeration_length": Domain_registeration_length,
        "Favicon": Favicon,
        "port": port,
        "HTTPS_token": HTTPS_token,
        "Request_URL": Request_URL,
        "URL_of_Anchor": URL_of_Anchor,
        "Links_in_tags": Links_in_tags,
        "SFH": SFH,
        "Submitting_to_email": Submitting_to_email,
        "Abnormal_URL": Abnormal_URL,
        "Redirect": Redirect,
        "on_mouseover": on_mouseover,
        "RightClick": RightClick,
        "popUpWidnow": popUpWidnow,
        "Iframe": Iframe,
        "age_of_domain": age_of_domain,
        "DNSRecord": DNSRecord,
        "web_traffic": web_traffic,
        "Page_Rank": Page_Rank,
        "Google_Index": Google_Index,
        "Links_pointing_to_page": Links_pointing_to_page,
        "Statistical_report": Statistical_report
    }
