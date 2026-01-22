# STORY-044: Suivi progression enfant

## Epic parent
EPIC-009: Parent/Tuteur

## Description
En tant que parent, je veux voir la progression détaillée de mon enfant.

## Critères d'acceptation spécifiques
- [ ] Profil complet de l'enfant
- [ ] Progression par EC avec statut
- [ ] Scores quiz
- [ ] Historique activités
- [ ] Graphique évolution dans le temps

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
- `frontend/src/pages/parent/ChildProgress.vue`
- `frontend/src/router.js`
- `cntemad_lms/api/guardian.py`
- `docs/INDEX.md`

## Commandes de validation
```bash
bench run-tests --app cntemad_lms --module api.guardian
npm run build --prefix frontend
```
