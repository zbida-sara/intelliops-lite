import re
from src.contrat import Evenement
from typing import Dict, Any


def extraire_metadonnees(log_text: str) -> Dict[Any, Any]:
    """
    Extrait les métadonnées clés d'une ligne ou d'un bloc de log textuel.
    """
    metadonnees = {}

    # Extraction du niveau de sévérité (LOG, WARNING, ERROR, CRITICAL)
    match_level = re.search(r"\b(INFO|WARNING|ERROR|CRITICAL)\b", log_text)
    if match_level:
        metadonnees["level"] = match_level.group(1)

    # Extraction du composant/service entre crochets ou clés
    match_service = re.search(r"\[(.*?)\]", log_text)
    if match_service:
        metadonnees["service"] = match_service.group(1)

    # Détection de mots-clés d'erreurs ou de procédures
    if "oomkilled" in log_text.lower():
        metadonnees["action_recommandee"] = "redemarrage_container"
    elif "disk full" in log_text.lower():
        metadonnees["action_recommandee"] = "nettoyage_disque"

    return metadonnees


_PATTERN_SECRET = re.compile(
    r"(?P<nom>password|passwd|token|secret|api_key|apikey)(?P<sep>\s*[=:]\s*)(?P<val>[^\s&,;]+)",
    re.IGNORECASE,
)
_PATTERN_BEARER = re.compile(r"(?P<pre>\bBearer\s+)(?P<val>[^\s&,;]+)", re.IGNORECASE)

def masquer_secrets(texte: str) -> str:
    texte = _PATTERN_SECRET.sub(lambda m: f"{m.group('nom')}{m.group('sep')}[SECRET]", texte)
    texte = _PATTERN_BEARER.sub(lambda m: f"{m.group('pre')}[SECRET]", texte)
    return texte


def normaliser_log(ligne: str, numero: int, source: str = "DOCKER",
                  environment: str = "production") -> Evenement:
    parties = ligne.split(maxsplit=4)
    if len(parties) < 5:
        raise ValueError("Format de log invalide")

    date, heure, niveau, composant, message = parties
    niveau = niveau.upper()

    if niveau in ("CRITICAL", "FATAL"):
        severity = "CRITICAL"
    elif niveau == "ERROR":
        severity = "HIGH"
    elif niveau in ("WARN", "WARNING"):
        severity = "MEDIUM"
    else:
        severity = "LOW"

    return Evenement(
        f"EVT-{numero:05d}",
        f"{date}T{heure}Z",
        source,
        composant,
        environment,
        "LOG",
        severity,
        masquer_secrets(message)
    )


def normaliser_scan(rapport: dict, numero: int,
                   environment: str = "production") -> Evenement:
    if any(cle not in rapport for cle in ("cve", "package", "severity", "date")):
        raise ValueError("Rapport de scan incomplet")

    severity = rapport["severity"].upper()
    if severity not in ("CRITICAL", "HIGH", "MEDIUM", "LOW"):
        severity = "LOW"

    return Evenement(
        f"EVT-{numero:05d}",
        rapport["date"],
        "TRIVY",
        rapport["package"],
        environment,
        "VULNERABILITY",
        severity,
        f"Vulnerabilite {rapport['cve']} dans {rapport['package']}"
    )


def normaliser_pipeline(rapport: dict, numero: int,
                       environment: str = "production") -> Evenement:
    if any(cle not in rapport for cle in ("job", "status", "date")):
        raise ValueError("Rapport de pipeline incomplet")

    failed = rapport["status"].lower() == "failed"

    return Evenement(
        f"EVT-{numero:05d}",
        rapport["date"],
        "CI",
        rapport["job"],
        environment,
        "PIPELINE_FAILURE" if failed else "PIPELINE_OK",
        "HIGH" if failed else "LOW",
        f"Pipeline {rapport['job']} : {rapport['status']}"
    )
