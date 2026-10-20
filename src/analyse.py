from src.contrat import Analyse, Evenement


def est_doublon(evt: Evenement, vus: set) -> bool:
    cle = (evt.timestamp, evt.source, evt.component, evt.event_type, evt.message)
    if cle in vus:
        return True
    vus.add(cle)
    return False