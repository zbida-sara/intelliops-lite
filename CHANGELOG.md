# Changelog
## [Non publie]
- Agent Analyse : filtrage et classification (B)
- Agent Notification : canaux, redaction, historique, validation humaine et audit (C).
- Agent Extraction : implementation de la fonction `extraire_metadonnees` pour analyser les niveaux de severite, les services et detecter les procedures recommandees dans les logs (A).
- **Tests Extraction** (`tests/test_extraction.py`) : Ajout de la suite de tests unitaires couvrant l'extraction du niveau, du service, de la procedure `oomkilled` et le comportement sur log neutre (A).
## [0.1.0]
- Squelette du projet : contrat, agents vides, workflow, demo.
