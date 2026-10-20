import re
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