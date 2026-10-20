# Changelog
## [Non publie]
- Agent Notification : canaux, redaction, historique, validation humaine et audit (C).## [0.1.0]
- Squelette du projet : contrat, agents vides, workflow, demo.

Implémentation de la fonction `extraire_metadonnees` pour analyser les niveaux de sévérité, les services et détecter les procédures recommandées dans les logs.
- **Tests Extraction** (`tests/test_extraction.py`) : Ajout de la suite de tests unitaires couvrant l'extraction du niveau, du service, de la procédure `oomkilled` et le comportement sur log neutre.