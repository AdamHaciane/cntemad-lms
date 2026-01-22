# STORY-036: Page correction détail

## Epic parent
EPIC-007: Évaluateur

## Description
En tant qu'évaluateur, je veux corriger une soumission en détail.

## Critères d'acceptation spécifiques
- [ ] Affichage soumission étudiant
- [ ] GradeInput pour la note
- [ ] FeedbackEditor pour commentaires
- [ ] Boutons: Valider, Rejeter, Sauvegarder brouillon
- [ ] Navigation vers suivant après validation

## Critères standard (OBLIGATOIRES)

### Fonctionnel
- [ ] Comportement attendu implémenté
- [ ] Cas limites gérés
- [ ] Happy path fonctionne

### Technique
- [ ] Frappe UI utilisé
- [ ] Code propre, pas de debug
- [ ] Pas de credentials en dur

### Tests
- [ ] Tests unitaires écrits
- [ ] `bench run-tests` passe
- [ ] Test manuel OK
- [ ] Mobile responsive vérifié

### Intégration
- [ ] `bench build` passe
- [ ] `bench migrate` passe
- [ ] Pas de régression

### Documentation
- [ ] INDEX.md mis à jour

## Fichiers impactés
- `frontend/src/pages/evaluator/EvaluationDetail.vue`
- `frontend/src/router.js`
- `cntemad_lms/api/evaluation.py`
- `docs/INDEX.md`

## Commandes de validation
```bash
bench run-tests --app cntemad_lms --module api.evaluation
npm run build --prefix frontend
```
