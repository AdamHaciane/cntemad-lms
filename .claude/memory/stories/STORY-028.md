# STORY-028: Stats par EC

## Epic parent
EPIC-005: Enseignant & Création Contenu

## Description
En tant qu'enseignant, je veux voir les statistiques de mes EC.

## Critères d'acceptation spécifiques
- [ ] Nb étudiants inscrits
- [ ] Nb étudiants ayant terminé
- [ ] Taux de réussite quiz
- [ ] Score moyen quiz
- [ ] Graphique progression dans le temps

## Critères standard (OBLIGATOIRES)

### Fonctionnel
- [ ] Comportement attendu implémenté
- [ ] Cas limites gérés (aucun étudiant)
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
- `frontend/src/pages/teacher/ECStats.vue`
- `frontend/src/router.js`
- `cntemad_lms/api/stats.py`
- `docs/INDEX.md`

## Commandes de validation
```bash
bench run-tests --app cntemad_lms --module api.stats
npm run build --prefix frontend
```
