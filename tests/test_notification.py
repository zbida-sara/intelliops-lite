
import unittest

from src.contrat import Analyse, Evenement
from src.notification import choisir_canal, notifier, rediger

def exemple(sensible=True, niveau="CRITICAL"):
    e = Evenement("EVT-00125", "2026-10-05T10:02:11Z", "DOCKER",
                  "backend", "production", "LOG", "HIGH",
                  "OOMKilled restarts=14")
    a = Analyse("EVT-00125", niveau, "Manque de memoire",
                "Redemarrer le service backend", sensible, ["DOCKER"])
    return e, a


class TestNotification(unittest.TestCase):
    def test_canaux(self):
        self.assertEqual(choisir_canal("CRITICAL"), "TEAMS")
        self.assertEqual(choisir_canal("HIGH"), "SLACK")
        self.assertEqual(choisir_canal("MEDIUM"), "EMAIL")
        self.assertEqual(choisir_canal("LOW"), "DASHBOARD")

    def test_canal_invalide(self):
        with self.assertRaises(ValueError):
            choisir_canal("UNKNOWN")


    def test_rediger(self):
        evt, analyse = exemple()
        texte = rediger(evt, analyse)

        self.assertEqual(texte.splitlines(), [
            "[CRITICAL] Composant : backend",
            "Evenement : OOMKilled restarts=14",
            "Explication : Manque de memoire",
            "Action proposee : Redemarrer le service backend",
            "Sources : DOCKER"
        ])


    def test_notifier(self):
        evt, analyse = exemple()
        historique = []

        notif = notifier(evt, analyse, historique)

        self.assertEqual(notif.event_id, evt.id)
        self.assertEqual(notif.channel, "TEAMS")
        self.assertEqual(notif.recipient, "equipe-ops")
        self.assertEqual(notif.text, rediger(evt, analyse))
        self.assertEqual(evt.status, "NOTIFIED")
        self.assertEqual(historique, [notif])
