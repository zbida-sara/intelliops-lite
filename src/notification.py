from src.contrat import Analyse, Evenement, Notification


def choisir_canal(niveau: str) -> str:
    canaux = {
        "CRITICAL": "TEAMS",
        "HIGH": "SLACK",
        "MEDIUM": "EMAIL",
        "LOW": "DASHBOARD"
    }
    if niveau not in canaux:
        raise ValueError("Niveau inconnu")
    return canaux[niveau]