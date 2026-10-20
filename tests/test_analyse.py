import unittest
from src.analyse import (analyser, chercher_procedures, classifier,
                         compter_erreurs, est_doublon)
from src.contrat import PROCEDURES, Evenement


def evt(type_="LOG", severity="HIGH", message="OOMKilled restarts=14",
        composant="backend", timestamp="2026-10-05T10:00:00Z"):
    return Evenement("EVT-00001", timestamp, "DOCKER", composant,
                     "production", type_, severity, message)


class TestAnalyse(unittest.TestCase):
    def test_doublon(self):
        vus = set()
        self.assertFalse(est_doublon(evt(), vus))
        self.assertTrue(est_doublon(evt(), vus))

    def test_non_doublon_secondes_differentes(self):
        vus = set()
        self.assertFalse(est_doublon(evt(timestamp="2026-10-05T10:00:00Z"), vus))
        self.assertFalse(est_doublon(evt(timestamp="2026-10-05T10:00:01Z"), vus))
