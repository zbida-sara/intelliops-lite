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


def rediger(evt: Evenement, analyse: Analyse) -> str:
    return (
        f"[{analyse.level}] Composant : {evt.component}\n"
        f"Evenement : {evt.message}\n"
        f"Explication : {analyse.explanation}\n"
        f"Action proposee : {analyse.action}\n"
        f"Sources : {', '.join(analyse.sources)}"
    )


def notifier(evt: Evenement, analyse: Analyse, historique: list) -> Notification:
    notif = Notification(
        evt.id,
        choisir_canal(analyse.level),
        "equipe-ops",
        rediger(evt, analyse)
    )
    historique.append(notif)
    evt.status = "NOTIFIED"
    return notif


def valider_action(analyse: Analyse, reponse: str) -> bool:
    if not analyse.sensitive:
        return True
    return reponse.strip().lower() in ("o", "oui", "ok", "yes")
