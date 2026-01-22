# STORY-035: Page file d'attente corrections

## Epic parent
EPIC-007: Évaluateur

## Description
En tant qu'évaluateur, je veux voir la liste des soumissions à corriger.

## Critères d'acceptation spécifiques
- [ ] Liste soumissions: étudiant, EC, date soumission
- [ ] Filtres: EC, date, priorité
- [ ] Tri par date (plus ancien d'abord)
- [ ] Badge nombre en attente
- [ ] Action: commencer correction

## Critères standard (OBLIGATOIRES)

### Fonctionnel
- [ ] Comportement attendu implémenté
- [ ] Cas limites gérés (aucune soumission)
- [ ] Happy path fonctionne

### Technique
- [ ] Frappe UI utilisé (Table)
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
- `frontend/src/pages/evaluator/EvaluationQueue.vue`
- `frontend/src/router.js`
- `cntemad_lms/api/evaluation.py`
- `docs/INDEX.md`

## Commandes de validation
```bash
bench run-tests --app cntemad_lms --module api.evaluation
npm run build --prefix frontend
```
