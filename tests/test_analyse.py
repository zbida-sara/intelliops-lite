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

    def test_compter_erreurs_high(self):
        compteur = {}
        self.assertEqual(compter_erreurs(evt(), compteur), 1)
        self.assertEqual(compter_erreurs(evt(), compteur), 2)
        self.assertEqual(compteur["backend"], 2)

    def test_compter_erreurs_critical(self):
        compteur = {}
        self.assertEqual(compter_erreurs(evt(severity="CRITICAL"), compteur), 1)

    def test_compter_erreurs_ignore(self):
        compteur = {}
        self.assertEqual(compter_erreurs(evt(severity="LOW"), compteur), 0)
        self.assertEqual(compter_erreurs(evt(type_="PIPELINE_FAILURE"), compteur), 0)
        self.assertEqual(compteur, {})

    def test_chercher_procedures_trouvee(self):
        res = chercher_procedures(evt(message="Container OOMKILLED"), PROCEDURES)
        self.assertEqual(res, [PROCEDURES["oomkilled"]])

    def test_chercher_procedures_ordre_base(self):
        res = chercher_procedures(evt(message="pipeline oomkilled"), PROCEDURES)
        self.assertEqual(res, [PROCEDURES["oomkilled"], PROCEDURES["pipeline"]])

    def test_chercher_procedures_vide(self):
        self.assertEqual(chercher_procedures(evt(message="rien"), PROCEDURES), [])

    def test_classifier_boucle(self):
        e = evt()
        self.assertEqual(classifier(e, 3), "CRITICAL")
        self.assertEqual(classifier(e, 2), "HIGH")

    def test_classifier_severite_par_defaut(self):
        self.assertEqual(classifier(evt(severity="MEDIUM")), "MEDIUM")

    def test_analyser_critical_sensible(self):
        e = evt()
        a = analyser(e, PROCEDURES, 3)
        self.assertEqual(a.level, "CRITICAL")
        self.assertEqual(a.action, "Redemarrer le service backend")
        self.assertTrue(a.sensitive)
        self.assertEqual(a.sources, ["DOCKER"])
        self.assertEqual(e.status, "ANALYZED")

    def test_analyser_cause_inconnue(self):
        a = analyser(evt(severity="LOW", message="Service demarre"), PROCEDURES)
        self.assertEqual(a.explanation, "Cause inconnue : analyse manuelle requise")
        self.assertEqual(a.action, "Surveiller")
        self.assertFalse(a.sensitive)

if __name__ == "__main__":
    unittest.main()
