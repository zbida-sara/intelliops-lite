
import unittest
from src.extraction import extraire_metadonnees


class TestExtraction(unittest.TestCase):

    def test_extraction_niveau_et_service(self):
        log = "2026-10-20 10:00:00 [backend] ERROR Connexion refusée"
        resultat = extraire_metadonnees(log)

        self.assertEqual(resultat.get("level"), "ERROR")
        self.assertEqual(resultat.get("service"), "backend")

    def test_detection_procedure_oomkilled(self):
        log = "2026-10-20 10:05:00 [docker] CRITICAL Process OOMKilled detected"
        resultat = extraire_metadonnees(log)

        self.assertEqual(resultat.get("action_recommandee"), "redemarrage_container")

    def test_log_sans_metadonnees(self):
        log = "Ligne de texte standard sans métadonnées"
        resultat = extraire_metadonnees(log)

        self.assertNotIn("level", resultat)
        self.assertNotIn("service", resultat)


if __name__ == "__main__":
    unittest.main()